## Language Models are Few-Shot Learners

| Tom B. Brown ∗              | Tom B. Brown ∗              | Benjamin Mann ∗ Nick        | Benjamin Mann ∗ Nick   | Melanie Subbiah ∗   | Melanie Subbiah ∗   |
|-----------------------------|-----------------------------|-----------------------------|------------------------|---------------------|---------------------|
| Jared Kaplan †              | Prafulla Dhariwal           | Prafulla Dhariwal           | Arvind Neelakantan     | Pranav Shyam        | Girish Sastry       |
| Amanda Askell               | Sandhini Agarwal            | Sandhini Agarwal            | Ariel Herbert-Voss     | Gretchen Krueger    | Tom Henighan        |
| Rewon Child                 | Aditya Ramesh               | Aditya Ramesh               | Daniel M. Ziegler      | Jeffrey Wu          | Clemens Winter      |
| Christopher Hesse           | Christopher Hesse           | Mark Chen                   | Eric Sigler            | Mateusz Litwin      | Scott Gray          |
| Benjamin Chess              | Benjamin Chess              | Benjamin Chess              | Jack Clark             | Christopher Berner  | Christopher Berner  |
| Sam McCandlish Alec Radford | Sam McCandlish Alec Radford | Sam McCandlish Alec Radford | Ilya Sutskever         | Dario               | Amodei              |
| OpenAI                      | OpenAI                      | OpenAI                      | OpenAI                 | OpenAI              | OpenAI              |

## Abstract

Recent work has demonstrated substantial gains on many NLP tasks and benchmarks by pre-training on a large corpus of text followed by fine-tuning on a specific task. While typically task-agnostic in architecture, this method still requires task-specific fine-tuning datasets of thousands or tens of thousands of examples. By contrast, humans can generally perform a new language task from only a few examples or from simple instructions - something which current NLP systems still largely struggle to do. Here we show that scaling up language models greatly improves task-agnostic, few-shot performance, sometimes even reaching competitiveness with prior state-of-the-art finetuning approaches. Specifically, we train GPT-3, an autoregressive language model with 175 billion parameters, 10x more than any previous non-sparse language model, and test its performance in the few-shot setting. For all tasks, GPT-3 is applied without any gradient updates or fine-tuning, with tasks and few-shot demonstrations specified purely via text interaction with the model. GPT-3 achieves strong performance on many NLP datasets, including translation, question-answering, and cloze tasks, as well as several tasks that require on-the-fly reasoning or domain adaptation, such as unscrambling words, using a novel word in a sentence, or performing 3-digit arithmetic. At the same time, we also identify some datasets where GPT-3's few-shot learning still struggles, as well as some datasets where GPT-3 faces methodological issues related to training on large web corpora. Finally, we find that GPT-3 can generate samples of news articles which human evaluators have difficulty distinguishing from articles written by humans. We discuss broader societal impacts of this finding and of GPT-3 in general.

∗ Equal contribution

† Johns Hopkins University, OpenAI

## Contents

| 1 Introduction   | 1 Introduction                                      | 1 Introduction                                       |   3 |
|------------------|-----------------------------------------------------|------------------------------------------------------|-----|
| 2                | Approach                                            | Approach                                             |   6 |
|                  | 2.1                                                 | Model and Architectures . . . . . . . . . . . . .    |   8 |
|                  | 2.2                                                 | Training Dataset . . . . . . . . . . . . . . . . . . |   8 |
|                  | 2.3                                                 | Training Process . . . . . . . . . . . . . . . . .   |   9 |
|                  | 2.4                                                 | Evaluation . . . . . . . . . . . . . . . . . . . . . |  10 |
| 3                | Results                                             | Results                                              |  10 |
|                  | 3.1                                                 | Language Modeling, Cloze, and Completion Tasks       |  11 |
|                  | 3.2                                                 | Closed Book Question Answering . . . . . . . .       |  13 |
|                  | 3.3                                                 | Translation . . . . . . . . . . . . . . . . . . . .  |  14 |
|                  | 3.4                                                 | Winograd-Style Tasks . . . . . . . . . . . . . . .   |  16 |
|                  | 3.5                                                 | Common Sense Reasoning . . . . . . . . . . . .       |  17 |
|                  | 3.6                                                 | Reading Comprehension . . . . . . . . . . . . .      |  18 |
|                  | 3.7                                                 | SuperGLUE . . . . . . . . . . . . . . . . . . . .    |  18 |
|                  | 3.8                                                 | NLI . . . . . . . . . . . . . . . . . . . . . . . .  |  20 |
|                  | 3.9                                                 | Synthetic and Qualitative Tasks . . . . . . . . . .  |  21 |
| 4                | Measuring and Preventing Memorization Of Benchmarks | Measuring and Preventing Memorization Of Benchmarks  |  29 |
| 5                | Limitations                                         | Limitations                                          |  33 |
| 6                | Broader Impacts                                     | Broader Impacts                                      |  34 |
|                  | 6.1                                                 | Misuse of Language Models . . . . . . . . . . .      |  35 |
|                  | 6.2                                                 | Fairness, Bias, and Representation . . . . . . . .   |  36 |
|                  | 6.3                                                 | Energy Usage . . . . . . . . . . . . . . . . . . .   |  39 |
| 7                | Related Work                                        | Related Work                                         |  39 |
| 8                | Conclusion                                          | Conclusion                                           |  40 |
| A                | Details of Common Crawl Filtering                   | Details of Common Crawl Filtering                    |  43 |
| B                | Details of Model Training                           | Details of Model Training                            |  43 |
| C                | Details of Test Set Contamination Studies           | Details of Test Set Contamination Studies            |  43 |
| D                | Total Compute Used to Train Language Models         | Total Compute Used to Train Language Models          |  46 |
| E                | Human Quality Assessment of Synthetic News Articles | Human Quality Assessment of Synthetic News Articles  |  46 |
| F                | Additional Samples from GPT-3                       | Additional Samples from GPT-3                        |  48 |
| G                | Details of Task Phrasing and Specifications         | Details of Task Phrasing and Specifications          |  50 |
| H                | Results on All Tasks for All Model Sizes            | Results on All Tasks for All Model Sizes             |  63 |

## 1 Introduction

Recent years have featured a trend towards pre-trained language representations in NLP systems, applied in increasingly flexible and task-agnostic ways for downstream transfer. First, single-layer representations were learned using word vectors [MCCD13, PSM14] and fed to task-specific architectures, then RNNs with multiple layers of representations and contextual state were used to form stronger representations [DL15, MBXS17, PNZtY18] (though still applied to task-specific architectures), and more recently pre-trained recurrent or transformer language models [VSP + 17] have been directly fine-tuned, entirely removing the need for task-specific architectures [RNSS18, DCLT18, HR18].

This last paradigm has led to substantial progress on many challenging NLP tasks such as reading comprehension, question answering, textual entailment, and many others, and has continued to advance based on new architectures and algorithms [RSR + 19, LOG + 19, YDY + 19, LCG + 19]. However, a major limitation to this approach is that while the architecture is task-agnostic, there is still a need for task-specific datasets and task-specific fine-tuning: to achieve strong performance on a desired task typically requires fine-tuning on a dataset of thousands to hundreds of thousands of examples specific to that task. Removing this limitation would be desirable, for several reasons.

First, from a practical perspective, the need for a large dataset of labeled examples for every new task limits the applicability of language models. There exists a very wide range of possible useful language tasks, encompassing anything from correcting grammar, to generating examples of an abstract concept, to critiquing a short story. For many of these tasks it is difficult to collect a large supervised training dataset, especially when the process must be repeated for every new task.

Second, the potential to exploit spurious correlations in training data fundamentally grows with the expressiveness of the model and the narrowness of the training distribution. This can create problems for the pre-training plus fine-tuning paradigm, where models are designed to be large to absorb information during pre-training, but are then fine-tuned on very narrow task distributions. For instance [HLW + 20] observe that larger models do not necessarily generalize better out-of-distribution. There is evidence that suggests that the generalization achieved under this paradigm can be poor because the model is overly specific to the training distribution and does not generalize well outside it [YdC + 19, MPL19]. Thus, the performance of fine-tuned models on specific benchmarks, even when it is nominally at human-level, may exaggerate actual performance on the underlying task [GSL + 18, NK19].

Third, humans do not require large supervised datasets to learn most language tasks - a brief directive in natural language (e.g. 'please tell me if this sentence describes something happy or something sad') or at most a tiny number of demonstrations (e.g. 'here are two examples of people acting brave; please give a third example of bravery') is often sufficient to enable a human to perform a new task to at least a reasonable degree of competence. Aside from pointing to a conceptual limitation in our current NLP techniques, this adaptability has practical advantages - it allows humans to seamlessly mix together or switch between many tasks and skills, for example performing addition during a lengthy dialogue. To be broadly useful, we would someday like our NLP systems to have this same fluidity and generality.

Figure 1.1: Language model meta-learning. During unsupervised pre-training, a language model develops a broad set of skills and pattern recognition abilities. It then uses these abilities at inference time to rapidly adapt to or recognize the desired task. We use the term 'in-context learning' to describe the inner loop of this process, which occurs within the forward-pass upon each sequence. The sequences in this diagram are not intended to be representative of the data a model would see during pre-training, but are intended to show that there are sometimes repeated sub-tasks embedded within a single sequence.

<!-- image -->

Figure 1.2: Larger models make increasingly efficient use of in-context information. Weshow in-context learning performance on a simple task requiring the model to remove random symbols from a word, both with and without a natural language task description (see Sec. 3.9.2). The steeper 'in-context learning curves' for large models demonstrate improved ability to learn a task from contextual information. We see qualitatively similar behavior across a wide range of tasks.

<!-- image -->

One potential route towards addressing these issues is meta-learning 1 - which in the context of language models means the model develops a broad set of skills and pattern recognition abilities at training time, and then uses those abilities at inference time to rapidly adapt to or recognize the desired task (illustrated in Figure 1.1). Recent work [RWC + 19] attempts to do this via what we call 'in-context learning', using the text input of a pretrained language model as a form of task specification: the model is conditioned on a natural language instruction and/or a few demonstrations of the task and is then expected to complete further instances of the task simply by predicting what comes next.

While it has shown some initial promise, this approach still achieves results far inferior to fine-tuning - for example [RWC + 19] achieves only 4% on Natural Questions, and even its 55 F1 CoQa result is now more than 35 points behind the state of the art. Meta-learning clearly requires substantial improvement in order to be viable as a practical method of solving language tasks.

Another recent trend in language modeling may offer a way forward. In recent years the capacity of transformer language models has increased substantially, from 100 million parameters [RNSS18], to 300 million parameters [DCLT18], to 1.5 billion parameters [RWC + 19], to 8 billion parameters [SPP + 19], 11 billion parameters [RSR + 19], and finally 17 billion parameters [Tur20]. Each increase has brought improvements in text synthesis and/or downstream NLP tasks, and there is evidence suggesting that log loss, which correlates well with many downstream tasks, follows a smooth trend of improvement with scale [KMH + 20]. Since in-context learning involves absorbing many skills and tasks within the parameters of the model, it is plausible that in-context learning abilities might show similarly strong gains with scale.

1 In the context of language models this has sometimes been called 'zero-shot transfer', but this term is potentially ambiguous: the method is 'zero-shot' in the sense that no gradient updates are performed, but it often involves providing inference-time demonstrations to the model, so is not truly learning from zero examples. To avoid this confusion, we use the term 'meta-learning' to capture the inner-loop / outer-loop structure of the general method, and the term 'in context-learning' to refer to the inner loop of meta-learning. We further specialize the description to 'zero-shot', 'one-shot', or 'few-shot' depending on how many demonstrations are provided at inference time. These terms are intended to remain agnostic on the question of whether the model learns new tasks from scratch at inference time or simply recognizes patterns seen during training - this is an important issue which we discuss later in the paper, but 'meta-learning' is intended to encompass both possibilities, and simply describes the inner-outer loop structure.

Figure 1.3: Aggregate performance for all 42 accuracy-denominated benchmarks While zero-shot performance improves steadily with model size, few-shot performance increases more rapidly, demonstrating that larger models are more proficient at in-context learning. See Figure 3.8 for a more detailed analysis on SuperGLUE, a standard NLP benchmark suite.

<!-- image -->

In this paper, we test this hypothesis by training a 175 billion parameter autoregressive language model, which we call GPT-3, and measuring its in-context learning abilities. Specifically, we evaluate GPT-3 on over two dozen NLP datasets, as well as several novel tasks designed to test rapid adaptation to tasks unlikely to be directly contained in the training set. For each task, we evaluate GPT-3 under 3 conditions: (a) 'few-shot learning', or in-context learning where we allow as many demonstrations as will fit into the model's context window (typically 10 to 100), (b) 'one-shot learning', where we allow only one demonstration, and (c) 'zero-shot' learning, where no demonstrations are allowed and only an instruction in natural language is given to the model. GPT-3 could also in principle be evaluated in the traditional fine-tuning setting, but we leave this to future work.

Figure 1.2 illustrates the conditions we study, and shows few-shot learning of a simple task requiring the model to remove extraneous symbols from a word. Model performance improves with the addition of a natural language task description, and with the number of examples in the model's context, K . Few-shot learning also improves dramatically with model size. Though the results in this case are particularly striking, the general trends with both model size and number of examples in-context hold for most tasks we study. We emphasize that these 'learning' curves involve no gradient updates or fine-tuning, just increasing numbers of demonstrations given as conditioning.

Broadly, on NLP tasks GPT-3 achieves promising results in the zero-shot and one-shot settings, and in the the few-shot setting is sometimes competitive with or even occasionally surpasses state-of-the-art (despite state-of-the-art being held by fine-tuned models). For example, GPT-3 achieves 81.5 F1 on CoQA in the zero-shot setting, 84.0 F1 on CoQA in the one-shot setting, 85.0 F1 in the few-shot setting. Similarly, GPT-3 achieves 64.3% accuracy on TriviaQA in the zero-shot setting, 68.0% in the one-shot setting, and 71.2% in the few-shot setting, the last of which is state-of-the-art relative to fine-tuned models operating in the same closed-book setting.

GPT-3 also displays one-shot and few-shot proficiency at tasks designed to test rapid adaption or on-the-fly reasoning, which include unscrambling words, performing arithmetic, and using novel words in a sentence after seeing them defined only once. We also show that in the few-shot setting, GPT-3 can generate synthetic news articles which human evaluators have difficulty distinguishing from human-generated articles.

At the same time, we also find some tasks on which few-shot performance struggles, even at the scale of GPT-3. This includes natural language inference tasks like the ANLI dataset, and some reading comprehension datasets like RACE or QuAC. By presenting a broad characterization of GPT-3's strengths and weaknesses, including these limitations, we hope to stimulate study of few-shot learning in language models and draw attention to where progress is most needed.

A heuristic sense of the overall results can be seen in Figure 1.3, which aggregates the various tasks (though it should not be seen as a rigorous or meaningful benchmark in itself).

We also undertake a systematic study of 'data contamination' - a growing problem when training high capacity models on datasets such as Common Crawl, which can potentially include content from test datasets simply because such content often exists on the web. In this paper we develop systematic tools to measure data contamination and quantify its distorting effects. Although we find that data contamination has a minimal effect on GPT-3's performance on most datasets, we do identify a few datasets where it could be inflating results, and we either do not report results on these datasets or we note them with an asterisk, depending on the severity.

In addition to all the above, we also train a series of smaller models (ranging from 125 million parameters to 13 billion parameters) in order to compare their performance to GPT-3 in the zero, one and few-shot settings. Broadly, for most tasks we find relatively smooth scaling with model capacity in all three settings; one notable pattern is that the gap between zero-, one-, and few-shot performance often grows with model capacity, perhaps suggesting that larger models are more proficient meta-learners.

Finally, given the broad spectrum of capabilities displayed by GPT-3, we discuss concerns about bias, fairness, and broader societal impacts, and attempt a preliminary analysis of GPT-3's characteristics in this regard.

The remainder of this paper is organized as follows. In Section 2, we describe our approach and methods for training GPT-3 and evaluating it. Section 3 presents results on the full range of tasks in the zero-, one- and few-shot settings. Section 4 addresses questions of data contamination (train-test overlap). Section 5 discusses limitations of GPT-3. Section 6 discusses broader impacts. Section 7 reviews related work and Section 8 concludes.

## 2 Approach

Our basic pre-training approach, including model, data, and training, is similar to the process described in [RWC + 19], with relatively straightforward scaling up of the model size, dataset size and diversity, and length of training. Our use of in-context learning is also similar to [RWC + 19], but in this work we systematically explore different settings for learning within the context. Therefore, we start this section by explicitly defining and contrasting the different settings that we will be evaluating GPT-3 on or could in principle evaluate GPT-3 on. These settings can be seen as lying on a spectrum of how much task-specific data they tend to rely on. Specifically, we can identify at least four points on this spectrum (see Figure 2.1 for an illustration):

- Fine-Tuning (FT) has been the most common approach in recent years, and involves updating the weights of a pre-trained model by training on a supervised dataset specific to the desired task. Typically thousands to hundreds of thousands of labeled examples are used. The main advantage of fine-tuning is strong performance on many benchmarks. The main disadvantages are the need for a new large dataset for every task, the potential for poor generalization out-of-distribution [MPL19], and the potential to exploit spurious features of the training data [GSL + 18, NK19], potentially resulting in an unfair comparison with human performance. In this work we do not fine-tune GPT-3 because our focus is on task-agnostic performance, but GPT-3 can be fine-tuned in principle and this is a promising direction for future work.
- Few-Shot (FS) is the term we will use in this work to refer to the setting where the model is given a few demonstrations of the task at inference time as conditioning [RWC + 19], but no weight updates are allowed. As shown in Figure 2.1, for a typical dataset an example has a context and a desired completion (for example an English sentence and the French translation), and few-shot works by giving K examples of context and completion, and then one final example of context, with the model expected to provide the completion. We typically set K in the range of 10 to 100 as this is how many examples can fit in the model's context window ( n ctx = 2048 ). The main advantages of few-shot are a major reduction in the need for task-specific data and reduced potential to learn an overly narrow distribution from a large but narrow fine-tuning dataset. The main disadvantage is that results from this method have so far been much worse than state-of-the-art fine-tuned models. Also, a small amount of task specific data is still required. As indicated by the name, few-shot learning as described here for language models is related to few-shot learning as used in other contexts in ML [HYC01, VBL + 16] - both involve learning based on a broad distribution of tasks (in this case implicit in the pre-training data) and then rapidly adapting to a new task.
- One-Shot (1S) is the same as few-shot except that only one demonstration is allowed, in addition to a natural language description of the task, as shown in Figure 1. The reason to distinguish one-shot from few-shot and zero-shot (below) is that it most closely matches the way in which some tasks are communicated to humans. For example, when asking humans to generate a dataset on a human worker service (for example Mechanical Turk), it is common to give one demonstration of the task. By contrast it is sometimes difficult to communicate the content or format of a task if no examples are given.

Figure 2.1: Zero-shot, one-shot and few-shot, contrasted with traditional fine-tuning . The panels above show four methods for performing a task with a language model - fine-tuning is the traditional method, whereas zero-, one-, and few-shot, which we study in this work, require the model to perform the task with only forward passes at test time. We typically present the model with a few dozen examples in the few shot setting. Exact phrasings for all task descriptions, examples and prompts can be found in Appendix G.

<!-- image -->

- Zero-Shot (0S) is the same as one-shot except that no demonstrations are allowed, and the model is only given a natural language instruction describing the task. This method provides maximum convenience, potential for robustness, and avoidance of spurious correlations (unless they occur very broadly across the large corpus of pre-training data), but is also the most challenging setting. In some cases it may even be difficult for humans to understand the format of the task without prior examples, so this setting is in some cases 'unfairly hard'. For example, if someone is asked to 'make a table of world records for the 200m dash', this request can be ambiguous, as it may not be clear exactly what format the table should have or what should be included (and even with careful clarification, understanding precisely what is desired can be difficult). Nevertheless, for at least some settings zero-shot is closest to how humans perform tasks - for example, in the translation example in Figure 2.1, a human would likely know what to do from just the text instruction.

Figure 2.1 shows the four methods using the example of translating English to French. In this paper we focus on zero-shot, one-shot and few-shot, with the aim of comparing them not as competing alternatives, but as different problem settings which offer a varying trade-off between performance on specific benchmarks and sample efficiency. We especially highlight the few-shot results as many of them are only slightly behind state-of-the-art fine-tuned models. Ultimately, however, one-shot, or even sometimes zero-shot, seem like the fairest comparisons to human performance, and are important targets for future work.

Sections 2.1-2.3 below give details on our models, training data, and training process respectively. Section 2.4 discusses the details of how we do few-shot, one-shot, and zero-shot evaluations.

Table 2.1: Sizes, architectures, and learning hyper-parameters (batch size in tokens and learning rate) of the models which we trained. All models were trained for a total of 300 billion tokens.

| Model Name            | n params   |   n layers |   d model |   n heads |   d head | Batch Size   | Learning Rate   |
|-----------------------|------------|------------|-----------|-----------|----------|--------------|-----------------|
| GPT-3 Small           | 125M       |         12 |       768 |        12 |       64 | 0.5M         | 6 . 0 × 10 - 4  |
| GPT-3 Medium          | 350M       |         24 |      1024 |        16 |       64 | 0.5M         | 3 . 0 × 10 - 4  |
| GPT-3 Large           | 760M       |         24 |      1536 |        16 |       96 | 0.5M         | 2 . 5 × 10 - 4  |
| GPT-3 XL              | 1.3B       |         24 |      2048 |        24 |      128 | 1M           | 2 . 0 × 10 - 4  |
| GPT-3 2.7B            | 2.7B       |         32 |      2560 |        32 |       80 | 1M           | 1 . 6 × 10 - 4  |
| GPT-3 6.7B            | 6.7B       |         32 |      4096 |        32 |      128 | 2M           | 1 . 2 × 10 - 4  |
| GPT-3 13B             | 13.0B      |         40 |      5140 |        40 |      128 | 2M           | 1 . 0 × 10 - 4  |
| GPT-3 175B or 'GPT-3' | 175.0B     |         96 |     12288 |        96 |      128 | 3.2M         | 0 . 6 × 10 - 4  |

## 2.1 Model and Architectures

We use the same model and architecture as GPT-2 [RWC + 19], including the modified initialization, pre-normalization, and reversible tokenization described therein, with the exception that we use alternating dense and locally banded sparse attention patterns in the layers of the transformer, similar to the Sparse Transformer [CGRS19]. To study the dependence of ML performance on model size, we train 8 different sizes of model, ranging over three orders of magnitude from 125 million parameters to 175 billion parameters, with the last being the model we call GPT-3. Previous work [KMH + 20] suggests that with enough training data, scaling of validation loss should be approximately a smooth power law as a function of size; training models of many different sizes allows us to test this hypothesis both for validation loss and for downstream language tasks.

Table 2.1 shows the sizes and architectures of our 8 models. Here n params is the total number of trainable parameters, n layers is the total number of layers, d model is the number of units in each bottleneck layer (we always have the feedforward layer four times the size of the bottleneck layer, dff = 4 ∗ d model ), and d head is the dimension of each attention head. All models use a context window of n ctx = 2048 tokens. We partition the model across GPUs along both the depth and width dimension in order to minimize data-transfer between nodes. The precise architectural parameters for each model are chosen based on computational efficiency and load-balancing in the layout of models across GPU's. Previous work [KMH + 20] suggests that validation loss is not strongly sensitive to these parameters within a reasonably broad range.

## 2.2 Training Dataset

Datasets for language models have rapidly expanded, culminating in the Common Crawl dataset 2 [RSR + 19] constituting nearly a trillion words. This size of dataset is sufficient to train our largest models without ever updating on the same sequence twice. However, we have found that unfiltered or lightly filtered versions of Common Crawl tend to have lower quality than more curated datasets. Therefore, we took 3 steps to improve the average quality of our datasets: (1) we downloaded and filtered a version of CommonCrawl based on similarity to a range of high-quality reference corpora, (2) we performed fuzzy deduplication at the document level, within and across datasets, to prevent redundancy and preserve the integrity of our held-out validation set as an accurate measure of overfitting, and (3) we also added known high-quality reference corpora to the training mix to augment CommonCrawl and increase its diversity.

Details of the first two points (processing of Common Crawl) are described in Appendix A. For the third, we added several curated high-quality datasets, including an expanded version of the WebText dataset [RWC + 19], collected by scraping links over a longer period of time, and first described in [KMH + 20], two internet-based books corpora (Books1 and Books2) and English-language Wikipedia.

Table 2.2 shows the final mixture of datasets that we used in training. The CommonCrawl data was downloaded from 41 shards of monthly CommonCrawl covering 2016 to 2019, constituting 45TB of compressed plaintext before filtering and 570GB after filtering, roughly equivalent to 400 billion byte-pair-encoded tokens. Note that during training, datasets are not sampled in proportion to their size, but rather datasets we view as higher-quality are sampled more frequently, such that CommonCrawl and Books2 datasets are sampled less than once during training, but the other datasets are sampled 2-3 times. This essentially accepts a small amount of overfitting in exchange for higher quality training data.

[2 https://commoncrawl.org/the-data/](https://commoncrawl.org/the-data/)

Figure 2.2: Total compute used during training . Based on the analysis in Scaling Laws For Neural Language Models [KMH + 20] we train much larger models on many fewer tokens than is typical. As a consequence, although GPT-3 3B is almost 10x larger than RoBERTa-Large (355M params), both models took roughly 50 petaflop/s-days of compute during pre-training. Methodology for these calculations can be found in Appendix D.

<!-- image -->

Table 2.2: Datasets used to train GPT-3 . 'Weight in training mix' refers to the fraction of examples during training that are drawn from a given dataset, which we intentionally do not make proportional to the size of the dataset. As a result, when we train for 300 billion tokens, some datasets are seen up to 3.4 times during training while other datasets are seen less than once.

| Dataset                 | Quantity (tokens)   | Weight in training mix   |   Epochs elapsed when training for 300B tokens |
|-------------------------|---------------------|--------------------------|------------------------------------------------|
| Common Crawl (filtered) | 410 billion         | 60%                      |                                           0.44 |
| WebText2                | 19 billion          | 22%                      |                                            2.9 |
| Books1                  | 12 billion          | 8%                       |                                            1.9 |
| Books2                  | 55 billion          | 8%                       |                                           0.43 |
| Wikipedia               | 3 billion           | 3%                       |                                            3.4 |

A major methodological concern with language models pretrained on a broad swath of internet data, particularly large models with the capacity to memorize vast amounts of content, is potential contamination of downstream tasks by having their test or development sets inadvertently seen during pre-training. To reduce such contamination, we searched for and attempted to remove any overlaps with the development and test sets of all benchmarks studied in this paper. Unfortunately, a bug in the filtering caused us to ignore some overlaps, and due to the cost of training it was not feasible to retrain the model. In Section 4 we characterize the impact of the remaining overlaps, and in future work we will more aggressively remove data contamination.

## 2.3 Training Process

As found in [KMH + 20, MKAT18], larger models can typically use a larger batch size, but require a smaller learning rate. We measure the gradient noise scale during training and use it to guide our choice of batch size [MKAT18]. Table 2.1 shows the parameter settings we used. To train the larger models without running out of memory, we use a mixture of model parallelism within each matrix multiply and model parallelism across the layers of the network. All models were trained on V100 GPU's on part of a high-bandwidth cluster provided by Microsoft. Details of the training process and hyperparameter settings are described in Appendix B.

## 2.4 Evaluation

For few-shot learning, we evaluate each example in the evaluation set by randomly drawing K examples from that task's training set as conditioning, delimited by 1 or 2 newlines depending on the task. For LAMBADA and Storycloze there is no supervised training set available so we draw conditioning examples from the development set and evaluate on the test set. For Winograd (the original, not SuperGLUE version) there is only one dataset, so we draw conditioning examples directly from it.

K can be any value from 0 to the maximum amount allowed by the model's context window, which is n ctx = 2048 for all models and typically fits 10 to 100 examples. Larger values of K are usually but not always better, so when a separate development and test set are available, we experiment with a few values of K on the development set and then run the best value on the test set. For some tasks (see Appendix G) we also use a natural language prompt in addition to (or for K = 0 , instead of) demonstrations.

On tasks that involve choosing one correct completion from several options (multiple choice), we provide K examples of context plus correct completion, followed by one example of context only, and compare the LM likelihood of each completion. For most tasks we compare the per-token likelihood (to normalize for length), however on a small number of datasets (ARC, OpenBookQA, and RACE) we gain additional benefit as measured on the development set by normalizing by the unconditional probability of each completion, by computing P (completion | context) P (completion | answer context) , where answer context is the string "Answer: " or "A: " and is used to prompt that the completion should be an answer but is otherwise generic.

On tasks that involve binary classification, we give the options more semantically meaningful names (e.g. 'True' or 'False' rather than 0 or 1) and then treat the task like multiple choice; we also sometimes frame the task similar to what is done by [RSR + 19] (see Appendix G) for details.

On tasks with free-form completion, we use beam search with the same parameters as [RSR + 19]: a beam width of 4 and a length penalty of α = 0 . 6 . We score the model using F1 similarity score, BLEU, or exact match, depending on what is standard for the dataset at hand.

Final results are reported on the test set when publicly available, for each model size and learning setting (zero-, one-, and few-shot). When the test set is private, our model is often too large to fit on the test server, so we report results on the development set. We do submit to the test server on a small number of datasets (SuperGLUE, TriviaQA, PiQa) where we were able to make submission work, and we submit only the 200B few-shot results, and report development set results for everything else.

## 3 Results

In Figure 3.1 we display training curves for the 8 models described in Section 2. For this graph we also include 6 additional extra-small models with as few as 100,000 parameters. As observed in [KMH + 20], language modeling performance follows a power-law when making efficient use of training compute. After extending this trend by two more orders of magnitude, we observe only a slight (if any) departure from the power-law. One might worry that these improvements in cross-entropy loss come only from modeling spurious details of our training corpus. However, we will see in the following sections that improvements in cross-entropy loss lead to consistent performance gains across a broad spectrum of natural language tasks.

Below, we evaluate the 8 models described in Section 2 (the 175 billion parameter parameter GPT-3 and 7 smaller models) on a wide range of datasets. We group the datasets into 9 categories representing roughly similar tasks.

In Section 3.1 we evaluate on traditional language modeling tasks and tasks that are similar to language modeling, such as Cloze tasks and sentence/paragraph completion tasks. In Section 3.2 we evaluate on 'closed book' question answering tasks: tasks which require using the information stored in the model's parameters to answer general knowledge questions. In Section 3.3 we evaluate the model's ability to translate between languages (especially one-shot and few-shot). In Section 3.4 we evaluate the model's performance on Winograd Schema-like tasks. In Section 3.5 we evaluate on datasets that involve commonsense reasoning or question answering. In Section 3.6 we evaluate on reading comprehension tasks, in Section 3.7 we evaluate on the SuperGLUE benchmark suite, and in 3.8 we briefly explore NLI. Finally, in Section 3.9, we invent some additional tasks designed especially to probe in-context learning abilities these tasks focus on on-the-fly reasoning, adaptation skills, or open-ended text synthesis. We evaluate all tasks in the few-shot, one-shot, and zero-shot settings.

Figure 3.1: Smooth scaling of performance with compute. Performance (measured in terms of cross-entropy validation loss) follows a power-law trend with the amount of compute used for training. The power-law behavior observed in [KMH + 20] continues for an additional two orders of magnitude with only small deviations from the predicted curve. For this figure, we exclude embedding parameters from compute and parameter counts.

<!-- image -->

Table 3.1: Zero-shot results on PTB language modeling dataset. Many other common language modeling datasets are omitted because they are derived from Wikipedia or other sources which are included in GPT-3's training data. a [RWC + 19]

| Setting          | PTB    |
|------------------|--------|
| SOTA (Zero-Shot) | 35.8 a |
| GPT-3 Zero-Shot  | 20.5   |

## 3.1 Language Modeling, Cloze, and Completion Tasks

In this section we test GPT-3's performance on the traditional task of language modeling, as well as related tasks that involve predicting a single word of interest, completing a sentence or paragraph, or choosing between possible completions of a piece of text.

## 3.1.1 Language Modeling

We calculate zero-shot perplexity on the Penn Tree Bank (PTB) [MKM + 94] dataset measured in [RWC + 19]. We omit the 4 Wikipedia-related tasks in that work because they are entirely contained in our training data, and we also omit the one-billion word benchmark due to a high fraction of the dataset being contained in our training set. PTB escapes these issues due to predating the modern internet. Our largest model sets a new SOTA on PTB by a substantial margin of 15 points, achieving a perplexity of 20.50. Note that since PTB is a traditional language modeling dataset it does not have a clear separation of examples to define one-shot or few-shot evaluation around, so we measure only zero-shot.

## 3.1.2 LAMBADA

The LAMBADA dataset [PKL + 16] tests the modeling of long-range dependencies in text - the model is asked to predict the last word of sentences which require reading a paragraph of context. It has recently been suggested that the continued scaling of language models is yielding diminishing returns on this difficult benchmark. [BHT + 20] reflect on the small 1.5% improvement achieved by a doubling of model size between two recent state of the art results ([SPP + 19]

Table 3.2: Performance on cloze and completion tasks. GPT-3 significantly improves SOTA on LAMBADA while achieving respectable performance on two difficult completion prediction datasets. a [Tur20] b [RWC + 19] c [LDL19] d [LCH + 20]

| Setting         | LAMBADA (acc)   | LAMBADA (ppl)   | StoryCloze (acc)   | HellaSwag (acc)   |
|-----------------|-----------------|-----------------|--------------------|-------------------|
| SOTA            | 68.0 a          | 8.63 b          | 91.8 c             | 85.6 d            |
| GPT-3 Zero-Shot | 76.2            | 3.00            | 83.2               | 78.9              |
| GPT-3 One-Shot  | 72.5            | 3.35            | 84.7               | 78.1              |
| GPT-3 Few-Shot  | 86.4            | 1.92            | 87.7               | 79.3              |

Figure 3.2: On LAMBADA, the few-shot capability of language models results in a strong boost to accuracy. GPT-3 2.7B outperforms the SOTA 17B parameter Turing-NLG [Tur20] in this setting, and GPT-3 175B advances the state of the art by 18%. Note zero-shot uses a different format from one-shot and few-shot as described in the text.

<!-- image -->

and [Tur20]) and argue that 'continuing to expand hardware and data sizes by orders of magnitude is not the path forward'. We find that path is still promising and in a zero-shot setting GPT-3 achieves 76% on LAMBADA, a gain of 8% over the previous state of the art.

LAMBADA is also a demonstration of the flexibility of few-shot learning as it provides a way to address a problem that classically occurs with this dataset. Although the completion in LAMBADA is always the last word in a sentence, a standard language model has no way of knowing this detail. It thus assigns probability not only to the correct ending but also to other valid continuations of the paragraph. This problem has been partially addressed in the past with stop-word filters [RWC + 19] (which ban 'continuation' words). The few-shot setting instead allows us to 'frame' the task as a cloze-test and allows the language model to infer from examples that a completion of exactly one word is desired. We use the following fill-in-the-blank format:

Alice was friends with Bob. Alice went to visit her friend . → Bob

George bought some baseball equipment, a ball, a glove, and a . →

When presented with examples formatted this way, GPT-3 achieves 86.4% accuracy in the few-shot setting, an increase of over 18% from the previous state-of-the-art. We observe that few-shot performance improves strongly with model size. While this setting decreases the performance of the smallest model by almost 20%, for GPT-3 it improves accuracy by 10%. Finally, the fill-in-blank method is not effective one-shot, where it always performs worse than the zero-shot setting. Perhaps this is because all models still require several examples to recognize the pattern.