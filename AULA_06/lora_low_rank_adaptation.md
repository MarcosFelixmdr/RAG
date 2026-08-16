## LORA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS

Edward Hu Yuanzhi Li

∗

Yelong Shen ∗ Shean Wang

Phillip Wallis

Zeyuan Allen-Zhu Weizhu Chen

Lu Wang

Microsoft Corporation

{ edwardhu, yeshe, phwallis, zeyuana, yuanzhil, swang, luw, wzchen } @microsoft.com yuanzhil@andrew.cmu.edu

(Version 2)

## ABSTRACT

An important paradigm of natural language processing consists of large-scale pretraining on general domain data and adaptation to particular tasks or domains. As we pre-train larger models, full fine-tuning, which retrains all model parameters, becomes less feasible. Using GPT-3 175B as an example - deploying independent instances of fine-tuned models, each with 175B parameters, is prohibitively expensive. We propose Lo wR ank A daptation, or LoRA, which freezes the pretrained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, greatly reducing the number of trainable parameters for downstream tasks. Compared to GPT-3 175B fine-tuned with Adam, LoRA can reduce the number of trainable parameters by 10,000 times and the GPU memory requirement by 3 times. LoRA performs on-par or better than finetuning in model quality on RoBERTa, DeBERTa, GPT-2, and GPT-3, despite having fewer trainable parameters, a higher training throughput, and, unlike adapters, no additional inference latency . We also provide an empirical investigation into rank-deficiency in language model adaptation, which sheds light on the efficacy of LoRA. We release a package that facilitates the integration of LoRA with PyTorch models and provide our implementations and model checkpoints for RoBERTa, DeBERTa, and GPT-2 at https://github.com/microsoft/LoRA .

## 1 INTRODUCTION

Many applications in natural language processing rely on adapting one large-scale, pre-trained language model to multiple downstream applications. Such adaptation is usually done via fi ne-tuning , which updates all the parameters of the pre-trained model. The major downside of fine-tuning is that the new model contains as many parameters as in the original model. As larger models are trained every few months, this changes from a mere 'inconvenience' for GPT-2 (Radford et al., b) or RoBERTa large (Liu et al., 2019) to a critical deployment challenge for GPT-3 (Brown et al., 2020) with 175 billion trainable parameters. 1

Many sought to mitigate this by adapting only some parameters or learning external modules for new tasks. This way, we only need to store and load a small number of task-specific parameters in addition to the pre-trained model for each task, greatly boosting the operational efficiency when deployed. However, existing techniques f(x)

∗ Equal contribution.

0

1 mance significantly as shown in Appendix A.

Compared to V1, this draft includes better baselines, experiments on GLUE, and more on adapter latency. While GPT-3 175B achieves non-trivial performance with few-shot learning, fine-tuning boosts its perfor-

Figure 1: Our reparametrization. We only train A and B .

<!-- image -->

Pretrained

Weights

𝑊 ∈ ℝ 𝑑×𝑑

x

𝑑

often introduce inference latency (Houlsby et al., 2019; Rebuffi et al., 2017) by extending model depth or reduce the model's usable sequence length (Li &amp; Liang, 2021; Lester et al., 2021; Hambardzumyan et al., 2020; Liu et al., 2021) (Section 3). More importantly, these method often fail to match the fine-tuning baselines, posing a trade-off between efficiency and model quality.

We take inspiration from Li et al. (2018a); Aghajanyan et al. (2020) which show that the learned over-parametrized models in fact reside on a low intrinsic dimension. We hypothesize that the change in weights during model adaptation also has a low 'intrinsic rank', leading to our proposed Lo wR ank A daptation (LoRA) approach. LoRA allows us to train some dense layers in a neural network indirectly by optimizing rank decomposition matrices of the dense layers' change during adaptation instead, while keeping the pre-trained weights frozen, as shown in Figure 1. Using GPT-3 175B as an example, we show that a very low rank (i.e., r in Figure 1 can be one or two) suffices even when the full rank (i.e., d ) is as high as 12,288, making LoRA both storage- and compute-efficient.

LoRA possesses several key advantages.

- A pre-trained model can be shared and used to build many small LoRA modules for different tasks. We can freeze the shared model and efficiently switch tasks by replacing the matrices A and B in Figure 1, reducing the storage requirement and task-switching overhead significantly.
- LoRA makes training more efficient and lowers the hardware barrier to entry by up to 3 times when using adaptive optimizers since we do not need to calculate the gradients or maintain the optimizer states for most parameters. Instead, we only optimize the injected, much smaller low-rank matrices.
- Our simple linear design allows us to merge the trainable matrices with the frozen weights when deployed, introducing no inference latency compared to a fully fine-tuned model, by construction.
- LoRA is orthogonal to many prior methods and can be combined with many of them, such as prefix-tuning. We provide an example in Appendix E.

Terminologies and Conventions We make frequent references to the Transformer architecture and use the conventional terminologies for its dimensions. We call the input and output dimension size of a Transformer layer d model . We use W q , W k , W v , and W o to refer to the query/key/value/output projection matrices in the self-attention module. W or W 0 refers to a pretrained weight matrix and ∆ W its accumulated gradient update during adaptation. We use r to denote the rank of a LoRA module. We follow the conventions set out by (Vaswani et al., 2017; Brown et al., 2020) and use Adam (Loshchilov &amp; Hutter, 2019; Kingma &amp; Ba, 2017) for model optimization and use a Transformer MLP feedforward dimension d ffn = 4 × d model .

## 2 PROBLEM STATEMENT

While our proposal is agnostic to training objective, we focus on language modeling as our motivating use case. Below is a brief description of the language modeling problem and, in particular, the maximization of conditional probabilities given a task-specific prompt.

Suppose we are given a pre-trained autoregressive language model P Φ ( y | x ) parametrized by Φ . For instance, P Φ ( y | x ) can be a generic multi-task learner such as GPT (Radford et al., b; Brown et al., 2020) based on the Transformer architecture (Vaswani et al., 2017). Consider adapting this pre-trained model to downstream conditional text generation tasks, such as summarization, machine reading comprehension (MRC), and natural language to SQL (NL2SQL). Each downstream task is represented by a training dataset of context-target pairs: Z = { ( x i , y i ) } i =1 ,..,N , where both x i and y i are sequences of tokens. For example, in NL2SQL, x i is a natural language query and y i its corresponding SQL command; for summarization, x i is the content of an article and y i its summary.

During full fine-tuning, the model is initialized to pre-trained weights Φ 0 and updated to Φ 0 +∆Φ by repeatedly following the gradient to maximize the conditional language modeling objective:

<!-- formula-not-decoded -->

One of the main drawbacks for full fine-tuning is that for each downstream task, we learn a different set of parameters ∆Φ whose dimension | ∆Φ | equals | Φ 0 | . Thus, if the pre-trained model is large (such as GPT-3 with | Φ 0 | ≈ 175 Billion), storing and deploying many independent instances of fine-tuned models can be challenging, if at all feasible.

In this paper, we adopt a more parameter-efficient approach, where the task-specific parameter increment ∆Φ = ∆Φ(Θ) is further encoded by a much smaller-sized set of parameters Θ with | Θ | ≪| Φ 0 | . The task of finding ∆Φ thus becomes optimizing over Θ :

<!-- formula-not-decoded -->

In the subsequent sections, we propose to use a low-rank representation to encode ∆Φ that is both compute- and memory-efficient. When the pre-trained model is GPT-3 175B, the number of trainable parameters | Θ | can be as small as 0 . 01% of | Φ 0 | .

## 3 AREN'T EXISTING SOLUTIONS GOOD ENOUGH?

The problem we set out to tackle is by no means new. Since the inception of transfer learning, dozens of works have sought to make model adaptation more parameter- and compute-efficient. See Section 6 for a survey of some of the well-known works. Using language modeling as an example, there are two prominent strategies when it comes to efficient adaptations: adding adapter layers (Houlsby et al., 2019; Rebuffi et al., 2017; Pfeiffer et al., 2021; R¨ uckl´ e et al., 2020) or optimizing some forms of the input layer activations (Li &amp; Liang, 2021; Lester et al., 2021; Hambardzumyan et al., 2020; Liu et al., 2021). However, both strategies have their limitations, especially in a large-scale and latency-sensitive production scenario.

Adapter Layers Introduce Inference Latency There are many variants of adapters. We focus on the original design by Houlsby et al. (2019) which has two adapter layers per Transformer block and a more recent one by Lin et al. (2020) which has only one per block but with an additional LayerNorm (Ba et al., 2016). While one can reduce the overall latency by pruning layers or exploiting multi-task settings (R¨ uckl´ e et al., 2020; Pfeiffer et al., 2021), there is no direct ways to bypass the extra compute in adapter layers. This seems like a non-issue since adapter layers are designed to have few parameters (sometimes &lt; 1% of the original model) by having a small bottleneck dimension, which limits the FLOPs they can add. However, large neural networks rely on hardware parallelism to keep the latency low, and adapter layers have to be processed sequentially. This makes a difference in the online inference setting where the batch size is typically as small as one. In a generic scenario without model parallelism, such as running inference on GPT-2 (Radford et al., b) medium on a single GPU, we see a noticeable increase in latency when using adapters, even with a very small bottleneck dimension (Table 1).

This problem gets worse when we need to shard the model as done in Shoeybi et al. (2020); Lepikhin et al. (2020), because the additional depth requires more synchronous GPU operations such as AllReduce and Broadcast , unless we store the adapter parameters redundantly many times.

Directly Optimizing the Prompt is Hard The other direction, as exemplified by prefix tuning (Li &amp; Liang, 2021), faces a different challenge. We observe that prefix tuning is difficult to optimize and that its performance changes non-monotonically in trainable parameters, confirming similar observations in the original paper. More fundamentally, reserving a part of the sequence length for adaptation necessarily reduces the sequence length available to process a downstream task, which we suspect makes tuning the prompt less performant compared to other methods. We defer the study on task performance to Section 5.

| Batch Size      | 32                   | 16                  | 1                   |
|-----------------|----------------------|---------------------|---------------------|
| Sequence Length | 512                  | 256                 | 128                 |
| &#124; Θ &#124; | 0.5M                 | 11M                 | 11M                 |
| Fine-Tune/LoRA  | 1449.4 ± 0.8         | 338.0 ± 0.6         | 19.8 ± 2.7          |
| Adapter L H     | 1482.0 ± 1.0 (+2.2%) | 354.8 ± 0.5 (+5.0%) | 23.9 ± 2.1 (+20.7%) |
| Adapter         | 1492.2 ± 1.0 (+3.0%) | 366.3 ± 0.5 (+8.4%) | 25.8 ± 2.2 (+30.3%) |

Table 1: Infernece latency of a single forward pass in GPT-2 medium measured in milliseconds, averaged over 100 trials. We use an NVIDIA Quadro RTX8000. ' | Θ | ' denotes the number of trainable parameters in adapter layers. Adapter L and Adapter H are two variants of adapter tuning, which we describe in Section 5.1. The inference latency introduced by adapter layers can be significant in an online, short-sequence-length scenario. See the full study in Appendix B.

## 4 OUR METHOD

We describe the simple design of LoRA and its practical benefits. The principles outlined here apply to any dense layers in deep learning models, though we only focus on certain weights in Transformer language models in our experiments as the motivating use case.

## 4.1 LOW-RANK-PARAMETRIZED UPDATE MATRICES

A neural network contains many dense layers which perform matrix multiplication. The weight matrices in these layers typically have full-rank. When adapting to a specific task, Aghajanyan et al. (2020) shows that the pre-trained language models have a low 'instrisic dimension' and can still learn efficiently despite a random projection to a smaller subspace. Inspired by this, we hypothesize the updates to the weights also have a low 'intrinsic rank' during adaptation. For a pre-trained weight matrix W 0 ∈ R d × k , we constrain its update by representing the latter with a low-rank decomposition W 0 +∆ W = W 0 + BA , where B ∈ R d × r , A ∈ R r × k , and the rank r ≪ min( d, k ) . During training, W 0 is frozen and does not receive gradient updates, while A and B contain trainable parameters. Note both W 0 and ∆ W = BA are multiplied with the same input, and their respective output vectors are summed coordinate-wise. For h = W 0 x , our modified forward pass yields:

<!-- formula-not-decoded -->

We illustrate our reparametrization in Figure 1. We use a random Gaussian initialization for A and zero for B , so ∆ W = BA is zero at the beginning of training. We then scale ∆ Wx by α r , where α is a constant in r . When optimizing with Adam, tuning α is roughly the same as tuning the learning rate if we scale the initialization appropriately. As a result, we simply set α to the first r we try and do not tune it. This scaling helps to reduce the need to retune hyperparameters when we vary r (Yang &amp; Hu, 2021).

A Generalization of Full Fine-tuning. A more general form of fine-tuning allows the training of a subset of the pre-trained parameters. LoRA takes a step further and does not require the accumulated gradient update to weight matrices to have full-rank during adaptation. This means that when applying LoRA to all weight matrices and training all biases 2 , we roughly recover the expressiveness of full fine-tuning by setting the LoRA rank r to the rank of the pre-trained weight matrices. In other words, as we increase the number of trainable parameters 3 , training LoRA roughly converges to training the original model, while adapter-based methods converges to an MLP and prefix-based methods to a model that cannot take long input sequences.

No Additional Inference Latency. When deployed in production, we can explicitly compute and store W = W 0 + BA and perform inference as usual. Note that both W 0 and BA are in R d × k . When we need to switch to another downstream task, we can recover W 0 by subtracting BA and then adding a different B ′ A ′ , a quick operation with very little memory overhead. Critically, this guarantees that we do not introduce any additional latency during inference compared to a fine-tuned model by construction.

2 They represent a negligible number of parameters compared to weights.

3 An inevitability when adapting to hard tasks.

## 4.2 APPLYING LORA TO TRANSFORMER

In principle, we can apply LoRA to any subset of weight matrices in a neural network to reduce the number of trainable parameters. In the Transformer architecture, there are four weight matrices in the self-attention module ( W q , W k , W v , W o ) and two in the MLP module. We treat W q (or W k , W v ) as a single matrix of dimension d model × d model , even though the output dimension is usually sliced into attention heads. We limit our study to only adapting the attention weights for downstream tasks and freeze the MLP modules (so they are not trained in downstream tasks) both for simplicity and parameter-efficiency.We further study the effect on adapting different types of attention weight matrices in a Transformer in Section 7.1. We leave the empirical investigation of adapting the MLP layers, LayerNorm layers, and biases to a future work.

Practical Benefits and Limitations. The most significant benefit comes from the reduction in memory and storage usage. For a large Transformer trained with Adam, we reduce that VRAM usage by up to 2 / 3 if r ≪ d model as we do not need to store the optimizer states for the frozen parameters. On GPT-3 175B, we reduce the VRAM consumption during training from 1.2TB to 350GB. With r = 4 and only the query and value projection matrices being adapted, the checkpoint size is reduced by roughly 10,000 × (from 350GB to 35MB) 4 . This allows us to train with significantly fewer GPUs and avoid I/O bottlenecks. Another benefit is that we can switch between tasks while deployed at a much lower cost by only swapping the LoRA weights as opposed to all the parameters. This allows for the creation of many customized models that can be swapped in and out on the fly on machines that store the pre-trained weights in VRAM. We also observe a 25% speedup during training on GPT-3 175B compared to full fine-tuning 5 as we do not need to calculate the gradient for the vast majority of the parameters.

LoRA also has its limitations. For example, it is not straightforward to batch inputs to different tasks with different A and B in a single forward pass, if one chooses to absorb A and B into W to eliminate additional inference latency. Though it is possible to not merge the weights and dynamically choose the LoRA modules to use for samples in a batch for scenarios where latency is not critical.

## 5 EMPIRICAL EXPERIMENTS

We evaluate the downstream task performance of LoRA on RoBERTa (Liu et al., 2019), DeBERTa (He et al., 2021), and GPT-2 (Radford et al., b), before scaling up to GPT-3 175B (Brown et al., 2020). Our experiments cover a wide range of tasks, from natural language understanding (NLU) to generation (NLG). Specifically, we evaluate on the GLUE (Wang et al., 2019) benchmark for RoBERTa and DeBERTa. We follow the setup of Li &amp; Liang (2021) on GPT-2 for a direct comparison and add WikiSQL (Zhong et al., 2017) (NL to SQL queries) and SAMSum (Gliwa et al., 2019) (conversation summarization) for large-scale experiments on GPT-3. See Appendix C for more details on the datasets we use. We use NVIDIA Tesla V100 for all experiments.

## 5.1 BASELINES

To compare with other baselines broadly, we replicate the setups used by prior work and reuse their reported numbers whenever possible. This, however, means that some baselines might only appear in certain experiments.

Fine-Tuning (FT) is a common approach for adaptation. During fine-tuning, the model is initialized to the pre-trained weights and biases, and all model parameters undergo gradient updates.A simple variant is to update only some layers while freezing others. We include one such baseline reported in prior work (Li &amp; Liang, 2021) on GPT-2, which adapts just the last two layers ( FT Top2 ).

4 We still need the 350GB model during deployment; however, storing 100 adapted models only requires 350GB + 35MB * 100 ≈ 354GB as opposed to 100 * 350GB ≈ 35TB.

5 For GPT-3 175B, the training throughput for full fine-tuning is 32.5 tokens/s per V100 GPU; with the same number of weight shards for model parallelism, the throughput is 43.1 tokens/s per V100 GPU for LoRA.

Table 2: RoBERTabase, RoBERTalarge, and DeBERTaXXL with different adaptation methods on the GLUEbenchmark. We report the overall (matched and mismatched) accuracy for MNLI, Matthew's correlation for CoLA, Pearson correlation for STS-B, and accuracy for other tasks. Higher is better for all metrics. * indicates numbers published in prior works. † indicates runs configured in a setup similar to Houlsby et al. (2019) for a fair comparison.

| Model &Method         | # Trainable Parameters   | MNLI      | SST-2     | MRPC       | CoLA       | QNLI      | QQP       | RTE        | STS-B      |   Avg. |
|-----------------------|--------------------------|-----------|-----------|------------|------------|-----------|-----------|------------|------------|--------|
| RoB base (FT)*        | 125.0M                   | 87.6      | 94.8      | 90.2       | 63.6       | 92.8      | 91.9      | 78.7       | 91.2       |   86.4 |
| RoB base (BitFit)*    | 0.1M                     | 84.7      | 93.7      | 92.7       | 62.0       | 91.8      | 84.0      | 81.5       | 90.8       |   85.2 |
| RoB base (Adpt D )*   | 0.3M                     | 87.1 ± .0 | 94.2 ± .1 | 88.5 ± 1.1 | 60.8 ± .4  | 93.1 ± .1 | 90.2 ± .0 | 71.5 ± 2.7 | 89.7 ± .3  |   84.4 |
| RoB base (Adpt D )*   | 0.9M                     | 87.3 ± .1 | 94.7 ± .3 | 88.4 ± .1  | 62.6 ± .9  | 93.0 ± .2 | 90.6 ± .0 | 75.9 ± 2.2 | 90.3 ± .1  |   85.4 |
| RoB base (LoRA)       | 0.3M                     | 87.5 ± .3 | 95.1 ± .2 | 89.7 ± .7  | 63.4 ± 1.2 | 93.3 ± .3 | 90.8 ± .1 | 86.6 ± .7  | 91.5 ± .2  |   87.2 |
| RoB large (FT)*       | 355.0M                   | 90.2      | 96.4      | 90.9       | 68.0       | 94.7      | 92.2      | 86.6       | 92.4       |   88.9 |
| RoB large (LoRA)      | 0.8M                     | 90.6 ± .2 | 96.2 ± .5 | 90.9 ± 1.2 | 68.2 ± 1.9 | 94.9 ± .3 | 91.6 ± .1 | 87.4 ± 2.5 | 92.6 ± .2  |   89.0 |
| RoB large (Adpt P ) † | 3.0M                     | 90.2 ± .3 | 96.1 ± .3 | 90.2 ± .7  | 68.3 ± 1.0 | 94.8 ± .2 | 91.9 ± .1 | 83.8 ± 2.9 | 92.1 ± .7  |   88.4 |
| RoB large (Adpt P ) † | 0.8M                     | 90.5 ± .3 | 96.6 ± .2 | 89.7 ± 1.2 | 67.8 ± 2.5 | 94.8 ± .3 | 91.7 ± .2 | 80.1 ± 2.9 | 91.9 ± .4  |   87.9 |
| RoB large (Adpt H ) † | 6.0M                     | 89.9 ± .5 | 96.2 ± .3 | 88.7 ± 2.9 | 66.5 ± 4.4 | 94.7 ± .2 | 92.1 ± .1 | 83.4 ± 1.1 | 91.0 ± 1.7 |   87.8 |
| RoB large (Adpt H ) † | 0.8M                     | 90.3 ± .3 | 96.3 ± .5 | 87.7 ± 1.7 | 66.3 ± 2.0 | 94.7 ± .2 | 91.5 ± .1 | 72.9 ± 2.9 | 91.5 ± .5  |   86.4 |
| RoB large (LoRA) †    | 0.8M                     | 90.6 ± .2 | 96.2 ± .5 | 90.2 ± 1.0 | 68.2 ± 1.9 | 94.8 ± .3 | 91.6 ± .2 | 85.2 ± 1.1 | 92.3 ± .5  |   88.6 |
| DeB XXL (FT)*         | 1500.0M                  | 91.8      | 97.2      | 92.0       | 72.0       | 96.0      | 92.7      | 93.9       | 92.9       |   91.1 |
| DeB XXL (LoRA)        | 4.7M                     | 91.9 ± .2 | 96.9 ± .2 | 92.6 ± .6  | 72.4 ± 1.1 | 96.0 ± .1 | 92.9 ± .1 | 94.9 ± .4  | 93.0 ± .2  |   91.3 |

Bias-only or BitFit is a baseline where we only train the bias vectors while freezing everything else. Contemporarily, this baseline has also been studied by BitFit (Zaken et al., 2021).

Prefix-embedding tuning (PreEmbed) inserts special tokens among the input tokens. These special tokens have trainable word embeddings and are generally not in the model's vocabulary. Where to place such tokens can have an impact on performance. We focus on 'prefixing', which prepends such tokens to the prompt, and 'infixing', which appends to the prompt; both are discussed in Li &amp; Liang (2021). We use l p (resp. l i ) denote the number of prefix (resp. infix) tokens. The number of trainable parameters is | Θ | = d model × ( l p + l i ) .

Prefix-layer tuning (PreLayer) is an extension to prefix-embedding tuning. Instead of just learning the word embeddings (or equivalently, the activations after the embedding layer) for some special tokens, we learn the activations after every Transformer layer. The activations computed from previous layers are simply replaced by trainable ones. The resulting number of trainable parameters is | Θ | = L × d model × ( l p + l i ) , where L is the number of Transformer layers.

Adapter tuning as proposed in Houlsby et al. (2019) inserts adapter layers between the selfattention module (and the MLP module) and the subsequent residual connection. There are two fully connected layers with biases in an adapter layer with a nonlinearity in between. We call this original design Adapter H . Recently, Lin et al. (2020) proposed a more efficient design with the adapter layer applied only after the MLP module and after a LayerNorm. We call it Adapter L . This is very similar to another deign proposed in Pfeiffer et al. (2021), which we call Adapter P . We also include another baseline call AdapterDrop (R¨ uckl´ e et al., 2020) which drops some adapter layers for greater efficiency ( Adapter D ). We cite numbers from prior works whenever possible to maximize the number of baselines we compare with; they are in rows with an asterisk (*) in the first column. In all cases, we have | Θ | = ˆ L Adpt × (2 × d model × r + r + d model )+2 × ˆ L LN × d model where ˆ L Adpt is the number of adapter layers and ˆ L LN the number of trainable LayerNorms (e.g., in Adapter L ).

LoRA adds trainable pairs of rank decomposition matrices in parallel to existing weight matrices. As mentioned in Section 4.2, we only apply LoRA to W q and W v in most experiments for simplicity. The number of trainable parameters is determined by the rank r and the shape of the original weights: | Θ | = 2 × ˆ L LoRA × d model × r , where ˆ L LoRA is the number of weight matrices we apply LoRA to.

| Model &Method        | # Trainable Parameters   | E2E NLG Challenge   | E2E NLG Challenge   | E2E NLG Challenge   | E2E NLG Challenge   | E2E NLG Challenge   |
|----------------------|--------------------------|---------------------|---------------------|---------------------|---------------------|---------------------|
|                      |                          | BLEU                | NIST                | MET                 | ROUGE-L             | CIDEr               |
| GPT-2 M(FT)*         | 354.92M                  | 68.2                | 8.62                | 46.2                | 71.0                | 2.47                |
| GPT-2 M(Adapter L )* | 0.37M                    | 66.3                | 8.41                | 45.0                | 69.8                | 2.40                |
| GPT-2 M(Adapter L )* | 11.09M                   | 68.9                | 8.71                | 46.1                | 71.3                | 2.47                |
| GPT-2 M(Adapter H )  | 11.09M                   | 67.3 ± .6           | 8.50 ± .07          | 46.0 ± .2           | 70.7 ± .2           | 2.44 ± .01          |
| GPT-2 M(FT Top2 )*   | 25.19M                   | 68.1                | 8.59                | 46.0                | 70.8                | 2.41                |
| GPT-2 M(PreLayer)*   | 0.35M                    | 69.7                | 8.81                | 46.1                | 71.4                | 2.49                |
| GPT-2 M(LoRA)        | 0.35M                    | 70.4 ± .1           | 8.85 ± .02          | 46.8 ± .2           | 71.8 ± .1           | 2.53 ± .02          |
| GPT-2 L (FT)*        | 774.03M                  | 68.5                | 8.78                | 46.0                | 69.9                | 2.45                |
| GPT-2 L (Adapter L ) | 0.88M                    | 69.1 ± .1           | 8.68 ± .03          | 46.3 ± .0           | 71.4 ± .2           | 2.49 ± .0           |
| GPT-2 L (Adapter L ) | 23.00M                   | 68.9 ± .3           | 8.70 ± .04          | 46.1 ± .1           | 71.3 ± .2           | 2.45 ± .02          |
| GPT-2 L (PreLayer)*  | 0.77M                    | 70.3                | 8.85                | 46.2                | 71.7                | 2.47                |
| GPT-2 L (LoRA)       | 0.77M                    | 70.4 ± .1           | 8.89 ± .02          | 46.8 ± .2           | 72.0 ± .2           | 2.47 ± .02          |

Table 3: GPT-2 medium (M) and large (L) with different adaptation methods on the E2E NLG Challenge. For all metrics, higher is better. LoRA outperforms several baselines with comparable or fewer trainable parameters. Confidence intervals are shown for experiments we ran. * indicates numbers published in prior works.

## 5.2 ROBERTA BASE/LARGE

RoBERTa (Liu et al., 2019) optimized the pre-training recipe originally proposed in BERT (Devlin et al., 2019a) and boosted the latter's task performance without introducing many more trainable parameters. While RoBERTa has been overtaken by much larger models on NLP leaderboards such as the GLUE benchmark (Wang et al., 2019) in recent years, it remains a competitive and popular pre-trained model for its size among practitioners. We take the pre-trained RoBERTa base (125M) and RoBERTa large (355M) from the HuggingFace Transformers library (Wolf et al., 2020) and evaluate the performance of different efficient adaptation approaches on tasks from the GLUE benchmark. We also replicate Houlsby et al. (2019) and Pfeiffer et al. (2021) according to their setup. To ensure a fair comparison, we make two crucial changes to how we evaluate LoRA when comparing with adapters. First, we use the same batch size for all tasks and use a sequence length of 128 to match the adapter baselines. Second, we initialize the model to the pre-trained model for MRPC, RTE, and STS-B, not a model already adapted to MNLI like the fine-tuning baseline. Runs following this more restricted setup from Houlsby et al. (2019) are labeled with † . The result is presented in Table 2 (Top Three Sections). See Section D.1 for details on the hyperparameters used.

## 5.3 DEBERTA XXL

DeBERTa (He et al., 2021) is a more recent variant of BERT that is trained on a much larger scale and performs very competitively on benchmarks such as GLUE (Wang et al., 2019) and SuperGLUE (Wang et al., 2020). We evaluate if LoRA can still match the performance of a fully fine-tuned DeBERTa XXL (1.5B) on GLUE. The result is presented in Table 2 (Bottom Section). See Section D.2 for details on the hyperparameters used.

## 5.4 GPT-2 MEDIUM/LARGE

Having shown that LoRA can be a competitive alternative to full fine-tuning on NLU, we hope to answer if LoRA still prevails on NLG models, such as GPT-2 medium and large (Radford et al., b). We keep our setup as close as possible to Li &amp; Liang (2021) for a direct comparison. Due to space constraint, we only present our result on E2E NLG Challenge (Table 3) in this section. See Section F.1 for results on WebNLG (Gardent et al., 2017) and DART (Nan et al., 2020). We include a list of the hyperparameters used in Section D.3.

Table 4: Performance of different adaptation methods on GPT-3 175B. We report the logical form validation accuracy on WikiSQL, validation accuracy on MultiNLI-matched, and Rouge-1/2/L on SAMSum. LoRA performs better than prior approaches, including full fine-tuning. The results on WikiSQL have a fluctuation around ± 0 . 5% , MNLI-m around ± 0 . 1% , and SAMSum around ± 0 . 2 / ± 0 . 2 / ± 0 . 1 for the three metrics.

| Model&Method       | # Trainable Parameters   |   WikiSQL Acc. (%) |   MNLI-m Acc. (%) | SAMSum R1/R2/RL   |
|--------------------|--------------------------|--------------------|-------------------|-------------------|
| GPT-3 (FT)         | 175,255.8M               |               73.8 |              89.5 | 52.0/28.0/44.5    |
| GPT-3 (BitFit)     | 14.2M                    |               71.3 |              91.0 | 51.3/27.4/43.5    |
| GPT-3 (PreEmbed)   | 3.2M                     |               63.1 |              88.6 | 48.3/24.2/40.5    |
| GPT-3 (PreLayer)   | 20.2M                    |               70.1 |              89.5 | 50.8/27.3/43.5    |
| GPT-3 (Adapter H ) | 7.1M                     |               71.9 |              89.8 | 53.0/28.9/44.8    |
| GPT-3 (Adapter H ) | 40.1M                    |               73.2 |              91.5 | 53.2/29.0/45.1    |
| GPT-3 (LoRA)       | 4.7M                     |               73.4 |              91.7 | 53.8/29.8/45.9    |
| GPT-3 (LoRA)       | 37.7M                    |               74.0 |              91.6 | 53.4/29.2/45.1    |

## 5.5 SCALING UP TO GPT-3 175B

As a final stress test for LoRA, we scale up to GPT-3 with 175 billion parameters. Due to the high training cost, we only report the typical standard deviation for a given task over random seeds, as opposed to providing one for every entry. See Section D.4 for details on the hyperparameters used.

As shown in Table 4, LoRA matches or exceeds the fine-tuning baseline on all three datasets. Note that not all methods benefit monotonically from having more trainable parameters, as shown in Figure 2. We observe a significant performance drop when we use more than 256 special tokens for prefix-embedding tuning or more than 32 special tokens for prefix-layer tuning. This corroborates similar observations in Li &amp; Liang (2021). While a thorough investigation into this phenomenon is out-of-scope for this work, we suspect that having more special tokens causes the input distribution to shift further away from the pre-training data distribution. Separately, we investigate the performance of different adaptation approaches in the low-data regime in Section F.3.

Figure 2: GPT-3 175B validation accuracy vs. number of trainable parameters of several adaptation methods on WikiSQL and MNLI-matched. LoRA exhibits better scalability and task performance. See Section F.2 for more details on the plotted data points.

<!-- image -->

## 6 RELATED WORKS

Transformer Language Models. Transformer (Vaswani et al., 2017) is a sequence-to-sequence architecture that makes heavy use of self-attention. Radford et al. (a) applied it to autoregressive language modeling by using a stack of Transformer decoders. Since then, Transformer-based language models have dominated NLP, achieving the state-of-the-art in many tasks. A new paradigm emerged with BERT (Devlin et al., 2019b) and GPT-2 (Radford et al., b) - both are large Transformer language models trained on a large amount of text - where fine-tuning on task-specific data after pretraining on general domain data provides a significant performance gain compared to training on task-specific data directly. Training larger Transformers generally results in better performance and remains an active research direction. GPT-3 (Brown et al., 2020) is the largest single Transformer language model trained to-date with 175B parameters.

Prompt Engineering and Fine-Tuning. While GPT-3 175B can adapt its behavior with just a few additional training examples, the result depends heavily on the input prompt (Brown et al., 2020). This necessitates an empirical art of composing and formatting the prompt to maximize a model's performance on a desired task, which is known as prompt engineering or prompt hacking. Fine-tuning retrains a model pre-trained on general domains to a specific task Devlin et al. (2019b); Radford et al. (a). Variants of it include learning just a subset of the parameters Devlin et al. (2019b); Collobert &amp; Weston (2008), yet practitioners often retrain all of them to maximize the downstream performance. However, the enormity of GPT-3 175B makes it challenging to perform fine-tuning in the usual way due to the large checkpoint it produces and the high hardware barrier to entry since it has the same memory footprint as pre-training.

Parameter-Efficient Adaptation. Many have proposed inserting adapter layers between existing layers in a neural network (Houlsby et al., 2019; Rebuffi et al., 2017; Lin et al., 2020). Our method uses a similar bottleneck structure to impose a low-rank constraint on the weight updates. The key functional difference is that our learned weights can be merged with the main weights during inference, thus not introducing any latency, which is not the case for the adapter layers (Section 3). A comtenporary extension of adapter is COMPACTER (Mahabadi et al., 2021), which essentially parametrizes the adapter layers using Kronecker products with some predetermined weight sharing scheme. Similarly, combining LoRA with other tensor product-based methods could potentially improve its parameter efficiency, which we leave to future work. More recently, many proposed optimizing the input word embeddings in lieu of fine-tuning, akin to a continuous and differentiable generalization of prompt engineering (Li &amp; Liang, 2021; Lester et al., 2021; Hambardzumyan et al., 2020; Liu et al., 2021). We include comparisons with Li &amp; Liang (2021) in our experiment section. However, this line of works can only scale up by using more special tokens in the prompt, which take up available sequence length for task tokens when positional embeddings are learned.

Low-Rank Structures in Deep Learning. Low-rank structure is very common in machine learning. A lot of machine learning problems have certain intrinsic low-rank structure (Li et al., 2016; Cai et al., 2010; Li et al., 2018b; Grasedyck et al., 2013). Moreover, it is known that for many deep learning tasks, especially those with a heavily over-parametrized neural network, the learned neural network will enjoy low-rank properties after training (Oymak et al., 2019). Some prior works even explicitly impose the low-rank constraint when training the original neural network (Sainath et al., 2013; Povey et al., 2018; Zhang et al., 2014; Jaderberg et al., 2014; Zhao et al., 2016; Khodak et al., 2021; Denil et al., 2014); however, to the best of our knowledge, none of these works considers low-rank update to a frozen model for adaptation to downstream tasks . In theory literature, it is known that neural networks outperform other classical learning methods, including the corresponding (finite-width) neural tangent kernels (Allen-Zhu et al., 2019; Li &amp; Liang, 2018) when the underlying concept class has certain low-rank structure (Ghorbani et al., 2020; Allen-Zhu &amp; Li, 2019; Allen-Zhu &amp; Li, 2020a). Another theoretical result in Allen-Zhu &amp; Li (2020b) suggests that low-rank adaptations can be useful for adversarial training. In sum, we believe that our proposed low-rank adaptation update is well-motivated by the literature.

## 7 UNDERSTANDING THE LOW-RANK UPDATES

Given the empirical advantage of LoRA, we hope to further explain the properties of the low-rank adaptation learned from downstream tasks. Note that the low-rank structure not only lowers the hardware barrier to entry which allows us to run multiple experiments in parallel, but also gives better interpretability of how the update weights are correlated with the pre-trained weights. We focus our study on GPT-3 175B, where we achieved the largest reduction of trainable parameters (up to 10,000 × ) without adversely affecting task performances.

Weperform a sequence of empirical studies to answer the following questions: 1) Given a parameter budget constraint, which subset of weight matrices in a pre-trained Transformer should we adapt to maximize downstream performance? 2) Is the 'optimal' adaptation matrix ∆ W really rankdeficient ? If so, what is a good rank to use in practice? 3) What is the connection between ∆ W and W ? Does ∆ W highly correlate with W ? How large is ∆ W comparing to W ?

We believe that our answers to question (2) and (3) shed light on the fundamental principles of using pre-trained language models for downstream tasks, which is a critical topic in NLP.

## 7.1 WHICH WEIGHT MATRICES IN TRANSFORMER SHOULD WE APPLY LORA TO?

Given a limited parameter budget, which types of weights should we adapt with LoRA to obtain the best performance on downstream tasks? As mentioned in Section 4.2, we only consider weight matrices in the self-attention module. We set a parameter budget of 18M (roughly 35MB if stored in FP16) on GPT-3 175B, which corresponds to r = 8 if we adapt one type of attention weights or r = 4 if we adapt two types, for all 96 layers. The result is presented in Table 5.

|                       | # of Trainable Parameters = 18M   | # of Trainable Parameters = 18M   | # of Trainable Parameters = 18M   | # of Trainable Parameters = 18M   | # of Trainable Parameters = 18M   | # of Trainable Parameters = 18M   | # of Trainable Parameters = 18M   |
|-----------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|-----------------------------------|
| Weight Type Rank r    | W q 8                             | W k 8                             | W v 8                             | W o 8                             | W q ,W k 4                        | W q ,W v 4                        | W q ,W k ,W v ,W o 2              |
| WikiSQL ( ± 0 . 5 %)  | 70.4                              | 70.0                              | 73.0                              | 73.2                              | 71.4                              | 73.7                              | 73.7                              |
| MultiNLI ( ± 0 . 1 %) | 91.0                              | 90.8                              | 91.0                              | 91.3                              | 91.3                              | 91.3                              | 91.7                              |

Table 5: Validation accuracy on WikiSQL and MultiNLI after applying LoRA to different types of attention weights in GPT-3, given the same number of trainable parameters. Adapting both W q and W v gives the best performance overall. We find the standard deviation across random seeds to be consistent for a given dataset, which we report in the first column.

Note that putting all the parameters in ∆ W q or ∆ W k results in significantly lower performance, while adapting both W q and W v yields the best result. This suggests that even a rank of four captures enough information in ∆ W such that it is preferable to adapt more weight matrices than adapting a single type of weights with a larger rank.

## 7.2 WHAT IS THE OPTIMAL RANK r FOR LORA?

We turn our attention to the effect of rank r on model performance. We adapt { W q , W v } , { W q , W k , W v , W c } , and just W q for a comparison.

|                       | Weight Type        |   r = 1 |   r = 2 |   r = 4 |   r = |   8 r = 64 |
|-----------------------|--------------------|---------|---------|---------|-------|------------|
| WikiSQL( ± 0 . 5 %)   | W q W q ,W v       |    68.8 |    69.6 |    70.5 |  70.4 |       70.0 |
| WikiSQL( ± 0 . 5 %)   |                    |    73.4 |    73.3 |    73.7 |  73.8 |       73.5 |
| WikiSQL( ± 0 . 5 %)   | W q ,W k ,W v ,W o |    74.1 |    73.7 |    74.0 |  74.0 |       73.9 |
| MultiNLI ( ± 0 . 1 %) | W q                |    90.7 |    90.9 |    91.1 |  90.7 |       90.7 |
| MultiNLI ( ± 0 . 1 %) | W q ,W v           |    91.3 |    91.4 |    91.3 |  91.6 |       91.4 |
| MultiNLI ( ± 0 . 1 %) | W q ,W k ,W v ,W o |    91.2 |    91.7 |    91.7 |  91.5 |       91.4 |

Table 6: Validation accuracy on WikiSQL and MultiNLI with different rank r . To our surprise, a rank as small as one suffices for adapting both W q and W v on these datasets while training W q alone needs a larger r . We conduct a similar experiment on GPT-2 in Section H.2.

Table 6 shows that, surprisingly, LoRA already performs competitively with a very small r (more so for { W q , W v } than just W q ). This suggests the update matrix ∆ W could have a very small 'intrinsic rank'. 6 To further support this finding, we check the overlap of the subspaces learned by different choices of r and by different random seeds. We argue that increasing r does not cover a more meaningful subspace, which suggests that a low-rank adaptation matrix is sufficient.

6 However, we do not expect a small r to work for every task or dataset. Consider the following thought experiment: if the downstream task were in a different language than the one used for pre-training, retraining the entire model (similar to LoRA with r = d model ) could certainly outperform LoRA with a small r .

Subspace similarity between different r . Given A r =8 and A r =64 which are the learned adaptation matrices with rank r = 8 and 64 using the same pre-trained model , we perform singular value decomposition and obtain the right-singular unitary matrices U A r =8 and U A r =64 . 7 We hope to answer: how much of the subspace spanned by the top i singular vectors in U A r =8 (for 1 ≤ i ≤ 8 ) is contained in the subspace spanned by top j singular vectors of U A r =64 (for 1 ≤ j ≤ 64 )? We measure this quantity with a normalized subspace similarity based on the Grassmann distance (See Appendix G for a more formal discussion)

<!-- formula-not-decoded -->

where U i A r =8 represents the columns of U A r =8 corresponding to the topi singular vectors.

φ ( · ) has a range of [0 , 1] , where 1 represents a complete overlap of subspaces and 0 a complete separation. See Figure 3 for how φ changes as we vary i and j . We only look at the 48th layer (out of 96) due to space constraint, but the conclusion holds for other layers as well, as shown in Section H.1.

Figure 3: Subspace similarity between column vectors of A r =8 and A r =64 for both ∆ W q and ∆ W v . The third and the fourth figures zoom in on the lower-left triangle in the first two figures. The top directions in r = 8 are included in r = 64 , and vice versa.

<!-- image -->

We make an important observation from Figure 3.

Directions corresponding to the top singular vector overlap significantly between A r =8 and A r =64 , while others do not. Specifically, ∆ W v (resp. ∆ W q ) of A r =8 and ∆ W v (resp. ∆ W q ) of A r =64 share a subspace of dimension 1 with normalized similarity &gt; 0 . 5 , providing an explanation of why r = 1 performs quite well in our downstream tasks for GPT-3.

Since both A r =8 and A r =64 are learned using the same pre-trained model, Figure 3 indicates that the top singular-vector directions of A r =8 and A r =64 are the most useful, while other directions potentially contain mostly random noises accumulated during training. Hence, the adaptation matrix can indeed have a very low rank.

Subspace similarity between different random seeds. We further confirm this by plotting the normalized subspace similarity between two randomly seeded runs with r = 64 , shown in Figure 4. ∆ W q appears to have a higher 'intrinsic rank' than ∆ W v , since more common singular value directions are learned by both runs for ∆ W q , which is in line with our empirical observation in Table 6. As a comparison, we also plot two random Gaussian matrices, which do not share any common singular value directions with each other.

## 7.3 HOW DOES THE ADAPTATION MATRIX ∆ W COMPARE TO W ?

Wefurther investigate the relationship between ∆ W and W . In particular, does ∆ W highly correlate with W ? (Or mathematically, is ∆ W mostly contained in the top singular directions of W ?) Also, how 'large' is ∆ W comparing to its corresponding directions in W ? This can shed light on the underlying mechanism for adapting pre-trained language models.

7 Note that a similar analysis can be carried out with B and the left-singular unitary matrices - we stick with A for our experiments.

Figure 4: Left and Middle: Normalized subspace similarity between the column vectors of A r =64 from two random seeds, for both ∆ W q and ∆ W v in the 48-th layer. Right: the same heat-map between the column vectors of two random Gaussian matrices. See Section H.1 for other layers.

<!-- image -->

To answer these questions, we project W onto the r -dimensional subspace of ∆ W by computing U ⊤ WV ⊤ , with U / V being the left/right singular-vector matrix of ∆ W . Then, we compare the Frobenius norm between ‖ U ⊤ WV ⊤ ‖ F and ‖ W ‖ F . As a comparison, we also compute ‖ U ⊤ WV ⊤ ‖ F by replacing U, V with the top r singular vectors of W or a random matrix.

Table 7: The Frobenius norm of U ⊤ W q V ⊤ where U and V are the left/right top r singular vector directions of either (1) ∆ W q , (2) W q , or (3) a random matrix. The weight matrices are taken from the 48th layer of GPT-3.

|                                           | r = 4                                      | r = 4                                      | r = 4                                      | r = 64                                     | r = 64                                     | r = 64                                     |
|-------------------------------------------|--------------------------------------------|--------------------------------------------|--------------------------------------------|--------------------------------------------|--------------------------------------------|--------------------------------------------|
|                                           | ∆ W q                                      | W q                                        | Random                                     | ∆ W q                                      | W q                                        | Random                                     |
| &#124;&#124; U ⊤ W q V ⊤ &#124;&#124; F = | 0.32                                       | 21.67                                      | 0.02                                       | 1.90                                       | 37.71                                      | 0.33                                       |
| &#124;&#124; W q &#124;&#124; F = 61 . 95 | &#124;&#124; ∆ W q &#124;&#124; F = 6 . 91 | &#124;&#124; ∆ W q &#124;&#124; F = 6 . 91 | &#124;&#124; ∆ W q &#124;&#124; F = 6 . 91 | &#124;&#124; ∆ W q &#124;&#124; F = 3 . 57 | &#124;&#124; ∆ W q &#124;&#124; F = 3 . 57 | &#124;&#124; ∆ W q &#124;&#124; F = 3 . 57 |

We draw several conclusions from Table 7. First, ∆ W has a stronger correlation with W compared to a random matrix, indicating that ∆ W amplifies some features that are already in W . Second, instead of repeating the top singular directions of W , ∆ W only amplifies directions that are not emphasized in W . Third, the amplification factor is rather huge: 21 . 5 ≈ 6 . 91 / 0 . 32 for r = 4 . See Section H.4 for why r = 64 has a smaller amplification factor. We also provide a visualization in Section H.3 for how the correlation changes as we include more top singular directions from W q . This suggests that the low-rank adaptation matrix potentially amplifies the important features for specific downstream tasks that were learned but not emphasized in the general pre-training model .

## 8 CONCLUSION AND FUTURE WORK

Fine-tuning enormous language models is prohibitively expensive in terms of the hardware required and the storage/switching cost for hosting independent instances for different tasks. We propose LoRA, an efficient adaptation strategy that neither introduces inference latency nor reduces input sequence length while retaining high model quality. Importantly, it allows for quick task-switching when deployed as a service by sharing the vast majority of the model parameters. While we focused on Transformer language models, the proposed principles are generally applicable to any neural networks with dense layers.

There are many directions for future works. 1) LoRA can be combined with other efficient adaptation methods, potentially providing orthogonal improvement. 2) The mechanism behind fine-tuning or LoRA is far from clear - how are features learned during pre-training transformed to do well on downstream tasks? We believe that LoRA makes it more tractable to answer this than full fine-