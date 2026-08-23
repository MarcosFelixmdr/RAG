# Parte 1 - Identificação dos Problemas
## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA
### 1.1 Descrição do Problema
#### Qual é o problema que você deseja resolver?
Na NBA, o ritmo é muito acelerado e os relatórios pós-jogo têm dezenas de páginas. Os técnicos não conseguem ler tudo isso no meio da partida. O problema é conseguir achar um detalhe tático exato em poucos segundos no meio do jogo.
#### Quem utilizaria a aplicação?
* **Cargo:** Assistente Técnico, Coordenador de Vídeo e Analista de Desempenho.
* **Contexto de uso:** No vestiário ou no tablet na beira da quadra durante o jogo.
* **Nível técnico:** Domínio absoluto de basquete e estratégia tática, mas nível básico a intermediário em tecnologia. Precisam fazer perguntas em linguagem natural e receber respostas imediatas sem depender de comandos complexos.
#### Que tipo de informação o usuário gostaria de consultar?
* Como o outro time defende certas jogadas.
* Para qual lado o jogador rival prefere ir quando tá sob pressão.
* Jogadas ensaiadas para o final do jogo.
* Como o time rival mudou os jogadores nos últimos jogos.
#### De onde vêm essas informações?
Vêm dos papéis e arquivos internos que a própria comissão técnica produz depois de analisar os vídeos dos jogos.
#### Por que utilizar um LLM sozinho não seria suficiente?
1. **Dados Privados:** Relatórios de *scouting* são dados sigilosos da franquia. Um LLM público/comercial não tem acesso aos documentos internos do time.
2. **Falta de Atualização:** Ele não sabe o que mudou no rival em um curto espaço de tempo.
3. **Risco de Alucinação:** Se o LLM inventar que um arremessador prefere ir para a esquerda quando a tendência real dele é ir para a direita, a instrução passada ao jogador em quadra estará errada e pode custar o jogo.
#### Como o usuário vai utilizar o sistema?
Através de um **aplicativo web** otimizado para navegação em **iPads/tablets**, que é a ferramenta que a comissão técnica já usa na beira da quadra e nas reuniões de vídeo.
---
### Perguntas Reais dos Usuários
1. *"Como Minnesota defende o Pick and Roll no topo quando o Edwards tá no banco?"*
2. *"O Tatum infiltra para qual lado quando dobra a marcação nele?"*
3. *"O Boston mudou a saída de fundo em relação ao mês passado?"*
---
### 1.2 Por que RAG?

#### Por que RAG é adequado para esse problema?
Porque o RAG pesquisa os relatórios internos antes de responder. Ele usa a inteligência do modelo de linguagem, mas força ele a ler os nossos arquivos atualizados ao invés de inventar informações.
#### Que tipo de conhecimento precisa ser fornecido ao modelo?
Relatórios de scouting do time, anotações de vídeo das jogadas do rival, observações dos analistas e resumos das reuniões táticas.
#### Esse conhecimento muda com que frequência?
Muda todo dia ou a cada dois dias, porque na NBA tem jogo o tempo todo e as táticas mudam por causa de lesões e escolhas táticas.
#### Existe necessidade de utilizar documentos privados ou específicos da organização?
**Sim, 100% dos documentos são privados e sigilosos.** Os relatórios de *scouting* são a vantagem competitiva da franquia e contêm estratégias confidenciais que não podem ser vazadas para outros times nem usadas para treinar modelos públicos.
#### Que problemas poderiam ocorrer se o LLM respondesse apenas com seu conhecimento pré-treinado?
Ele daria respostas genéricas da internet, desatualizadas ou inventadas.
**Exemplo concreto de resposta errada:**
* **Pergunta:** *"Como o Denver defende a dobra no topo no segundo tempo?"*
* **Resposta sem RAG:** *"Eles usam marcação por zona 2-3 para fechar o garrafão."*
* **Por que é um desastre:** Na vida real o Denver joga homem a homem. Se o técnico acreditar nisso, vai desenhar o ataque errado e perder a posse de bola.
---
### 1.3 Limitações - Quando RAG Não É a Resposta
#### Em quais situações RAG não seria a melhor solução para esse problema?
O RAG é péssimo para fazer contas matemáticas e puxar estatísticas exatas. Se a gente precisar somar pontos ou calcular médias, o RAG não serve.
---
#### Análise das Alternativas Tecnológicas
* **Busca tradicional por palavra-chave (BM25):** Melhor para achar o nome exato de uma jogada como *"Spain PnR"*.
* **Banco de dados estruturado e consultas SQL:** Perfeito para contas, médias e porcentagens de arremesso.
* **Regras determinísticas:** Ideal para controlar quem pode ou não acessar o sistema.
* **Combinação de alguma dessas técnicas com RAG:** Misturar a busca por palavras com busca por significado, e mandar perguntas de números direto para um banco SQL.
---
#### Qual pergunta do próprio cenário o RAG responderia mal e um banco relacional responderia bem?
* **Pergunta:** *"Qual o aproveitamento de 3 pontos do Tatum nos últimos 5 jogos contra defesa em zona?"*
* **Por que o RAG vai mal:** Teria que ler um monte de texto, tentar achar os números e fazer a conta de dividir, o que é oponto fraco do RAG.
* **Por que o SQL vai bem:** Ele faz uma conta exata na tabela de estatísticas em milissegundos.
---
# Parte 2 - Organização dos Documentos
## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA
### 2.1 Descrição e Especificação dos Arquivos
* **Tipos de arquivo:** Arquivos de texto em Markdown (`.md`), PDFs de estatísticas e arquivos JSON de transcrições de vídeo.
* **Volume aproximado:** Uns 300 a 400 documentos por ano.
* **Tamanho típico:** De 2 a 8 páginas por relatório (arquivos leve de texto).
* **Frequência e ciclo de vida:** Entram arquivos novos todo dia de jogo. Os antigos não são apagados, viram histórico.
---
### 2.2 Proposta da Estrutura de Pastas

```
documentos_scouting/
├── 2025-2026/
│   ├── adversarios/
│   │   ├── boston_celtics/
│   │   │   ├── 2025-11-12_jogo_01_pre.md
│   │   │   ├── 2025-11-12_jogo_01_pos.md
│   │   │   └── 2026-03-10_jogo_02_pre.md
│   │   └── minnesota_timberwolves/
│   │       └── 2026-01-20_jogo_01_pre.md
│   ├── interno/
│   │   ├── playbooks/
│   │   │   └── ataque_transicao_v2.md
│   │   └── relatorios_individuais/
│   │       └── evolucao_defensiva_calouros.md
│   └── liga_geral/
│       └── tendencias_arbitragem_2026.pdf
└── arquivo_temporadas/
    └── 2024-2025/

```
#### Justificativa da Estrutura:
A organização por **`Temporada -> Categoria (Adversário/Interno) -> Franquia`** reflete exatamente a forma como os analistas e treinadores pensam na informação.
Quando o assistente técnico vai preparar a equipe para o jogo da noite contra o *Boston Celtics*, o contexto tático que importa é o da **temporada atual**. Dividir as pastas dessa forma permite que o pipeline de ingestão e o mecanismo de busca apliquem filtros de diretório diretamente na leitura dos arquivos, além de mapear a estrutura física das pastas para os metadados de `temporada`, `time_adversario` e `tipo_documento` automaticamente na ingestão.
---
### 2.3 Gestão e Segurança
#### O que NÃO entra e como impedir?
Contratos de dinheiro, exames médicos dos jogadores e rascunhos não revisados. A gente impede colocando travas no sistema para ele só ler pastas autorizadas e ignorar arquivos marcados como "privado".
#### Como lidar com VERSÕES?
Colocando etiquetas de data em cada trecho de texto. Quando um relatório novo do mesmo time chega, o sistema marca os antigos como "arquivados" para a IA não usar tática velha por engano.
---

# Parte 3 - Pipeline de Ingestão
**Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA**
**Arquitetura do Fluxo de Ingestão**
O fluxo de ingestão é o "esteira de produção" que pega os arquivos brutos criados pela galera do vídeo e do *scouting* e os transforma em dados prontos para a IA pesquisar. O caminho que a informação faz é este:

```
[ Documentos Brutos (.md, .pdf, .json) ]
                  │
                  ▼
         [ 1. Extração de Texto ]
                  │
                  ▼
       [ 2. Limpeza / Normalização ]
                  │
                  ▼
  [ 3. Enriquecimento de Metadados via LLM ]
                  │
                  ▼
       [ 4. Chunking / Splitting ]
                  │
                  ▼
        [ 5. Vetorização / Embeddings ]
                  │
                  ▼
  [ 6. Armazenamento no Banco Vetorial (ChromaDB) ]

```
---
### 3.1 Detalhamento da Etapa de Extração
Nesta etapa, o objetivo é pegar arquivos de todos os tipos e tamanhos sobre *scouting* e tática e transformar tudo em texto limpo e organizado, sem perder nenhum detalhe do jogo.
* **PDFs com texto selecionável (Relatórios digitais de plataformas como Synergy ou Second Spectrum):**
* **Como tratar:** Usamos ferramentas de programação (como `pdfplumber` ou `UnstructuredPDFLoader`) para ler e puxar a camada de texto direto do arquivo. O sistema foca em ler na ordem correta da página e joga fora o que é só enfeite visual, como logos de times e marcas d'água.
* **PDFs digitalizados (Análises escaneadas e papéis rabiscados pela comissão):**
* **Como tratar:** Passamos os arquivos por um leitor óptico de imagens (OCR, usando `Tesseract` ou `EasyOCR`). Antes do sistema tentar ler as letras, a imagem passa por um "tapa visual" (ajuste de brilho, contraste e limpeza de sujeiras da folha) para conseguir entender até anotações feitas à mão ou papéis antigos escaneados.
* **Tratamento de Tabelas (Quadros de números e mapas de arremesso):**
* **É importante manter?** **Sim, crucial.** As tabelas trazem os dados mais importantes do *scouting* (ex: porcentagem de acerto por área da quadra, eficiência defendendo o *Pick and Roll*).
* **Como tratar:** Não podemos ler uma tabela como se fosse um texto comum solto, senão os números se misturam. O leitor `pdfplumber` transforma a tabela em uma estrutura organizada de texto (em formato **Markdown** ou **JSON**). Isso garante que o sistema não perca a linha do raciocínio (ex: entenda claramente que *"Canto Esquerdo"* se refere a *"45% de aproveitamento"*).
* **Tratamento de Imagens (Desenhos de prancheta e diagramas de jogadas):**
* **Posso descartar?** De jeito nenhum, se a foto mostrar o desenho de uma jogada com setas e posições dos jogadores.
* **Quais informações elas têm?** A rota que o atacante faz, onde o pivô tem que fazer o bloqueio e como a defesa se posiciona.
* **Como tratar:** O sistema pega a imagem e manda para uma IA de visão (como o `GPT-4o`). A IA "olha" o desenho e escreve um resumo detalhado em texto do que está acontecendo ali (ex: *"Desenho tático mostrando o armador recebendo um bloqueio cego na cabeça do garrafão enquanto o pivô abre para a linha de três"*). O sistema substitui a foto por essa explicação em texto.
* **Tratamento de Documentos Multimodais (Vídeos de jogos + Áudios das reuniões do time):**
* **Vídeo + Áudio:** Os arquivos de áudio das reuniões da comissão técnica são passados pela ferramenta de transcrição **Whisper (da OpenAI)**, que transforma toda a fala dos técnicos em texto escrito.
* **Sincronização de Minutagem:** A transcrição é gravada junto com o relógio do jogo (*timestamps*). O sistema cria um documento onde a fala do técnico fica colada no segundo exato do vídeo da partida (ex: *"Aos 02:15 do 3º quarto: repare como o pivô afunda na área pintada"*).
---
#### Problemas que podem surgir durante a extração e casos concretos
1. **Desalinhamento da Ordem de Leitura em Múltiplas Colunas:**
* **O problema:** Os relatórios costumam ter texto dividido em duas ou três colunas na folha. Se o leitor do sistema for meio "burro", ele lê direto na horizontal, juntando o começo da primeira coluna com o começo da segunda. Vira uma maçaroca que não dá para entender nada.
2. **Perda de Contexto em Tabelas Sem Bordas:**
* **O problema:** Quando a tabela não tem aquelas linhas desenhadas, o leitor de imagem se perde e junta todos os números numa frase só (tipo *"Tatum 25 10 4 45%"*). Aí a gente não sabe o que é ponto, o que é rebote ou o que é aproveitamento.
3. **Caso Concreto (Problema Enfrentado na Aula 04 / Atividades Anteriores):**
* **Caso:** Quando a gente tentou ler os arquivos na Aula 04, o sistema quebrou as linhas de qualquer jeito. Ele sumiu com os títulos e colou o começo de um assunto no fim do outro. Ficou tudo misturado — tática de ataque junta com tática de defesa —, e o sistema se perdeu inteirinho na hora de procurar as respostas.

### 3.2 Limpeza e normalização
#### O que precisa ser removido?
* **Cabeçalhos e Rodapés Repetidos:** Coisas que se repetem em toda folha, tipo *"Relatório Secreto do Celtics"* ou *"Página 3 de 12"*. Se deixar isso, a IA acha que essa frase é super importante só porque aparece toda hora.
* **Marcas d'Água e Lixo Visual:** Palavras como *"RASCUNHO"* ou *"USO PRIVADO"* que o leitor de imagem puxa sem querer.
* **Números de Página e Sumários:** Listas de capítulos e números de página perdidos no meio do texto que só atrapalham a leitura.
* **Sujeiras do Arquivo:** Linhas divisórias tipo `-------------------`, links quebrados e códigos estranhos de computador.
---
#### O que precisa ser padronizado?
* **Termos de Basquete e Siglas:**
* Deixar tudo escrito do mesmo jeito. Tipo, transformar `"P&R"`, `"pnr"` e `"pick-and-roll"` em uma coisa só: `"Pick and Roll"`.
* Traduzir siglas para o português normal (ex: trocar `"PG"` por `"Armador"` ou `"ATO"` por `"Depois do Pedido de Tempo"`).
* **Tipo de Texto (Encoding):**
* Salvar tudo no padrão **UTF-8** para sumir com aqueles símbolos estranhos e letras com acento quebradas.
* **Espaços e Linhas Cortadas:**
* Juntar palavras que foram cortadas no fim da linha (transformar `"de- fesa"` em `"defesa"`).
* Tirar aquele monte de espaço em branco e linhas vazias acumuladas.
---
#### Que informação você corre o risco de perder ao limpar demais?
1. **Os Títulos dos Assuntos (Markdown):**
Se apagar os símbolos de título (tipo `#` ou `##`) na empolgação de limpar, a IA não vai mais saber onde termina a parte do *"Ataque"* e onde começa a da *"Defesa"*, misturando tudo num bloco só.
2. **Nomes dos Jogadores com Acento:**
Se tirar os acentos para simplificar (mudar `"Nikola Jokić"` para `"Nikola Jokic"`), o sistema pode se perder na hora que alguém pesquisar o nome do jogador escrito do jeito certo.
3. **Palavras de Negação (O "Não"):**
Se o limpador sair apagando pontuação ou palavrinhas curtas, ele pode mudar totalmente o sentido da tática. Uma frase como *"Não dobrar na marcação"* pode virar *"Dobrar na marcação"*, o que seria um desastre em quadra.
### 3.3 Frequência de ingestão
#### Como o pipeline roda e com que frequência chegam novos documentos?
* **Modo de Execução:** Ele roda de um jeito **misto: quando o arquivo chega e em horários programados**.
1. **Aviso Automático (Na hora):** Quando o analista joga um arquivo novo de relatório na pasta do time, o sistema percebe sozinho e processa aquele arquivo imediatamente.
2. **Agendado (Na madrugada):** Todo dia às 3h da manhã, roda um processo automático para puxar e organizar as falas dos vídeos e dados de plataformas parceiras.
* **Frequência de Chegada dos Documentos:**
* **Em Dias de Jogo:** Chegam de 2 a 4 relatórios novos por dia (análise do rival, plano de jogo e o resumo do que rolou na partida).
* **Em Dias sem Jogo:** Chega pouca coisa, tipo 1 ou 2 arquivos de treino ou de como os jogadores estão evoluindo.
---
#### Reprocessamento: Apenas o documento atualizado ou a base inteira?
* **Estratégia Escolhida:** Processar **só o arquivo que mudou (Incremental)**.
* **Por que não reprocessar tudo do zero?** Fazer o sistema ler todos os arquivos de novo a cada relatório novo custa uma fortuna em IA e faz o tablet do técnico demorar para receber a informação atualizada.

# Parte 4 - Metadados
### 4.1 Metadados do Documento
Os metadados no nível de documento são atribuídos no momento da ingestão e servem como pilar para o filtro pré-busca (*Pre-Retrieval Filtering*). Isso garante que o sistema restrinja a busca vetorial apenas ao universo de documentos táticos relevantes para a partida.
#### Schema JSON do Documento
json
{
  "document_id": "doc_scout_bos_20260310_01",
  "title": "Relatório de Scouting Pré-Jogo - Boston Celtics",
  "author": "Lucas Silva (Analista Head de Scouting)",
  "source": "documentos_scouting/2025-2026/adversarios/boston_celtics/2026-03-10_jogo_02_pre.md",
  "document_type": "scouting_pre_jogo",
  "created_at": "2026-03-09T18:30:00Z",
  "updated_at": "2026-03-10T10:15:00Z",
  "category": "adversarios",
  "temporada": "2025-2026",
  "time_adversario": "Boston Celtics",
  "data_partida": "2026-03-10",
  "mando_campo": "casa",
  "versao_relatorio": "2.0",
  "is_latest": true,
  "nivel_acesso": "comissao_tecnica"
}

### 4.2 Metadados do Chunk
Enquanto os metadados do documento descrevem o arquivo como um todo, os metadados do *chunk* trazem granularidade tática ao trecho específico de texto. Isso garante precisão cirúrgica no *retrieval* e citação exata de fonte.
#### Schema JSON do Chunk
json
{
  "document_id": "doc_scout_bos_20260310_01",
  "chunk_id": "doc_scout_bos_20260310_01-c04",
  "chunk_index": 4,
  "page": 2,
  "section": "Defesa de Pick and Roll",
  "fase_jogo": "defesa_pnr",
  "jogadores_foco": ["Jayson Tatum", "Al Horford"],
  "time_adversario": "Boston Celtics",
  "temporada": "2025-2026",
  "data_partida": "2026-03-10",
  "is_latest": true,
  "text": "Contra o Pick and Roll no topo da chave, o Celtics utiliza Drop Coverage com Al Horford recuado no garrafão, enquanto Tatum passa por cima do bloqueio para contestar o arremesso de média distância."
}

#### Justificativa de Cada Metadado Escolhido
* **`document_id` (`string`):** O código que liga o pedaço de texto ao arquivo original.
* **`chunk_id` (`string`):** O RG único desse pedacinho de texto no banco. Serve para apagar ou alterar ele depois.
* **`chunk_index` (`integer`):** A posição dele no texto (ex: pedaço 1, pedaço 2). Ajuda a puxar o trecho de antes ou de depois para entender melhor o contexto.
* **`page` (`integer`):** O número da página do PDF de onde o texto saiu.
* **`section` (`string`):** O título da seção do relatório (ex: *"Defesa de Pick and Roll"*).
* **`fase_jogo` (`string`):** A categoria da jogada (ex: *"defesa"*, *"contra-ataque"*, *"bola parada"*).
* **`jogadores_foco` (`list[string]`):** Lista com os nomes dos jogadores citados no trecho.
* **Herança do Arquivo Pai (`time_adversario`, `temporada`, `data_partida`, `is_latest`):** Informações copiadas do arquivo principal para conseguir filtrar o texto direto no banco de dados, sem ter que fazer buscas complexas.
---
### Respostas às Perguntas do Projeto
#### 1. Quais metadados você usaria para filtrar a busca? Dê um exemplo de pergunta em que o filtro é indispensável.
* **Metadados de Filtro:** `time_adversario`, `temporada`, `fase_jogo`, `is_latest` e `jogadores_foco`.
* **Exemplo de Pergunta Indispensável:**
> *"Como o Boston Celtics defendeu o Pick and Roll nos últimos jogos sem o Porziņģis em quadra?"*
* **Por que é indispensável?**
Se a gente não filtrar e pesquisar só "defesa de Pick and Roll", a IA vai trazer dados do *Lakers* ou de dois anos atrás. Com o filtro ligado (`time_adversario == "Boston Celtics"` e `is_latest == true`), a gente força o sistema a procurar **só** nos relatórios recentes do Celtics.
---
#### 2. Quais metadados você usaria para citar a fonte ao usuário? O que exatamente apareceria na tela junto da resposta?
* **Metadados para Citação:** `title`, `data_partida`, `section`, `page` e `author`.
* **O que aparece na tela do tablet do técnico:**
> **Resposta da IA:**
> *"O Boston Celtics deixa o pivô recuado na área pintada contra o Pick and Roll e força o arremesso de meia distância."*
> **Fonte Consultada:**
> *Relatório de Scouting Pré-Jogo - Boston Celtics*
> **Data:** 10/03/2026 | **Seção:** *Defesa de Pick and Roll* (Pág. 2)
> **Analista:** *Lucas Silva (Head de Scouting)*
---
#### 3. Que metadado seria caríssimo de acrescentar depois que a base já estivesse indexada? Por quê?
* **Metadados Caríssimos:** **`fase_jogo`** e **`jogadores_foco`** (que exigem leitura da IA).
* **Por quê?**
Coisas simples como a data ou o time adversário o computador descobre fácil olhando o nome da pasta. Mas para saber a `fase_jogo` ou quais `jogadores_foco` estão no texto, a gente precisa pagar uma IA para **ler pedaço por pedaço de milhares de textos**. Se decidir colocar isso depois que tudo já foi salvo, vai ter que pagar o processamento de tudo de novo do zero.
---
#### 4. Como você vai extrair esses metadados?
A gente tira essas informações de três jeitos durante a leitura:
1. **Olhando a pasta do arquivo:**
O sistema lê o caminho da pasta (tipo `/2025-2026/boston_celtics/`) e já descobre sozinho a `temporada` e o `time_adversario`.
2. **Lendo a estrutura do documento:**
O cortador de texto identifica os títulos com `#` para preencher o campo `section`, enquanto o leitor de PDF anota o `chunk_index` e a `page`.
3. **Usando uma IA leve para analisar o texto:**
Antes de salvar, uma IA rápida lê o pedacinho de texto e devolve uma listinha pronta com a `fase_jogo` e os `jogadores_foco` encontrados.

# Parte 5 - Chunking / Splitting
### Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA**
### 5.1 Estratégia de Chunking e Configurações**
* **Estratégia Escolhida:** `RecursiveCharacterTextSplitter` usando a própria estrutura do Markdown para cortar o texto sem quebrar frases ao meio.
* **Tamanho e Sobreposição:** Chunks de **350 a 500 caracteres** com sobreposição de **50 a 70 caracteres** (para não perder o fio da meada entre um pedaço e outro).
* **Regra por Tipo de Arquivo:**
* **Relatórios (.md):** Corta respeitando os títulos (`#`, `##`).
* **Vídeos/Áudios (.json/.txt):** Corta por tempo (a cada 1 ou 2 min) ou por fala de quem está discursando.
* **Tabelas (.pdf):** Mantém a tabela inteira em um pedaço só.
---
**5.2 Respostas às Perguntas de Avaliação**
* **Se o pedaço for pequeno demais:** Falta contexto. Viram frases soltas (tipo *"Celtics faz dobra"*), e a IA não sabe responder *quem*, *quando* ou *onde*.
* **Se o pedaço for grande demais:** A informação principal fica "diluída" no meio de tanto texto, gastando mais processamento e fazendo o sistema ignorar o detalhe importante.
* **Como tratar Tabelas e Imagens:**
* **Tabelas:** Cortadas ao meio perdem o sentido (os números ficam sem os cabeçalhos). A regra é nunca cortar; se for gigante, repete o nome das colunas em cada linha.
* **Imagens (Pranchetas):** Não se cortam imagens. Uma IA de visão lê o desenho antes e transforma a jogada em um resumo escrito.
* **Como provar se o corte ficou bom:**
* **Métricas automáticas:** Testar se o sistema acha as respostas certas sem trazer "lixo" junto.
* **Teste prático:** Pegar 20 perguntas reais dos técnicos e provar que o tamanho de ~450 caracteres é o que mais acerta os esquemas táticos.

# Parte 6 - Embeddings**

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA**
### 6.1 Tabela Comparativa e Especificação do Modelo**
| Item | Especificação no Cenário da NBA |
| --- | --- |
| **Modelo escolhido** | **`text-embedding-3-small` (OpenAI)** / *Opção Local:* `BAAI/bge-m3` |
| **Tamanho do vetor** | **1.536 dimensões** (dá para diminuir se precisar de mais rapidez) |
| **Entende português?** | **Sim**, funciona super bem em português e inglês |
| **É multilíngue?** | **Sim** (entende mais de 100 línguas) |
| **Tamanho máximo de texto** | **8.191 tokens** (~6.000 palavras por vez) |
| **É código aberto (grátis)?** | **Não** (é um serviço pago da OpenAI) |
| **Roda no nosso computador?** | **Não** (depende da internet e dos servidores da OpenAI) |
| **Tem API de integração?** | **Sim** (integra direto no nosso sistema) |
| **Custo aproximado** | **Centavos de dólar** (uns R$ 0,10 para processar 1 milhão de palavras) |
| **Link oficial** | [Documentação da OpenAI](https://platform.openai.com/docs/guides/embeddings) |

### 6.2 Justificativa: Por que esse modelo é adequado ao cenário?
Ele é a escolha perfeita porque entrega **alta precisão custando quase nada**.
Na prática, relatórios de basquete usam termos em inglês (como *"Pick and Roll"* e *"Drop Coverage"*) misturados com observações em português. Por ser multilíngue, o modelo entende o significado das jogadas mesmo trocando de idioma. Suas 1.536 dimensões conseguem diferenciar detalhes táticos sutis (tipo a diferença de uma dobra no topo ou na linha de fundo) em milissegundos.
---
### 6.3 Respostas às Perguntas de Análise
#### Considerou algum modelo alternativo e descartou? Qual, e por quê?
* **Modelos Avaliados:** `text-embedding-ada-002` (antigo da OpenAI) e `all-MiniLM-L6-v2` (modelo aberto da Hugging Face).
* **Por que descartou?**
* O `ada-002` ficou ultrapassado: é mais caro e entende pior os textos do que o modelo atual.
* O `all-MiniLM-L6-v2` aceita textos muito curtos (no máximo uns 2 parágrafos pequenos), o que cortaria a explicação de jogadas mais longas.
---
#### Se o cenário envolve documentos sigilosos, isso muda sua escolha entre modelo local e API? Como?
**Sim, totalmente.** Se a regra do time mudar sobre sigilo de dados, a arquitetura muda na hora:
* **Pela API / Nuvem (Escolha Principal):** Usando a conta empresarial da OpenAI, o contrato garante que nossos relatórios secretos **não** são usados para treinar a IA deles.
* **Rodando em Servidor Próprio (Opção Secreta):** Se os donos do time proibirem o envio de dados para fora, trocamos para o **`BAAI/bge-m3`**. Por ser um modelo aberto, instalamos ele dentro do computador do centro de treinamento e rodamos tudo sem precisar de internet.
---
#### O tamanho máximo de entrada do modelo tem relação com a sua decisão de chunking da Parte 5? Explique.
**Sim, completamente.** O limite de entrada do modelo é o "teto" máximo de palavras que um pedaço de texto pode ter.
O modelo aguenta textos grandes (até ~6.000 palavras), mas na Parte 5 escolhemos pedaços bem pequenos (de 350 a 500 caracteres). Fizemos isso porque, se o texto for gigante, a IA faz um "resumão" do pedaço inteiro e esquece as táticas pequenas. Pedaços menores garantem que a busca ache exatamente a jogada que o técnico precisa.



###################################################### Cenário 2 ###############################################################################################

# Parte 1 - Identificação dos Problemas
## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária
### 1.1 Descrição do Problema
#### Qual é o problema que você deseja resolver?
Achar livro pesquisando só por nome do autor ou título não funciona quando a pessoa quer uma história por causa do "clima", do estilo de escrita ou da sensação da leitura. Além disso, as editoras recebem pilhas de manuscritos e relatórios de leitura, e os editores perdem um tempão para descobrir quais livros do catálogo encaixam no gosto de cada leitor.
---
#### Quem utilizaria a aplicação? (Descrição concreta do usuário)
* **Perfil 1: Editor ou Curador Literário**
* **Cargo:** Editor de livros ou responsável por indicar obras em clubes de leitura.
* **Contexto de uso:** Nas reuniões de pauta ou ao responder os leitores, tentando achar rapidamente livros do acervo que combinem com pedidos específicos (tipo *"quero algo com o clima de tal obra"*).
* **Nível técnico:** Entende tudo de literatura e livros, mas nada de programação.
* **Perfil 2: Leitor Comum**
* **Cargo:** Assinante do aplicativo ou cliente do site de livros.
* **Contexto de uso:** Procurando a próxima leitura no celular no tempo livre.
* **Nível técnico:** Leigo total em tecnologia.
---
#### Que tipo de informação o usuário gostaria de consultar?
* Resumos detalhados e opiniões dos críticos.
* Trechos marcantes e amostras de capítulos.
* Avaliações internas sobre o ritmo da história e avisos de temas sensíveis.
* Fichas com os dados do livro (gênero, ano de lançamento, prêmios e época em que se passa a história).
---
#### De onde vêm essas informações?
1. **Arquivos dos próprios livros (`.epub`, `.pdf`):** O texto completo do livro ou amostras de capítulos.
2. **Relatórios da equipe (`.md`, `.docx`):** Pareceres internos feitos pelos leitores da editora.
3. **Fichas do catálogo (`.json`, `.csv`):** Dados de publicação (autor, ano, gênero, prêmios).
---
#### Por que utilizar um LLM sozinho não seria suficiente?
* **A IA inventa histórias:** Se deixar a IA responder sozinha, ela começa a inventar finais, misturar livros diferentes e citar personagens que nem existem na história.
* **Ela não conhece nosso acervo:** A IA genérica da internet não tem acesso aos livros inéditos nem aos relatórios secretos mantidos pela editora.
* **Fica caro demais:** Copiar e colar livros inteiros de 300 páginas na conversa com a IA a cada pergunta sairia uma fortuna e travaria o sistema.
---
#### Como o usuário vai utilizar o sistema?
Os editores vão usar através de um painel simples no navegador do computador, e os leitores vão usar por meio de um botão ou aba de recomendação no aplicativo do celular.
---
#### Três Perguntas Reais de Usuários (Casos Concretos)
1. *"Quero um romance de ficção científica num futuro feio, mas focado na relação de uma família e não em guerras. Qual livro nosso tem isso?"*
2. *"Tem algum suspense no acervo com aquele clima sufocante de 'O Iluminado', mas escrito por uma autora da América Latina?"*
3. *"Quais livros publicados entre 2020 e 2024 falam sobre luto na infância sem usar uma linguagem muito pesada?"*

### 1.2 Por que RAG?

#### Por que RAG é adequado para esse problema?
O RAG é perfeito para isso porque junta a capacidade da IA de entender e conversar com a nossa lista real de livros. Em vez de adivinhar, o RAG vai direto nos relatórios e nos trechos dos livros para encontrar a resposta exata, garantindo que o sistema só indique histórias que realmente existem no nosso catálogo.
---
#### Que tipo de conhecimento precisa ser fornecido ao modelo?
* **Relatórios e Pareceres Internos:** As anotações da nossa equipe sobre o tom da história, o ritmo, os temas principais e os avisos de conteúdo sensível.
* **Trechos e Capítulos dos Livros:** Amostras dos textos (`.epub`, `.pdf`, `.md`) para a IA avaliar o estilo de escrita e a linguagem do autor.
* **Ficha Completa do Catálogo:** Dados como título, autor, gênero, ano, público-alvo, prêmios e situação dos direitos autorais.
---
#### Esse conhecimento muda com que frequência?
* **De Toda Semana a Todo Mês:** Muda o tempo todo, conforme novos livros são avaliados pelos pareceristas, contratos são assinados ou novos títulos chegam ao catálogo.
---
#### Existe necessidade de utilizar documentos privados ou específicos da organização?
* **Sim, total.** Os pareceres dos livros não publicados, os relatórios da equipe e os dados de compra de direitos são segredos da editora e nunca estiveram na internet para a IA aprender.
---
#### Que problemas poderiam ocorrer se o LLM respondesse apenas com seu conhecimento pré-treinado? (Com Exemplo Concreto)
A IA iria **inventar livros da cabeça dela** e **ignorar o nosso catálogo**:
1. Indicaria livros de outras editoras em vez de vender os nossos.
2. Misturaria histórias e personagens que não têm nada a ver.
3. Não saberia nada sobre os livros novos que acabaram de chegar na editora.
* **Exemplo de Resposta Errada (Sem RAG):**
> **Pergunta do Editor:**
> *"Qual livro de suspense do nosso catálogo tem uma história fora de ordem focada em trauma de família, parecido com 'A Garota no Trem'?"*
> **Resposta Errada da IA Solta:**
> *"Recomendo o livro **'O Segredo da Casa Amarela'**, da Juliana Mendes, que vocês lançaram em 2023. É um suspense sobre uma mulher com amnésia tentando lembrar do passado por diários no sótão."*
> **O Erro:** Esse livro **simplesmente não existe** (a IA inventou o nome e a autora), e a história é só uma colagem de clichês que não tá em nenhum livro do nosso acervo.

### 1.3 Limitações — Quando RAG Não É a Resposta

#### Em quais situações RAG não seria a melhor solução para esse problema?
O RAG é ruim quando a gente precisa de contas exatas, dados cadastrais ou regras fixas. Nesses casos, três opções funcionam bem melhor:
1. **Banco de Dados Tradicional (SQL):**
* **Para que serve:** Achar dados exatos como código do livro (ISBN), preço, data de lançamento ou quantidade no estoque.
* **Por que é melhor:** O RAG tenta adivinhar por proximidade de assunto e pode se confundir com números exatos. O banco comum entrega o número certo na hora.
2. **Busca Simples por Palavra-Chave:**
* **Para que serve:** Encontrar nomes difíceis de autores, códigos ou títulos exatos.
* **Por que é melhor:** A IA de vetores nem sempre entende nomes próprios raros. A busca por palavra-chave só procura a palavra exata digitada e pronto.
3. **Busca Mista (Misturar Palavra-Chave, RAG e SQL):**
* **Para que serve:** Perguntas misturadas, tipo *"livro com clima triste, lançado em 2022 e com menos de 300 páginas"*.
* **Como funciona:** O sistema separa a pergunta: o que é filtro fixo (ano e número de páginas) ele busca no banco de dados, e o que é clima/história ele busca no RAG. Depois ele junta as duas respostas.
---
#### Existe alguma pergunta, dentro do seu próprio cenário, que RAG responderia mal e um banco de dados relacional responderia bem? Qual, e por quê?
* **Exemplo de pergunta ruim para o RAG:**
> *"Quantos livros de ficção científica lançados depois de 2020 temos no catálogo e qual é o preço médio deles?"*
* **Por que o RAG vai mal:** Ele teria que puxar centenas de pedaços de texto, tentar contar livro por livro na "cabeça" da IA e calcular a média. Vai demorar, custar caro e a IA provavelmente vai errar a conta de matemática.
* **Por que o Banco Comum (SQL) vai bem:** Uma linha simples de código resolve tudo com exatidão e na hora:
```sql
SELECT COUNT(*), AVG(preco) 
FROM catalogo_livros 
WHERE genero = 'Ficção Científica' AND ano_publicacao > 2020;

```
---
#### O que aconteceria se a pergunta do usuário exigisse contar, somar ou ordenar informação espalhada por muitos documentos?
Se pedirem algo tipo *"Ordene todos os pareceres dos livros pela nota da equipe"*, o RAG vai falhar por três motivos:
1. **Ele só pega um pedaço do acervo:** O RAG é configurado para buscar só os 5 ou 10 pedaços de texto mais parecidos. Ele nunca traz o catálogo inteiro, então vai deixar um monte de livro de fora.
2. **A IA se perde com muito texto:** Mesmo que a gente mandasse centenas de páginas para ela ler de uma vez, a IA acaba esquecendo os dados que ficam no meio do texto.
3. **A IA não sabe somar ou ordenar de verdade:** Como o modelo só tenta adivinhar qual é a próxima palavra mais provável, ele não tem uma "calculadora" por dentro. A chance de inventar a ordem ou errar a contagem é enorme.

# Parte 2 - Organização dos Documentos**

## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária**
### 2.1 Descrição e Especificação dos Arquivos**
* **Tipos de arquivo:**
* **Markdown (`.md`) e Word (`.docx`):** Os relatórios, pareceres e anotações internas da equipe sobre os livros.
* **EPUB (`.epub`) e PDF (`.pdf`):** O texto dos livros inteiros, amostras de capítulos ou rascunhos enviados pelos autores.
* **JSON (`.json`):** As fichas técnicas dos livros com dados fixos (como ISBN, autor, gênero e prêmios).
* **Volume aproximado:**
* **Muitos milhares de arquivos:** Uma editora média/grande costuma ter de **2.000 a 5.000 livros publicados** e uns **10.000 a 15.000 relatórios** guardados (contando os livros aprovados e os que foram recusados).
* **Tamanho de cada arquivo:**
* **Relatórios e Pareceres (`.md` / `.docx`):** Textos curtos de **2 a 5 páginas** (uns 20 KB a 80 KB).
* **Livros e Manuscritos (`.epub` / `.pdf`):** Textos longos de **150 a 500 páginas** (de 500 KB a 10 MB, se tiver ilustrações).
* **Fichas Técnicas (`.json`):** Arquivos bem levinhos (de 5 KB a 20 KB).
* **Frequência de entrada e atualização:**
* **Entrada de novos arquivos:** Chegam toda semana ou todo mês (com novos rascunhos para avaliar e cerca de 5 a 20 lançamentos de livros por mês).
* **Atualização:** Livro pronto quase não muda (só se sair uma edição nova). Os relatórios da equipe mudam um pouco se o autor reescrever partes do texto antes de lançar.

## Proposta da Estrutura de Pastas**
```
acervo_editorial/
├── catalogo_publicado/
│   ├── ficcao/
│   │   └── romance/
│   │       └── 9788535900001_a_hora_da_estrela/
│   │           ├── texto_integral.epub
│   │           ├── ficha_catalografica.json
│   │           └── parecer_editorial_v1.md
│   └── nao_ficcao/
├── manuscritos_em_avaliacao/
│   └── 2026/
│       └── reader_reports/
└── metadados_gerais/

```
## Justificativa da Estrutura:**
A gente dividiu as pastas por **Status do livro -> Gênero -> Subgênero -> Pasta da obra** para ficar fácil de organizar o trabalho e não dar confusão na busca:
1. **Separar o que tá publicado do que ainda é rascunho:**
Isso serve para o sistema não dar mancada e indicar para um leitor comum no aplicativo um livro que nem foi lançado ainda ou que a gente nem comprou os direitos.
2. **Organizar por gênero e subgênero:**
É a divisão normal de qualquer livraria. Ajuda o sistema a descobrir o gênero do livro sozinho, só de olhar o caminho da pasta onde ele tá guardado.
3. **Deixar tudo do mesmo livro no mesmo lugar:**
Junta o texto do livro, o relatório da equipe e a ficha com os dados numa pasta só. Assim a gente não corre o risco de misturar a análise de um livro com a história de outro.

### 2.3 Respostas às Perguntas de Gestão e Segurança

#### Existe documento que NÃO deve entrar na base? Como você impediria a entrada?
* **O que não pode entrar de jeito nenhum:** Contratos, dados de vendas e pagamentos dos autores, informações pessoais (CPF, telefone, conta bancária) e anotações soltas ou rascunhos sem aprovação.
* **Como barrar isso:**
* O sistema só aceita ler arquivos que estejam dentro das pastas oficiais.
* Ele ignora sozinho qualquer arquivo marcado com "rascunho" ou "sigiloso".
* Usa um rastreador automático para barrar arquivos que tenham números de CPF, e-mail ou dados de banco.
#### Como você lidaria com VERSÕES do mesmo documento?
* **O problema:** O autor muda a história do livro e manda a Versão 2. Se o sistema puxar a Versão 1, vai falar de um personagem ou final que nem existe mais.
* **Como resolver:**
* Cada arquivo ganha um "carimbo" avisando o número da versão e se ele é o documento atualizado.
* Quando entra a Versão 2, o sistema marca a Versão 1 como "ultrapassada".
* A busca é travada para olhar sempre só a versão mais recente, a não ser que o editor peça para comparar com o rascunho antigo.

# Parte 3 - Pipeline de Ingestão**

## Parte 3.1 - Detalhamento da Extração de Documentos**

### 1. Estratégia Geral de Extração por Formato**
A ideia é abrir qualquer arquivo de livro ou relatório e transformar tudo em um texto limpo e organizado:
* **Livros Digitais (`.epub`):** Usamos programas leitores (como `ebooklib` e `BeautifulSoup4`) para ler a estrutura do livro e transformar os capítulos e parágrafos em texto comum.
* **Relatórios e Anotações (`.docx`, `.md`):** Lemos o arquivo do Word com uma ferramenta (`python-docx`) para organizar os títulos. Nos arquivos Markdown, a gente separa o texto do relatório das informações da ficha do livro.
---
**2. Tratamento de PDFs com Texto Selecionável**
Para ler os PDFs normais de livros e rascunhos, a gente usa uma ferramenta chamada `pdfplumber`:
* **Para não misturar o texto:** Ele analisa o visual da folha para não juntar por engano o texto de colunas diferentes (tipo em edições de revistas literárias).
* **Para achar os capítulos:** O leitor repara no tamanho e no peso da letra para descobrir o que é título de capítulo e o que é texto comum.
---
**3. Tratamento de PDFs Digitalizados (Escaneados / Sem Camada de Texto)**
Quando o arquivo é só uma imagem escaneada de um papel ou de um livro bem antigo:
1. **Checagem inicial:** O sistema conta as letras da página. Se não achar texto de verdade, ele entende que a folha é só uma foto.
2. **Leitores de foto (OCR):**
* **Jeito padrão (para muitos arquivos):** Melhora a qualidade da imagem e usa um leitor automático (`Tesseract`) em português.
* **Para textos difíceis ou manuscritos:** Manda a foto direto para uma IA com visão (como `GPT-4o` ou `Claude`) para ela "olhar" a imagem e digitar o texto organizado para a gente.

### Tratamento de Tabelas

**É fundamental manter a estrutura das tabelas.** No ambiente editorial, tabelas aparecem em fichas catalográficas, cronogramas de lançamentos e tabelas comparativas de vendas/público nos *reader reports*.
* **Extração:** `pdfplumber` identifica as linhas e colunas de grade da tabela.
* **Conversão:** A tabela extraída é convertida para **Markdown Table** ou um objeto **JSON inline** dentro do texto do *chunk*:
```
| Parâmetro | Avaliação do Parecerista |
| :--- | :--- |
| Ritmo de Leitura | Rápido / Flutuante |
| Público-Alvo | Jovem Adulto (16-24 anos) |
| Potencial Comercial | Alto |
```
* **Justificativa:** Representar tabelas como texto puro desalinhado faz com que o LLM perca a associação entre chave e valor (ex: associar "Ritmo de Leitura" à nota "Alto" em vez de "Rápido").

### Tratamento de Imagens e Capas**
* **Desenhos e enfeites do livro:** A gente simplesmente joga fora, porque só servem para enfeitar e atrapalham o sistema.
* **Capas e desenhos da história:** Uma IA de visão "olha" a imagem da capa e digita uma explicação em texto (descrevendo o clima, as cores e os elementos). Esse resumo fica salvo junto com as informações do livro.
---
### Documentos com Áudio e Vídeo**
* **Áudios (entrevistas e audiolivros):** Passam por uma IA de voz (tipo o *Whisper*) que ouve tudo e transforma a fala em texto digitado.
* **Vídeos (trailers de livros e gravações):** O sistema tira o áudio do vídeo para virar texto e pega algumas fotos da tela para a IA descrever como é o visual da propaganda.
---
### Problemas Comuns e Exemplo de Erro**
* **Chateações normais de arrumar:**
* Palavras cortadas no fim da linha (tipo `recomen-` e `dação`).
* Sujeiras de escaneamento em folhas amareladas que viram letras estranhas.
* O título do capítulo repetido no topo das páginas ficando preso no meio das frases.
* **Erro real que aconteceu na prática:**
Ao tentar ler uma página dividida em duas colunas, o leitor de PDF leu a folha de fora a fora na horizontal. Ele juntou a primeira linha da coluna da esquerda com a primeira linha da coluna da direita, criando uma frase maluca misturando a história do livro com números do mercado editorial.
* **Como resolveu:** Trocamos a ferramenta por uma que consegue "enxergar" os blocos da página, forçando a leitura de toda a coluna da esquerda antes de ir para a da direita.
#### O que precisa ser removido?
* **Cabeçalhos, Rodapés e Páginas Repetidas:** Títulos de topo, nome do autor no rodapé, números de página soltos e marcas d'água de segurança (como *"RASCUNHO CONFIDENCIAL"*).
* **Páginas sem Conteúdo Relevante:** Folhas em branco, fichas de licença gráfica, avisos de marca registrada e listas de agradecimentos comerciais.
* **Sumários e Índices Numéricos:** Listas estáticas de capítulos ligadas a números de página (ex: *"Capítulo 1 ............ pág 12"*), que perdem o sentido ao cortar o texto.
* **Sujeira de Leitura (OCR):** Símbolos estranhos de páginas escaneadas, traços de borda e códigos de formatação de computador.
---
#### O que precisa ser padronizado?
* **Formato de Arquivo e Acentos (UTF-8):** Garantir que 100% dos textos fiquem no formato UTF-8 para não quebrar acentos, cedilhas ou nomes próprios de autores estrangeiros.
* **Pontuação Literária e Diálogos:** Deixar aspas, reticências e travessões de fala todos no mesmo padrão para a IA entender fácil as conversas dos personagens.
* **Palavras Cortadas no Fim da Linha:** Juntar palavras divididas por hífen na virada de página (transformando `"recomen- dação"` em `"recomendação"`).
* **Espaços e Parágrafos:** Tirar espaços duplos e quebras de linha artificiais do PDF, mantendo apenas a separação limpa entre um parágrafo e outro (`\n\n`).

#### Informações em Risco de Perda por Sobre-limpeza
* **Troca de Cenas e Ritmo da História:** Mudanças de cenário ou saltos no tempo costumam ser marcados por asteriscos (`* * *`) ou linhas em branco. Se o limpador apagar isso achando que é espaço à toa, o sistema vai misturar duas cenas diferentes no mesmo pedaço de texto.
* **Estilo e Voz do Autor:** Certos autores escrevem sem pontuação, usam palavras inventadas ou escrevem tudo em letra minúscula de propósito. Corrigir essa gramática apaga o estilo do livro e impede a IA de avaliar o tom da obra.
* **Notas de Rodapé Importantes:** Em biografias e livros históricos, as notas do tradutor e do editor explicam o contexto do texto. Se apagar as notas na limpeza, a IA perde explicações essenciais sobre termos antigos e eventos da história.
* **Confusão nos Diálogos:** Apagar anotações de margem ou divisores pode fazer o sistema se perder em conversas curtas, fazendo a IA atribuir a fala do texto para o personagem errado.
---
####  Detalhamento da Frequência de Ingestão e Ciclo de Vida
#### Como o pipeline roda e com que frequência chegam novos documentos?
* **Modo de Execução:** Ele funciona de forma **mista: no momento em que o arquivo chega e em horários programados**.
1. **Na Hora (Aviso Automático):** Quando alguém envia um relatório novo ou a versão final de um livro para a pasta da editora, o sistema percebe sozinho e processa aquele arquivo imediatamente.
2. **De Madrugada (Agendado):** Todo dia às 2h da manhã, roda um processo automático para atualizar preços, novos códigos de livros (ISBN) e conferir se nenhum documento ficou para trás.
* **Frequência de Chegada dos Documentos:**
* **Relatórios e Avaliações:** Chegam em fluxo contínuo, de 15 a 30 relatórios novos por semana.
* **Livros Lançados:** Entram de 5 a 20 títulos finalizados por mês, seguindo o plano de lançamentos da editora.

#### Reprocessamento: Apenas o documento atualizado ou a base inteira?
* **Estratégia Escolhida:** Processar **só o arquivo que mudou (Incremental)**.
* **Por que não reprocessar tudo?** Reler milhares de livros e recalcular os códigos da IA toda vez que um único relatório muda gastaria uma fortuna com chamadas de API e deixaria a busca lenta sem necessidade.
---
#### Como o sistema sabe qual documento reprocessar?
Ele usa uma espécie de "impressão digital" do arquivo (chamada **Hash SHA-256**) e uma lista de controle para comparar:
1. **Gera a impressão digital do texto:** Quando o sistema lê o arquivo, ele cria um código único baseado no conteúdo exato dele.
2. **Confera na lista de controle:**
* **Arquivo Novo:** Roda a leitura completa e salva os dados novos na IA.
* **Arquivo Igual:** O sistema vê que o código é idêntico e ignora o arquivo para não gastar processamento.
* **Arquivo Alterado (mesmo livro, mas com texto modificado):** O sistema apaga do banco de dados os trechos antigos daquele livro, lê a versão nova e salva os trechos atualizados no lugar.

---

#### 4.1 Metadados do Documento
Estes dados registram a obra por completo no momento em que ela entra no sistema, permitindo isolar livros por público, gênero ou validade de contrato.

```json
{
  "document_id": "doc_isbn_9788532511010_v1",
  "title": "Harry Potter e a Pedra Filosofal",
  "author": "J.K. Rowling",
  "source": "acervo_editorial/catalogo_publicado/ficcao/fantasia/9788532511010_hp_pedra_filosofal/texto_integral.epub",
  "document_type": "livro_integral",
  "created_at": "2026-02-10T08:00:00Z",
  "updated_at": "2026-02-10T08:00:00Z",
  "category": "catalogo_publicado",
  "isbn": "9788532511010",
  "genero_principal": "Fantasia",
  "subgeneros": ["Fantasia Juvenil", "Aventura", "Magia"],
  "ordem_serie": 1,
  "nome_serie": "Harry Potter",
  "ano_publicacao": 1997,
  "idioma_original": "en-GB",
  "tradutor": "Lya Wyler",
  "status_direitos": "ativo",
  "publico_alvo": "Infantojuvenil",
  "is_latest": true,
  "nivel_acesso": "publico_geral"
}

```
* **Identificação e Controle (`document_id`, `title`, `author`, `source`, `document_type`, etc.):** Mantêm o histórico do arquivo e garantem que o sistema consiga atualizar ou apagar a obra correta no banco.
* **Código Comercial (`isbn`):** Permite cruzar os dados do livro com os sistemas de vendas, estoque e contratos da editora.
* **Classificação Literária (`genero_principal` e `subgeneros`):** Permitem filtrar o acervo por categorias amplas (*"Fantasia"*) ou específicas (*"Magia"*).
* **Cronologia da Saga (`ordem_serie` e `nome_serie`):** Garantem que a IA entenda a ordem dos livros, evitando dar *spoilers* de volumes futuros.
* **Origem e Tradução (`ano_publicacao`, `idioma_original` e `tradutor`):** Identificam o ano de lançamento e a versão em português. O tradutor é crucial para manter a consistência de termos adaptados (como *Quadribol* ou *Sonserina*).
* **Regras de Negócio e Segurança (`status_direitos`, `publico_alvo`, `is_latest` e `nivel_acesso`):**
* `status_direitos`: Impede a recomendação de livros cujos contratos de publicação já venceram.
* `publico_alvo`: Garante recomendações adequadas para a faixa etária do leitor.
* `is_latest`: Força o sistema a consultar apenas a edição revisada mais recente.
* `nivel_acesso`: Controla quem pode ver a obra (liberando para o público final no app ou restringindo para uso interno da editora).
---

#### 4.2 Metadados do Chunk (Ficha do Pedaço de Texto)
Anexados diretamente a cada bloco de texto recortado do livro, esses dados ajudam a IA a localizar cenas específicas por clima, personagens ou temas abordados.

```json
{
  "document_id": "doc_isbn_9788532511010_v1",
  "chunk_id": "doc_isbn_9788532511010_v1-c87",
  "chunk_index": 87,
  "page": 108,
  "section": "Capítulo 7: O Chapéu Seletor",
  "document_type": "livro_integral",
  "nome_serie": "Harry Potter",
  "ordem_serie": 1,
  "genero_principal": "Fantasia",
  "publico_alvo": "Infantojuvenil",
  "temas_chave": ["Rito de passagem", "Pertencimento", "Casas de Hogwarts", "Escolha do Chapéu"],
  "elementos_mágicos": ["Chapéu Seletor", "Gryffindor", "Slytherin", "Hogwarts"],
  "tom_narrativo": "Mágico, Misterioso, Tensão Juvenil",
  "is_latest": true,
  "nivel_acesso": "publico_geral",
  "text": "— Gryffindor! — gritou o chapéu para o salão. A mesa da extrema esquerda explodiu em vivas e palmas. Harry viu os irmãos de Rony de pé assobiando enquanto o garoto caminhava até eles com as pernas trêmulas."
}

```
* **Localização Exata (`document_id`, `chunk_id`, `chunk_index`):** Identificam a qual livro o pedaço pertence e qual é a sua posição na história, permitindo puxar os trechos vizinhos para reconstruir cenas longas sem cortar o contexto.
* **Referência da Origem (`page`, `section`, `document_type`):** Registram o capítulo e o número da página física para citação precisa, além de separar o texto do livro das opiniões de pareceristas.
* **Filtros Rápidos (`nome_serie`, `ordem_serie`, `genero_principal`, `publico_alvo`):** Herdado do documento original para permitir buscas rápidas sem precisar ler a obra inteira.
* **Análise do Conteúdo do Trecho:**
* `temas_chave`: Assuntos centrais da cena (ex: *Pertencimento*, *Rito de passagem*).
* `elementos_mágicos`: Objetos, casas ou locais citados no trecho (ex: *Chapéu Seletor*, *Gryffindor*).
* `tom_narrativo`: A atmosfera emocional do momento (ex: *Mágico*, *Tensão Juvenil*).
* **Segurança da Resposta (`is_latest` e `nivel_acesso`):** Asseguram que a busca recupere apenas trechos homologados e dentro da permissão de acesso do usuário.

### Respostas às Perguntas do Projeto

#### Quais metadados você usaria para filtrar a busca? Dê um exemplo de pergunta em que o filtro é indispensável.
* **Metadados de Filtro:** `nome_serie`, `ordem_serie`, `publico_alvo`, `genero_principal`, `document_type`, `is_latest` e `nivel_acesso`.
* **Exemplo de Pergunta:**
> *"No primeiro livro de Harry Potter, em qual cena o protagonista descobre a qual casa de Hogwarts ele pertence?"*
* **Por que o filtro é indispensável?**
Sem travar a busca em `nome_serie = "Harry Potter"`, `ordem_serie = 1` e `document_type = "livro_integral"`, a IA poderia puxar lembranças dessa cena nos livros 5 ou 7 (em conversas dos personagens) ou até relatórios internos da equipe analisando o capítulo. O filtro garante que a busca olhe **apenas** no texto original do Volume 1 (*A Pedra Filosofal*).

---
#### Quais metadados você usaria para citar a fonte ao usuário? O que exatamente apareceria na tela junto da resposta?
* **Metadados para Citação:** Nome do livro, autor, capítulo (`section`), número da página (`page`) e número do livro na série (`ordem_serie`).
* **O que aparece na tela do usuário:**
> **Resposta do Assistente:**
> *"Harry descobre sua casa durante a cerimônia do Chapéu Seletor, que fica em dúvida entre Sonserina e Grifinória, mas decide enviá-lo para a Grifinória após o garoto pedir para não ir para a Sonserina."*
> **Fonte Consultada:**
> * **Obra:** *Harry Potter e a Pedra Filosofal* (Volume 1) — J.K. Rowling
> * **Localização:** *Capítulo 7: O Chapéu Seletor* (Pág. 108)
> * **Tipo:** Texto Integral do Livro
---

#### Que metadado seria caríssimo de acrescentar depois que a base já estivesse indexada? Por quê?
* **Metadados Caríssimos:** **`temas_chave`**, **`elementos_mágicos`** e **`tom_narrativo`**.
* **Por quê?**
Descobrir o capítulo ou a página dá para fazer rapidinho com um código simples. Mas para preencher temas, elementos e o tom de cada pedaço, a gente teria que mandar **cada um dos milhares de trechos de volta para a IA analisar**. Só nos 7 livros da saga, seriam mais de 4.500 chamadas de API, o que custaria uma fortuna, demoraria horas e exigiria atualizar todo o banco de dados do zero.

---
#### Como você vai extrair esses metadados?
1. **Informações do Arquivo e da Pasta (Automático):** Nome do livro, autor, série, público-alvo e nível de acesso são puxados direto da pasta onde o livro está guardado.
2. **Leitura da Estrutura do Livro (`.epub`):** O nome do capítulo e a ordem do trecho são identificados lendo a própria formatação do arquivo digital.
3. **Análise de Texto por IA (Structured Output):** Cada pedaço de texto passa por uma IA mais barata (`gpt-4o-mini`), que lê o trecho e devolve a lista pronta com os temas, elementos mágicos e o tom da cena.

# Parte 5 - Chunking / Splitting

## Estratégia de Splitting Definida
#### Qual estratégia de splitting você utilizaria?
Usaremos uma **divisão recursiva baseada na estrutura do texto**. Para livros e relatórios, o corte não pode quebrar uma cena ou conversa ao meio. Por isso, o sistema respeita a divisão natural da história: capítulos primeiro, depois parágrafos e, por último, a pontuação dos diálogos.
#### Qual tamanho aproximado dos chunks?
* **Tamanho Alvo:** **1.000 a 1.200 caracteres** (cerca de 150 a 200 palavras).
* **Por que esse tamanho?** Em livros como *Harry Potter*, um parágrafo longo ou uma conversa rápida tem mais ou menos essa extensão. Esse tamanho é ideal para guardar a ideia completa de uma cena (como o Chapéu Seletor escolhendo a casa do Harry ou a primeira aula de poções) sem misturar com outros assuntos da história.
#### Utilizaria overlap (sobrinha entre os pedaços)? Quanto?
* **Sim, de 150 a 200 caracteres** (uns 15% a 20% do tamanho do pedaço).
* **Por que usar?** Em histórias, a continuação das conversas é importante. Essa "sobrinha" de texto garante que o começo de um pedaço repita o final do pedaço anterior, evitando cortar a resposta de um personagem ou o final de uma ação no meio.

#### A divisão seria por caracteres, palavras, sentenças, parágrafos ou seções?
A divisão segue uma **lista de prioridades**, tentando sempre manter os maiores blocos possíveis antes de cortar em partes menores:
1. **Primeira opção:** Cortar na troca de capítulos (`\n\nCapítulo`).
2. **Segunda opção:** Cortar na troca de parágrafos (`\n\n`).
3. **Terceira opção:** Cortar nas trocas de linhas das falas (`\n`).
4. **Quarta opção:** Cortar no ponto final ou pontuação (`. `, `! `, `? `).
5. **Último recurso:** Cortar nos espaços entre as palavras (` `).

#### Utilizaria um splitter recursivo?
**Sim.** Ele tenta cortar o texto usando a maior divisão possível (como parágrafos). Se o parágrafo for gigante e passar dos 1.200 caracteres, o próprio sistema tenta sozinho diminuir o corte para as frases, garantindo que nenhum pedaço fique maior do que o limite.

#### Utilizaria uma estratégia específica para cada tipo de documento? Um contrato e uma transcrição pedem o mesmo tratamento?
**Com certeza. Cada tipo de arquivo precisa de um corte totalmente diferente:**
* **Livros Literários (ex: *Harry Potter*):** Corte **por parágrafos e cenas** (1.000 a 1.200 caracteres), focado em não estragar a história.
* **Relatórios e Pareceres da Equipe:** Corte **por seções do documento**. Como o relatório já vem dividido em partes (ex: *"Resumo"*, *"Análise dos Personagens"*), o corte precisa manter cada parte inteira para não misturar opinião com resumo.
* **Contratos de Direitos Autorais:** Corte **por cláusulas do contrato**. Cortar uma regra contratual ao meio tira o sentido jurídico e faz a IA falar besteira sobre o documento.
* **Gravações de Reuniões / Atendimento:** Corte **por trocas de fala**. Cada pedaço agrupa a pergunta de uma pessoa e a resposta da outra, mantendo o sentido da conversa.

//
### Respostas às Perguntas do Projeto

#### O que pode acontecer se os chunks forem muito pequenos?
* **Perda de sentido:** Um pedaço muito curto (tipo só a frase *"— Sonserina não, eh?"*) fica sem contexto. A IA não consegue saber quem falou, onde a pessoa estava nem sobre o que era a conversa.
* **Busca confusa:** O código que a IA gera para esse trecho fica muito genérico, fazendo o sistema trazer resultados errados que não têm nada a ver com a pergunta.
* **Resposta fraca:** Como a IA só recebe pedaços soltos e sem história, ela fica incapaz de dar uma resposta completa e bem explicada sobre o livro.
---
#### O que pode acontecer se os chunks forem muito grandes?
* **A informação se perde (efeito "agulha no paliteiro"):** Se o pedaço tiver um capítulo inteiro de 20 páginas, a IA faz uma média geral de todo o assunto. Se você perguntar por um detalhe pequeno (como o nome do sapo do Neville), o sistema não vai achar porque o detalhe ficou escondido no meio de milhares de palavras.
* **Fica caro e lento:** Mandar blocos gigantescos de texto para a IA ler consome muita memória, demora mais para responder e deixa a conta da API bem mais alta.
* **Citação ruim:** Na hora de mostrar para o usuário de onde tirou a informação, o sistema vai indicar um texto gigante em vez de apontar para a cena exata do livro.
---
#### Como você trataria uma tabela na hora de dividir? Uma tabela cortada ao meio ainda significa alguma coisa? E uma imagem?
* **Tratamento de Tabelas:**
* Cortar uma tabela ao meio faz ela perder todo o sentido, porque as linhas de baixo ficam sem saber a qual cabeçalho pertencem.
* **Como resolver:** A gente transforma a tabela em texto organizado (Markdown) e tenta guardar a tabela inteira num pedaço só sem cortar. Se ela for gigante e precisar ser dividida de qualquer jeito, o sistema repete a linha do topo (cabeçalho) em todas as partes cortadas para a IA não se perder.
* **Tratamento de Imagens e Ilustrações (capas, mapas de Hogwarts):**
* O sistema de busca por texto não consegue ler uma foto ou desenho puro em pixels.
* **Como resolver:** A gente passa a imagem por uma IA de visão para ela "olhar" e escrever um resumo em texto sobre o desenho (descrevendo, por exemplo, o Mapa do Maroto ou a capa). Esse resumo em texto é salvo no sistema junto com o link da imagem original. Assim, quando o leitor fizer uma pergunta sobre a cena, o sistema consegue achar o texto e mostrar o desenho na tela.

//
### Como saber se a sua escolha de chunking foi boa? Que evidência você juntaria para provar isso?
Para provar que a divisão do texto funcionou, a melhor abordagem é combinar **métricas numéricas de busca** com **testes práticos usando perguntas reais** (utilizando ferramentas de avaliação de RAG, como Ragas ou TruLens).
#### Métricas Numéricas de Busca (Avaliação do Retrieval)
* **Taxa de Acerto (*Recall@K / Hit Rate*):** Mede com que frequência o trecho exato que contém a resposta aparece entre os primeiros resultados trazidos pela busca. Um bom chunking deve manter essa taxa acima de 90% nos primeiros 5 resultados (*Recall@5*).
* **Precisão de Contexto (*Context Precision*):** Avalia a proporção de texto útil em relação ao texto irrelevante que vem junto no bloco. Chunks bem ajustados entregam muita informação relevante sem "palha".
* **Primeira Posição (*MRR - Mean Reciprocal Rank*):** Mede se o pedaço mais importante da história aparece logo no topo da lista de busca vetorial.
---
#### Testes de Estresse com um Banco de Perguntas Reais (*Golden Dataset*)
Criaríamos um conjunto de teste com cerca de 100 perguntas representativas do acervo de *Harry Potter*, divididas em três tipos de busca:
* **Perguntas Fatuais e Pontuais:** *"Qual o número da plataforma de trem em King's Cross?"* (Garante que detalhes pequenos não foram diluídos no meio do texto).
* **Perguntas de Diálogo e Cena:** *"O que Dumbledore disse a Harry em frente ao Espelho de Ojesed?"* (Confirma que a troca de falas entre os personagens não foi cortada ao meio).
* **Perguntas Temáticas ou Gerais:** *"Como é descrita a atmosfera da casa Sonserina ao longo do primeiro livro?"* (Garante que os pedaços recuperados cobrem bem o tema sem trazer textos fora de contexto).
---
#### Prova de Ausência de Cortes na Informação 
Monitoraríamos as respostas da IA para identificar com que frequência ela emite avisos como *"o texto não informa o final porque a frase foi cortada"*.
Manter uma taxa de falha de borda próxima de **0%** é a evidência definitiva de que a escolha do tamanho do bloco e a "sobrinha" de texto (*overlap*) foram configuradas na medida certa.

# Parte 6 - Embeddings**
Para montar o sistema da editora (tanto a parte de sugerir livros para os leitores quanto o painel interno de análise de manuscritos e da saga *Harry Potter*), a gente resolveu dividir a ideia em duas frentes: **Cenário A (Aberto ao público/Recomendações)** e **Cenário B (Interno/Para manuscritos secretos)**.

---

### Tabela Comparativa dos Modelos
| Item | Cenário A: Recomendação (Público) | Cenário B: Manuscritos e Sigilo (Interno) |
| --- | --- | --- |
| **Modelo escolhido** | **text-embedding-3-large** (OpenAI) | **multilingual-e5-large** (Microsoft) |
| **Tamanho do código (Dimensão)** | 3.072 (dá para diminuir para 1.536 ou 256) | 1.024 |
| **Entende português?** | Sim, funciona super bem | Sim, muito bom em PT-BR |
| **Funciona em vários idiomas?** | Sim | Sim (aceita mais de 100 línguas) |
| **Limite de texto de uma vez** | Bastante texto (~8.000 tokens) | Pedaços menores (~512 tokens / 1.500 caracteres) |
| **É código aberto (Open Source)?** | Não, é pago e fechado | Sim, código livre |
| **Dá para rodar no nosso computador?** | Não, precisa da internet | Sim, dá para instalar na nossa máquina |
| **Tem API pronta?** | Sim, direto da OpenAI | Sim, ou a gente mesmo cria a nossa |
| **Custo aproximado** | US$ 0,00013 a cada 1.000 tokens | Grátis (só paga o computador para rodar) |
| **Onde achar (Link)** | [Doc OpenAI](https://platform.openai.com/docs/guides/embeddings) | [Hugging Face](https://huggingface.co/intfloat/multilingual-e5-large) |

### Por que a gente escolheu cada um?
* **Cenário A (`text-embedding-3-large`):**
Achei uma boa para a parte do aplicativo aberto ao público. Ele parece entender super bem o estilo dos livros, o clima das histórias de *Harry Potter* e do nosso catálogo em português. Uma coisa bem legal dele é que dá para diminuir o tamanho dos dados para economizar espaço e dinheiro no banco de dados sem o sistema ficar burro.
* **Cenário B (`multilingual-e5-large`):**
Esse aqui encaixa perfeito para as coisas secretas da editora, tipo os livros que nem lançaram ainda. Como ele é de graça e dá para baixar e rodar num computador próprio da empresa, a gente não corre o risco de vazar a história de um autor inédito na internet ou ter problemas com a lei de dados (LGPD). Além disso, ele é bem famoso por ser bom em buscas em português.

### Respostas às Perguntas do Projeto

#### Considerou algum modelo alternativo e descartou? Qual, e por quê?
* **Modelos testados:** `text-embedding-ada-002` (OpenAI) e `bge-large-en-v1.5` (BAAI).
* **Por que foram descartados:**
* O `ada-002` é uma versão mais antiga da OpenAI. Ele é pior para entender o português e não deixa a gente diminuir o tamanho do código para economizar espaço no banco.
* O `bge-large-en` é focado quase que 100% em inglês. Quando a gente testou com coisas em português do Brasil (tipo gírias ou o jeito que os livros de *Harry Potter* foram traduzidos), ele deu uma engasgada e perdeu a precisão.
#### Se o cenário envolve documentos sigilosos, isso muda sua escolha entre modelo local e API? Como?
* **Sim, muda tudo.**
* **Na prática:** Livro que nem foi lançado ainda e contrato de autor são coisas muito secretas. Se vazar, a editora perde dinheiro e toma processo.
* Por isso, no **Cenário B**, a gente **proibiu usar APIs de fora** (como a da OpenAI). Escolhemos rodar um modelo próprio dentro do computador da empresa (`multilingual-e5-large`). Assim, o texto do livro nunca sai da nossa rede interna e ninguém de fora consegue bisbilhotar nem usar a história para treinar outras IAs.

#### O tamanho máximo de entrada do modelo tem relação com a sua decisão de chunking da Parte 5? Explique.
* **Sim, totalmente.** O tamanho do pedaço de texto não pode passar do limite que o modelo consegue ler de uma vez só.
* **Como funciona na prática:**
* No **Cenário A** (OpenAI), o modelo lê blocos gigantes de até 8.000 palavras, então nosso pedaço de 1.200 caracteres entra rindo.
* No **Cenário B** (Microsoft local), o limite é bem menor: ele só lê até uns 1.500 a 2.000 caracteres por vez.
* **Conclusão:** A escolha que a gente fez na Parte 5 de cortar o texto em blocos de **1.000 a 1.200 caracteres** foi pensada nisso. Ficou no tamanho perfeito para caber no modelo menor sem que ele precise "degolar" o final das frases por falta de espaço.

///////////////////////////////////////////Comparação////////////////////////////////////////////////////////////////////////////////
### Comparação entre os Dois Cenários
A tabela a seguir coloca lado a lado as escolhas feitas para o **Cenário A (Aplicativo de Recomendação Literária — Público Geral)** e o **Cenário B (Avaliação Editorial e Manuscritos Sigilosos — Interno)**, mostrando onde as arquiteturas se distanciam e o motivo de cada decisão.
---
#### Em que pontos as decisões foram diferentes? Por quê?
| Etapa | Cenário A (Público / Recomendação) | Cenário B (Interno / Manuscritos) | Por que são diferentes? |
| --- | --- | --- | --- |
| **Onde o sistema roda** | Na nuvem (usando serviços e APIs prontas da OpenAI) | No computador da empresa (rede interna e servidores próprios) | **Segurança e Sigilo:** O Cenário B lida com livros que nem foram lançados. Nenhum texto secreto pode sair da empresa ou ir para a internet. |
| **Modelo de Embeddings** | `text-embedding-3-large` (Pago / OpenAI) | `multilingual-e5-large` (Gratuito / Instalado na empresa) | **Qualidade de Recomendação vs. Privacidade:** O público precisa da melhor inteligência para achar livros por estilo; a equipe interna precisa de proteção total contra vazamentos. |
| **Tamanho dos Cortes (Chunking)** | Blocos de 1.000 a 1.200 caracteres (foco em cenas e conversas) | Blocos de 800 a 1.000 caracteres (foco em tópicos e relatórios) | **Tipo de Texto:** Livros de histórias têm parágrafos longos que precisam de espaço; relatórios de pareceristas têm tópicos técnicos curtos. |
| **Uso dos Metadados** | Para achar livros por estilo (`publico_alvo`, `temas_chave`, `genero_principal`) | Para controlar quem pode ler (`nivel_acesso`, `status_direitos`, `autor_pseudonimo`) | **Objetivo do Usuário:** O leitor quer achar uma história legal; o editor precisa saber se o documento é confidencial e quem tem permissão de ver. |

#### Em que pontos foram iguais? Isso é sinal de boa prática geral ou de repetição sem pensar?
As duas frentes compartilham quatro pontos principais na estrutura:
1. **Corte de texto inteligente e recursivo (`RecursiveCharacterTextSplitter`)**
2. **Uso de "sobrinhas" entre os blocos de texto (*Overlap* de 150 a 200 caracteres)**
3. **Busca Híbrida (Misturar busca por código de IA com busca por palavras-chave exatas)**
4. **Uso de fichas de dados bem completas (Metadados ricos)**
#### Análise: Boa prática geral ou repetição sem pensar?
Isso é **sinal de boa prática geral**, e não uma cópia sem reflexão. Os motivos para manter essa base nos dois lados são:
* **Evitar frases cortadas pela metade:** Cortar o texto no meio de uma frase é ruim tanto para um diálogo de *Harry Potter* quanto para uma análise técnica de um editor. A "sobrinha" de texto (*overlap*) e o corte recursivo funcionam como uma garantia para não perder o sentido das coisas em nenhum tipo de arquivo.
* **Achar nomes inventados e termos específicos (Busca Híbrida):** A busca por inteligência artificial é ótima para entender ideias (como *"livro sobre escola de magia"*), mas costuma falhar com palavras inventadas. Juntar isso com a busca por palavras-chave tradicionais (BM25) é obrigatório para o sistema achar termos do mundo bruxo como *"Horcrux"*, *"Dementador"* ou nomes próprios de autores sem se confundir.
* **Não gastar energia à toa (Filtro por Metadados):** Filtrar as coisas antes de rodar a busca (garantindo, por exemplo, que o sistema só olhe arquivos marcados como `is_latest: true`) evita que o banco perca tempo vasculhando milhares de documentos velhos. É uma regra de ouro para qualquer sistema de busca rápido e bem feito.

#### Se você tivesse que construir apenas um dos dois, qual escolheria, e por quê?
### Escolha:** **Cenário B (Sistema Interno de Avaliação Editorial e Gestão de Manuscritos)**
#### Justificativa do Negócio e de Engenharia:
1. **Maior Retorno Financeiro e Defesa do Negócio (ROI):**
Descobrir um livro sucesso de vendas ou rejeitar uma obra ruim é o que faz uma editora dar lucro ou prejuízo. Um erro aqui custa caríssimo. Ter uma IA ajudando o time de editores economiza mais da metade do tempo de leitura e garante que nenhum bom livro passe despercebido.
2. **Desafio de Engenharia de IA Mais Seguro:**
O Cenário B resolve o maior pesadelo das empresas hoje: como usar inteligência artificial mantendo **100% de privacidade**. Criar um sistema rodando dentro da própria empresa, sem enviar nada para fora, gera um conhecimento valiosíssimo que fica guardado como patrimônio da editora.
3. **Testar em Casa Antes de Mostrar para o Cliente:**
Fazer o sistema interno primeiro permite testar a ferramenta com quem entende do assunto (os próprios editores). Depois que tudo estiver funcionando perfeitamente sem erros, fica muito mais fácil e seguro criar o aplicativo do leitor (Cenário A).
### Referências e Documentações Técnicas
* **Modelos e APIs de Embeddings:**
* [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings) (`text-embedding-3-large`)
* [Hugging Face - intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) (Modelo Open Source Local)
* **Bancos de Dados Vetoriais:**
* [Qdrant Documentation](https://qdrant.tech/documentation/) (Vector Search Engine)
* [ChromaDB Documentation](https://docs.trychroma.com/) (Open-source Vector Database)
* **Ferramentas de Extração, Processamento e Chunking:**
* [LangChain - RecursiveCharacterTextSplitter](https://www.google.com/search?q=https://python.langchain.com/docs/modules/data_connection/document_transformers/)
* [pdfplumber GitHub Repository](https://github.com/jsvine/pdfplumber) (Extração estruturada de PDFs)
* [EbookLib Documentation](https://www.google.com/search?q=https://ebooklib.readthedocs.io/) (Parsing de arquivos EPUB)


### Seção de Referências e Fontes Técnicas

* **Modelos de Embeddings da OpenAI (`text-embedding-3-large`):**
* [OpenAI Embeddings Guide & API Documentation](https://platform.openai.com/docs/guides/embeddings)

* **Modelo de Embeddings Open-Source (`multilingual-e5-large`):**
* [Hugging Face Model Card — intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)

* **Banco de Dados Vetorial (Qdrant Vector Database):**
* [Qdrant Documentation & Filtering Features](https://qdrant.tech/documentation/)

* **Modelos de Re-ranking (Cohere Rerank v3):**
* [Cohere Rerank Documentation](https://docs.cohere.com/docs/rerank-2)

* **Estrutura e Bibliotecas de Parsing de Documentos:**
* [EbookLib Documentation (EPUB Extraction)](https://www.google.com/search?q=https://docs.pypi.org/project/EbookLib/)
* [pdfplumber GitHub Repository & Documentation](https://github.com/jsvine/pdfplumber)
* [BeautifulSoup4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

* **Frameworks de Avaliação de RAG (Ragas & TruLens):**
* [Ragas Evaluation Framework Documentation](https://docs.ragas.io/)
* [TruLens RAG Triad Documentation](https://www.trulens.org/)

# Como você usou IA para te apoiar nessa atividade? Quais ferramentas? Como você avaliou e verificou a resposta dela? 
Usei IA para dados e termos que eu não tinha conhecimento, estruturação do arquivo md, informações adicionais relevantes, revisão e pesquisa.