# Parte 1 - Identificação dos Problemas

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 1.1 Descrição do Problema

#### Qual é o problema que você deseja resolver?
Em uma temporada regular da NBA, cada time joga 82 partidas em um ritmo insano, muitas vezes com jogos em dias seguidos (*back-to-back*) e viagens longas. A comissão técnica gera um volume enorme de relatórios e anotações sobre os adversários, mas os treinadores e analistas não têm tempo para re-ler arquivos de 30 páginas para achar uma resposta rápida antes de entrar em quadra. O problema é a dificuldade de extrair dados táticos específicos, atualizados e confiáveis em poucos segundos.

#### Quem utilizaria a aplicação?
* **Cargo:** Assistente Técnico (*Assistant Coach*), Coordenador de Vídeo (*Video Coordinator*) e Analista de Desempenho (*Scouting Analyst*).
* **Contexto de uso:** No vestiário antes do jogo, no hotel durante a preparação da partida ou na beira da quadra (*bench*) entre os quartos do jogo, ajustando o plano tático no tablet.
* **Nível técnico:** Domínio absoluto de basquete e estratégia tática, mas nível básico a intermediário em tecnologia. Precisam fazer perguntas em linguagem natural e receber respostas imediatas sem depender de comandos complexos.

#### Que tipo de informação o usuário gostaria de consultar?
* Tendências de esquemas defensivos e ofensivos dos adversários (ex: como reagem a dobras, se usam *Drop Coverage* ou troca de marcação no *Pick and Roll*).
* Preferências e hábitos de jogadores específicos em situações de pressão (ex: direção da infiltração, arremessos da zona morta).
* Padrões de jogadas desenhadas para momentos decisivos (*clutch time*) ou saídas de fundo de quadra.
* Comparativo de mudanças na rotação do rival nos últimos 5 ou 10 jogos.

#### De onde vêm essas informações?
Os dados vêm dos relatórios internos da própria comissão técnica, arquivos Markdown/PDF exportados de softwares de análise de vídeo (como *Synergy Sports* e *Hudl*), anotações de olheiros e cadernos de jogadas (*playbooks*) digitais da equipe.

#### Por que utilizar um LLM sozinho não seria suficiente?
1. **Dados Privados e Estratégicos:** Relatórios de *scouting* são dados sigilosos da franquia. Um LLM público/comercial não tem acesso aos documentos internos do time.
2. **Falta de Atualização em Tempo Real:** Um modelo base não sabe que um rival trocou a forma de defender há três dias ou que um jogador titular entrou na lista de lesionados.
3. **Risco Crítico de Alucinação:** Se o LLM inventar que um arremessador prefere ir para a esquerda quando a tendência real dele é ir para a direita, a instrução passada ao atleta em quadra estará errada e pode custar o jogo.

#### Como o usuário vai utilizar o sistema?
Através de um **aplicativo web responsivo (Web App)** otimizado para navegação em **iPads/tablets**, que é a ferramenta que a comissão técnica já usa na beira da quadra e nas reuniões de vídeo.

---

### Perguntas Reais dos Usuários

1. *"Como o Minnesota tá defendendo o Pick and Roll no topo da chave quando o Edwards tá no banco?"*
2. *"Qual é a tendência do Tatum na infiltração quando ele recebe a dobra no lado esquerdo da quadra?"*
3. *"O Boston mudou alguma jogada de fundo de quadra em relação ao jogo do mês passado contra a gente?"*


### 1.2 Por que RAG?

#### Por que RAG é adequado para esse problema?
O RAG é a arquitetura perfeita para este cenário porque resolve três limitações centrais de um LLM puro: a **falta de dados privados**, a **defasagem temporal** e a **tendência a alucinar**. Ele permite conectar a capacidade de síntese e linguagem do modelo diretamente aos relatórios táticos atualizados da comissão técnica, funcionando como uma busca inteligente que fundamenta cada resposta em evidências reais antes de responder ao treinador.

#### Que tipo de conhecimento precisa ser fornecido ao modelo?
Precisa ser fornecido um conhecimento altamente especializado e proprietário, incluindo:
* Relatórios de *scouting* detalhados sobre times adversários e seus jogadores.
* Análises táticas de vídeo convertidas em texto (mapeamento de esquemas de *Pick and Roll*, dobras de marcação e rotações).
* Observações de pós-jogo feitas pelos analistas da própria franquia.
* Transcrições e resumos das reuniões internas de preparação tática.

#### Esse conhecimento muda com que frequência?
Muda com **frequência diária ou quase diária**. Na NBA, os jogos acontecem a cada 24 ou 48 horas. A cada nova partida disputada pela liga, novos dados de desempenho são gerados e as tendências dos adversários se alteram (por causa de lesões, trocas de jogadores ou ajustes táticos feitos pelos técnicos rivais).

#### Existe necessidade de utilizar documentos privados ou específicos da organização?
**Sim, 100% dos documentos são privados e sigilosos.** Os relatórios de *scouting* são a vantagem competitiva da franquia e contêm estratégias confidenciais que não podem ser vazadas para outros times nem usadas para treinar modelos públicos.

#### Que problemas poderiam ocorrer se o LLM respondesse apenas com seu conhecimento pré-treinado?
O modelo responderia com base em estatísticas médias genéricas da internet, dados defasados de temporadas passadas ou, pior, inventaria padrões táticos convincentes mas completamente falsos (*alucinação*).

**Exemplo concreto de resposta errada:**
* **Pergunta do Assistente Técnico:** *"Como o Denver Nuggets está defendendo a dobra de marcação no topo da chave no segundo tempo?"*
* **Resposta de um LLM sem RAG (apenas pré-treino):** *"O Denver Nuggets costuma utilizar uma defesa em zona 2-3 para proteger o garrafão e forçar arremessos do perímetro, confiando na mobilidade de seus alas para fechar os espaços."*
* **Por que essa resposta é um desastre:** Na vida real, o Denver Nuggets roda uma defesa de homem-a-homem com o Nikola Jokić atuando em *Drop Coverage* ou *Show/Recover*, e quase nunca usa zona 2-3 como defesa principal. Se o treinador acreditasse nessa resposta da IA, desenharia um ataque contra zona e o time perderia posses de bola decisivas no jogo.


### 1.3 Limitações - Quando RAG Não É a Resposta

#### Em quais situações RAG não seria a melhor solução para esse problema?
O RAG é excelente para interpretação semântica e síntese de contexto não estruturado, mas é **péssimo para cálculos numéricos exatos, agregações quantitativas e filtros categóricos estritos sem margem para erro**. Se a necessidade da comissão técnica for extrair métricas exatas, contagens brutas de estatísticas ou regras táticas rígidas de "se/senão", confiar apenas no RAG (vetores + LLM) é um erro de arquitetura.

---

#### Análise das Alternativas Tecnológicas

* **Busca tradicional por palavra-chave (BM25 / Full-Text Search):**
  * *Quando supera o RAG:* Quando o treinador busca por códigos exatos de jogadas ou nomes próprios de termos táticos específicos (ex: `"Horns Flex 2"`, `"Spain PnR"` ou `"DHO"`). A busca vetorial por similaridade semântica pode se confundir com esses códigos curtos, enquanto a busca por palavra-chave entrega exatamente o documento com a correspondência literal.
* **Banco de dados estruturado e consultas SQL:**
  * *Quando supera o RAG:* Para qualquer tipo de dado quantitativo (ex: aproveitamento de arremessos, número de faltas, minutos em quadra). O banco relacional executa somas, médias e ordenações com precisão matemática perfeita em milissegundos, sem o risco de "chutar" valores como um LLM faz.
* **Regras determinísticas (If/Else):**
  * *Quando supera o RAG:* Para tomada de decisão de segurança e permissões do aplicativo (ex: *"Se o usuário for da imprensa, bloqueie o acesso aos relatórios do assistente técnico"*). Lógica de negócios e controle de acesso devem ser 100% determinísticos.
* **Combinação dessas técnicas com RAG (Solução Ideal / Hybrid Search + Text-to-SQL):**
  * A arquitetura ideal para a NBA não é o RAG isolado, mas sim um **RAG Híbrido**:
    1. **Busca Híbrida (BM25 + Vetores):** Combina termos exatos de jogadas com a busca semântica.
    2. **Text-to-SQL + RAG:** Perguntas numéricas são convertidas em consultas SQL direcionadas ao banco relacional de estatísticas oficiais, enquanto o RAG cuida da análise qualitativa dos relatórios de vídeo.

---

#### Qual pergunta do próprio cenário o RAG responderia mal e um banco relacional responderia bem?

* **Pergunta Exemplo:** *"Qual foi o aproveitamento de arremessos de 3 pontos do Jayson Tatum nos últimos 5 jogos da temporada contra defesas em zona?"*

* **Por que o RAG responderia mal?**
  Para responder a isso via RAG, o retriever precisaria recuperar dezenas de chunks picados, e o LLM teria que tentar extrair os números de cada texto, converter para float, somar os acertos, somar as tentativas e fazer uma divisão matemática. LLMs são modelos de linguagem probabilísticos e erram contas aritméticas básicas com facilidade, além de correrem o risco de omitir algum jogo por limitação da janela de contexto.

* **Por que o Banco Relacional responde bem?**
  Em um banco de dados estruturado (SQL), a tabela de *boxscores* já possui os campos organizados (`player_name`, `opponent`, `fg3_made`, `fg3_attempted`, `defensive_scheme`). O banco executa em 2 milissegundos:
  ```sql
  SELECT SUM(fg3_made) * 100.0 / SUM(fg3_attempted) AS pct
  FROM player_stats
  WHERE player_name = 'Jayson Tatum' AND zone_defense = TRUE
  ORDER BY game_date DESC LIMIT 5;

Aqui está a **Parte 2 - Organização dos documentos** no formato `.md`, mantendo a linguagem técnica, direta e totalmente alinhada ao cenário de *scouting* da NBA:

```markdown
# Parte 2 - Organização dos Documentos

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 2.1 Descrição e Especificação dos Arquivos

* **Tipos de arquivo:**
  * **Markdown (`.md`):** Formato principal dos relatórios de *scouting* e análises de pós-jogo, por facilitar a estruturação em tópicos e a extradição de metadados.
  * **PDF (`.pdf`):** Relatórios formais de dados estatísticos/físicos exportados de plataformas externas (como *Synergy Sports* ou *Second Spectrum*).
  * **JSON (`.json`):** Transcrições estruturadas de reuniões de vídeo e marcações de minutagem de jogadas.

* **Volume aproximado:**
  * **Centenas de documentos** por temporada. Em média, são gerados de 3 a 5 relatórios por partida (82 jogos na fase regular + *playoffs*), totalizando cerca de 300 a 400 documentos por ano por franquia.

* **Tamanho típico de cada documento:**
  * De **2 a 8 páginas** por relatório (aproximadamente **15 KB a 100 KB** por arquivo no formato texto/markdown). São documentos enxutos, focados em tópicos operacionais e táticos.

* **Frequência de entrada e ciclo de vida:**
  * **Entrada de novos arquivos:** Diária ou a cada 2 dias (acompanhando o calendário oficial de jogos).
  * **Atualização/Substituição:** Documentos de *scouting* de um adversário específico são **atualizados incrementalmente** antes de cada novo confronto na temporada. Relatórios antigos de jogos passados não são apagados, mas são arquivados para manter o histórico de evolução do rival.

---

### 2.2 Proposta da Estrutura de Pastas

```text
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

### 2.3 Respostas às Perguntas de Gestão e Segurança

#### Existe documento que NÃO deve entrar na base? Como você impediria a entrada?

* **Documentos proibidos na base de RAG:**
1. **Dados Médicos e Fisiológicos Pessoais:** Exames de imagem (ressonâncias), relatórios médicos confidenciais e registros de lesões protegidos por sigilo/hipaa/direitos dos atletas.
2. **Contratos e Informações Financeiras:** Salários, clausulas contratuais, negociações de *trade* e dados do teto salarial (*salary cap*).
3. **Rascunhos e Anotações Não Validadas:** Arquivos temporários de vídeo que ainda não passaram pelo crivo do coordenador da análise.


* **Mecanismos de Prevenção:**
* **Validação por Schema na Ingestão (CI/CD / Script de Carga):** O script de ingestão verifica se o arquivo possui a estrutura de cabeçalho válida (YAML front-matter) e se está localizado dentro das pastas permitidas (`/adversarios/` ou `/interno/`).
* **Filtro por Extensão e Nomenclatura:** Extensões não homologadas (`.docx`, `.xlsx`) ou arquivos marcados com a tag `status: draft` ou `sigiloso: true` no metadata são ignorados automaticamente pelo pipeline.
* **Controle de Acesso ao Repositório (RBAC):** A pasta onde o pipeline de RAG lê os arquivos é isolada e tem acesso restrito apenas aos analistas de desempenho autorizados.



#### Como você lidaria com VERSÕES do mesmo documento?

* **O Problema no Cenário:** Um relatório de *scouting* do *Boston Celtics* feito em novembro de 2025 pode conter um esquema de troca de marcação que o time rival já abandonou em março de 2026. Se o RAG recuperar a versão antiga sem contexto, o técnico receberá uma instrução desatualizada.
* **Solução na Arquitetura:**
1. **Versionamento via Metadados Obrigatórios (`data_partida` + `versao`):** Todo chunk armazenado na Vector Store obrigatoriamente carrega a data do relatório e o número da versão do jogo.
2. **Filtro de Recência no Pre-Retrieval:** Por padrão, as buscas para o jogo de hoje aplicam o filtro para buscar apenas chunks da partida mais recente ou da temporada vigente (`temporada == '2025-2026'`).
3. **Depreciação/Soft Delete:** Quando um novo relatório de *scouting* do mesmo adversário entra no sistema, o pipeline marca os vetores da versão anterior no banco com a tag `status: arquivado` ou `is_latest: false`. O retriever ignora vetores onde `is_latest == false`, a menos que o técnico pergunte explicitamente: *"O que mudou na defesa do Celtics em relação ao primeiro jogo do ano?"*.



```

```


# Parte 3 - Pipeline de Ingestão

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 3.1 Arquitetura do Fluxo de Ingestão

O pipeline transforma os arquivos brutos produzidos pela equipe de vídeo e *scouting* em vetores pesquisáveis no banco vetorial. O fluxo segue estas etapas encadeadas:

```text
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

### 3.1 Detalhamento da Etapa de Extração

Nesta etapa, o objetivo é converter arquivos heterogêneos de *scouting* e análise em texto estruturado sem perda de contexto tático.

---

#### Como o texto seria extraído por tipo de documento?

* **PDFs com texto selecionável (Relatórios Digitais do Synergy/Second Spectrum):**
  * **Tratamento:** Utilização da biblioteca `pdfplumber` ou `UnstructuredPDFLoader`. O foco é extrair a camada de texto nativa mantendo a sequência de leitura correta e ignorando elementos visuais decorativos (como logotipos dos times ou marcas d'água).

* **PDFs digitalizados (Imagens escaneadas de anotações da comissão):**
  * **Tratamento:** Aplicação de pipeline de **OCR (Optical Character Recognition)** com `Tesseract` ou `EasyOCR`. Antes da extração do texto, a imagem da página passa por pré-processamento (binarização, ajuste de contraste e remoção de ruídos) para maximizar a precisão no reconhecimento de anotações manuscritas ou escaneadas.

* **Tratamento de Tabelas (Quadros Estatísticos e Métricas de Arremesso):**
  * **É importante manter?** **Sim, extremamente importante.** Tabelas de *scouting* contêm métricas decisivas (ex: aproveitamento de arremessos por zona do campo, eficiência em *Pick and Roll*).
  * **Como tratar:** Em vez de extrair a tabela como linhas desconexas de texto, a ferramenta `pdfplumber` converte a estrutura da tabela para o formato **Markdown Table** ou **JSON**. Isso garante que a relação lógica entre as colunas (*Ex: "Zona Morta Esquerda" -> "Arremessos Convertidos" -> "45%"*) seja preservada para o LLM.

* **Tratamento de Imagens (Diagramas de Prancheta e Formações Táticas):**
  * **Posso descartar?** Não se a imagem contiver diagramas de jogadas (prancheta tática com setas e posições dos atletas).
  * **Quais informações elas têm?** Rotas de movimentação ofensiva, pontos de bloqueio e posicionamento defensivo.
  * **Como tratar:** As imagens extraídas do relatório passam por um modelo multimodal (ex: `GPT-4o` com visão computacional) que gera uma **descrição textual detalhada da jogada** (ex: *"Diagrama mostrando o armador recebendo bloqueio cego na cabeça do garrafão com o pivô abrindo para o arremesso de três"*). Essa descrição em texto é inserida no documento no lugar da imagem original.

* **Tratamento de Documentos Multimodais (Vídeos de Análise + Áudio das Reuniões):**
  * **Vídeo + Áudio:** Os arquivos de vídeo das reuniões táticas passam pelo modelo de transcrição **Whisper (OpenAI)** para converter a fala do treinador e dos analistas em texto.
  * **Sincronização de Minutagem:** A transcrição é gerada com *timestamps* (marcações de tempo), permitindo criar um documento Markdown estruturado contendo o texto da fala associado ao minuto exato do vídeo do jogo.

---

#### Problemas que podem surgir durante a extração e casos concretos

1. **Desalinhamento da Ordem de Leitura em Múltiplas Colunas:**
   * *O problema:* PDFs de *scouting* usam frequentemente layouts de 2 ou 3 colunas (lado a lado). Parsers ingênuos leem o arquivo na horizontal da esquerda para a direita, misturando linhas da Coluna 1 com linhas da Coluna 2 e destruindo a coerência do texto.

2. **Perda de Contexto em Tabelas Sem Bordas:**
   * *O problema:* Ferramentas comuns de OCR agrupam os números de uma tabela estatística em uma única frase corrida (ex: *"Jayson Tatum 25 10 4 45%"*), fazendo o modelo perder a noção de qual número pertence a qual métrica (*Pontos, Rebotes, Assistências ou Aproveitamento*).

3. **Caso Concreto (Problema Enfrentado na Aula 04 / Atividades Anteriores):**
   * *Caso:* Ao processar arquivos Markdown/PDF na Aula 04 contendo código ou tabelas táticas simples, a leitura direta por quebra de linha simples desformatava os cabeçalhos das seções e colava o título da seção seguinte no final do último parágrafo da seção anterior. Isso gerou *chunks* misturando assuntos distintos (como juntar as observações sobre o ataque com as instruções sobre a defesa), o que poluiu a busca semântica do retriever.



### 3.2 Detalhamento da Etapa de Limpeza e Normalização

A etapa de limpeza e normalização garante que o texto extraído fique higienizado, legível e livre de ruídos estruturais que possam poluir o cálculo de similaridade vetorial ou gastar tokens desnecessariamente no LLM.

---

#### O que precisa ser removido?

* **Cabeçalhos e Rodapés Repetidos:** Elementos fixos do topo e fim das páginas dos PDFs (ex: *"Boston Celtics Scouting Report - Confidential"*, *"Page 3 of 12"*). Se mantidos, esses textos repetitivos criam falsos picos de relevância na busca semântica.
* **Marcas d'Água e Ruídos de Layout:** Inscrições institucionais (ex: *"DRAFT"*, *"USO EXCLUSIVO DA COMISSÃO TÉCNICA"*) extraídas acidentalmente pelo OCR.
* **Numeração de Páginas e Sumários:** Índices com números de página e contadores isolados no meio do texto que quebram o fluxo de leitura do modelo.
* **Metadados de Impressão e Artefatos Visuais:** Linhas pontilhadas, divisores estéticos (ex: `-------------------`), links quebrados de mídias/vídeos e tags HTML/PDF órfãs.

---

#### O que precisa ser padronizado?

* **Nomenclatura Tática e Siglas do Esporte:**
  * Padronização de termos táticos para garantir uma representação vetorial única no banco (ex: converter variações como `"P&R"`, `"pnr"`, `"pick & roll"` e `"Pick-and-Roll"` para o termo padrão `"Pick and Roll"`).
  * Tradução ou expansão de siglas de posições e ações de quadra (ex: `"PG"` -> `"Armador"`, `"BLOB"` -> `"Saída de Fundo"`, `"ATO"` -> `"Após Pedido de Tempo"`).
* **Codificação de Texto (Encoding):**
  * Conversão forçada de todos os arquivos para **UTF-8**, eliminando caracteres corrompidos, símbolos de acentuação desformatados ou *mojibake* decorrentes da exportação de PDFs antigos.
* **Quebras de Linha e Espaçamento Branco:**
  * Remoção de hifenização de quebra de página (ex: converter `"de- fesa"` para `"defesa"`).
  * Substituição de múltiplos espaços em branco, tabulações e quebras de linha duplas/triplas por espaços únicos ou quebras organizadas por parágrafo (`\n\n`).

---

#### Que informação você corre o risco de perder ao limpar demais?

1. **Estrutura de Tópicos e Hierarquia (Cabeçalhos Markdown):**
   Ao remover quebras de linha ou caracteres de formatação de forma agressiva, corre-se o risco de apagar os marcadores `#` e `##`. Isso destrói a separação entre seções cruciais (como a fronteira entre a seção de *"Ataque"* e a de *"Defesa"*), fazendo com que o splitter misture conceitos opostos no mesmo *chunk*.

2. **Acentos e Grafia Original de Nomes Próprios:**
   Normalizar o texto removendo acentuação (passando tudo para ASCII simples, ex: de `"Nikola Jokić"` para `"Nikola Jokic"`) pode facilitar a busca por palavra-chave simples, mas perde a especificidade do nome próprio e prejudica a correspondência exata quando o usuário pesquisa usando a ortografia correta do atleta.

3. **Métricas Negativas ou Condicionais:**
   Filtros ingênuos que removem palavras de parada (*stop words*) ou pontuações podem alterar completamente o significado tático de uma instrução. Por exemplo, apagar pontuações ou palavras curtas pode transformar a frase *"Não faz dobras no perímetro"* em *"Faz dobras no perímetro"*, invertendo a orientação tática dada ao time.



### 3.3 Detalhamento da Frequência de Ingestão e Ciclo de Vida

A ingestão de dados em uma franquia da NBA precisa acompanhar a dinâmica de uma temporada regular, equilibrando o tempo de resposta do sistema com a atualização constante dos dados de *scouting*.

---

#### Como o pipeline roda e com que frequência chegam novos documentos?

* **Modo de Execução:** O pipeline opera de forma **híbrida: Orientada a Eventos (*Event-Driven*) e Agendada (*Cron Job*)**.
  1. **Orientada a Eventos (Sob Demanda via Webhook / File Watcher):** Sempre que um analista de desempenho exporta um novo arquivo `.md` ou `.pdf` para a pasta monitorada do time (`/documentos_scouting/2025-2026/...`), um serviço (*File Watcher*) detecta a criação do arquivo e dispara o pipeline de ingestão imediatamente para aquele documento específico.
  2. **Agendada (Noturna / Batch):** Um *Cron Job* roda diariamente às 03:00 AM para sincronizar transcrições de vídeos e dados estáticos consumidos das APIs parceiras (como *Synergy Sports*).

* **Frequência de Chegada de Novos Documentos:**
  * **Em Dias de Jogo (a cada 24h ou 48h):** Chegam de 2 a 4 novos relatórios (análises pré-jogo, plano de jogo da comissão e relatório pós-jogo).
  * **Dias Sem Jogo / Treino:** Entrada menor (1 a 2 documentos com revisões táticas ou relatórios de evolução individual de atletas).

---

#### Reprocessamento: Apenas o documento atualizado ou a base inteira?

* **Estratégia Escolhida:** Reprocessamento **Incremental (Apenas o Documento Alterado)**.
* **Por que não reprocessar a base inteira?** Reprocessar centenas de documentos a cada modificação gera custo desnecessário com chamadas de API de embeddings/LLM e aumenta a latência de disponibilidade da informação no iPad do treinador.

---

#### Como o sistema sabe qual documento reprocessar?

O controle de alteração e idempotência é feito por **Hash de Conteúdo (MD5/SHA-256) + Mapeamento de Metadados**:

1. **Cálculo do Hash no Início da Carga:**
   Quando o script de ingestão lê um arquivo, ele calcula o hash do seu conteúdo (ex: `SHA-256`).
2. **Checagem na Tabela de Controle (Manifesto de Ingestão):**
   O sistema consulta um banco SQLite/Redis interno mantido pelo pipeline:
   * **Arquivo Novo (Hash não existe):** Executa o pipeline completo (extração, chunking, embedding e inserção de novos vetores).
   * **Arquivo Identico (Hash idêntico ao gravado):** Ignorado. Nenhuma ação é tomada.
   * **Arquivo Modificado (Mesmo nome de arquivo/caminho, mas Hash diferente):**
     * O sistema recupera todos os vetores antigos associados ao `documento_id` ou `caminho_arquivo` no banco vetorial (ChromaDB/Qdrant).
     * Executa a **deleção dos vetores antigos** correspondentes àquele documento específico.
     * Gera os novos *chunks*, calcula os novos embeddings e realiza a inserção dos vetores atualizados (*Upsert*).

# Parte 4 - Metadados

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 4.1 Metadados do Documento

Os metadados no nível de documento são atribuídos no momento da ingestão e servem como pilar para o filtro pré-busca (*Pre-Retrieval Filtering*). Isso garante que o sistema restrinja a busca vetorial apenas ao universo de documentos táticos relevantes para a partida.

#### Schema JSON do Documento

```json
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

```json
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


Aqui está o bloco completo da **Subseção 4.2 - Metadados do Chunk** em formato `.md`, respondendo a todas as perguntas do checklist com foco absoluto no cenário da NBA:

```markdown
### 4.2 Metadados do Chunk

Enquanto os metadados do documento descrevem o arquivo como um todo, os metadados do *chunk* trazem granularidade tática ao trecho específico de texto. Isso garante precisão cirúrgica no *retrieval* e citação exata de fonte.

#### Schema JSON do Chunk

```json
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

```

---

#### Justificativa de Cada Metadado Escolhido

* **`document_id` (`string`):** Chave estrangeira que vincula o chunk ao documento pai no repositório.
* **`chunk_id` (`string`):** Identificador único do vetor na Vector Store (formato `<doc_id>-c<index>`). Necessário para atualizar ou deletar trechos específicos.
* **`chunk_index` (`integer`):** Ordem sequencial do trecho dentro do documento. Permite recuperar o chunk anterior ou posterior (*Adjacent Chunk Retrieval*) para reconstruir contexto contínuo se necessário.
* **`page` (`integer`):** Número da página no documento original (ou PDF) de onde o trecho foi extraído.
* **`section` (`string`):** Cabeçalho da seção Markdown (ex: `"Defesa de Pick and Roll"`). Preserva o tópico tático ao qual o parágrafo pertence.
* **`fase_jogo` (`string`):** Categoria tática do trecho (`defesa_pnr`, `transicao_ofensiva`, `bola_parada`, `isolamento`). Crucial para filtros temáticos.
* **`jogadores_foco` (`list[string]`):** Lista de atletas citados diretamente no parágrafo. Permite buscas focadas no comportamento de um jogador específico.
*  Herança de Metadados Críticos (`time_adversario`, `temporada`, `data_partida`, `is_latest`): Replicados do documento pai para permitir filtragem booleana direta no índice de vetores sem precisar fazer *joins* em tempo de execução.

---

### Respostas às Perguntas do Projeto

#### 1. Quais metadados você usaria para filtrar a busca? Dê um exemplo de pergunta em que o filtro é indispensável.

* **Metadados de Filtro:** `time_adversario`, `temporada`, `fase_jogo`, `is_latest` e `jogadores_foco`.
* **Exemplo de Pergunta em que o Filtro é Indispensável:**
> *"Como o Boston Celtics defendeu o Pick and Roll nos últimos jogos sem o Porziņģis em quadra?"*


* **Por que é indispensável?**
Se o sistema fizer uma busca vetorial simples por "defesa de Pick and Roll", o modelo retornará trechos de como o *Lakers*, *Nuggets* ou *Warriors* defendem essa jogada, ou relatórios do próprio *Celtics* da temporada passada. Aplicando o filtro pré-busca (`time_adversario == "Boston Celtics"` AND `fase_jogo == "defesa_pnr"` AND `is_latest == true`), o banco reduz a busca exclusivamente aos relatórios do rival atual.

---

#### 2. Quais metadados você usaria para citar a fonte ao usuário? O que exatamente apareceria na tela junto da resposta?

* **Metadados para Citação:** `title`, `data_partida`, `section`, `page` e `author`.
* **O que apareceria na tela do iPad do Treinador (Exemplo de Interface):**

> **Resposta da IA:**
> *"O Boston Celtics utiliza Drop Coverage contra o Pick and Roll no topo, mantendo o pivô recuado na área pintada e forçando o arremessador para a meia distância."*
> 📌 **Fonte Consultada:**
> 📄 *Relatório de Scouting Pré-Jogo - Boston Celtics*
> 📅 **Data:** 10/03/2026 | 📖 **Seção:** *Defesa de Pick and Roll* (Pág. 2)
> 👤 **Analista:** *Lucas Silva (Head of Scouting)*

---

#### 3. Que metadado seria caríssimo de acrescentar depois que a base já estivesse indexada? Por quê?

* **Metadado Caríssimo:** **`fase_jogo`** e **`jogadores_foco`** (Metadados Semânticos/Extraídos via LLM).
* **Por quê?**
Metadados simples como `data_partida` ou `time_adversario` podem ser inferidos do caminho da pasta usando scripts em milissegundos. Porém, extrair a `fase_jogo` ou identificar todos os `jogadores_foco` citados dentro do texto exige que um LLM (como o GPT-4o-mini) **leia e analise o conteúdo de cada um dos milhares de chunks individualmente**.
Se a base já estiver indexada com 10.000 chunks e você decidir criar o campo `fase_jogo` depois, terá que rodar uma chamada de API de LLM para cada chunk, gerando um custo alto de processamento, gasto financeiro com tokens e reindexação total do banco vetorial.

---

#### 4. Como você vai extrair esses metadados?

A extração utiliza uma estratégia em três camadas durante a ingestão:

1. **Extração Automática do Caminho/Estrutura de Arquivos (Folder-Based Metadata):**
* O pipeline lê a estrutura de diretórios `/2025-2026/adversarios/boston_celtics/` e preenche automaticamente `temporada`, `category` e `time_adversario` via Regex.


2. **Parsing do Cabeçalho e Estrutura do Documento (Structural Parsing):**
* O `RecursiveCharacterTextSplitter` preserva a hierarquia Markdown (`#`, `##`), preenchendo o campo `section` a partir do título do tópico atual.
* `page` e `chunk_index` são gerados iterativamente pelos parsers de PDF e splitters.


3. **Extração Semântica Estruturada via LLM (LLM-Based Extraction):**
* Antes do embedding, o texto do chunk passa por um modelo LLM leve com **Structured Output (JSON Schema / Pydantic)** para identificar entidades citadas no texto, preenchendo os campos `jogadores_foco` e `fase_jogo`.



```

```

# Parte 5 - Chunking / Splitting

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 5.1 Estratégia de Chunking e Configurações

A definição da estratégia de divisão de texto é determinante para a precisão do *retrieval*. Em relatórios táticos de basquete, um trecho precisa conter contexto suficiente para descrever uma jogada inteira sem diluir o significado nem cortar dados essenciais.

---

#### Qual estratégia de splitting e splitter você utilizaria?

* **Estratégia Escolhida:** **`RecursiveCharacterTextSplitter`** estruturado com **divisores baseados em sintaxe Markdown**.
* **Utilizaria um splitter recursivo?** **Sim.** O splitter recursivo tenta primeiro dividir por marcadores de seções maiores e, se o trecho ainda ultrapassar o tamanho limite, tenta quebrar em marcadores menores de forma hierárquica.
* **Separadores Utilizados (em ordem de prioridade):**
  1. `"\n## "` (Cabeçalhos de Seção Principal, ex: `## Defesa de Pick and Roll`)
  2. `"\n### "` (Subseções, ex: `### Ajuste no Garrafão`)
  3. `"\n\n"` (Quebras de Parágrafo)
  4. `"\n"` (Quebras de Linha)
  5. `" "` (Espaço entre palavras)

---

#### Qual tamanho aproximado dos chunks e overlap?

* **Tamanho dos Chunks (`chunk_size`):** **350 a 500 caracteres** (~70 a 100 palavras em português/inglês).
* **Overlap (`chunk_overlap`):** **50 a 70 caracteres** (~10 a 15% do tamanho do chunk).
* **Base da Divisão:** A divisão é feita **por caracteres com respeito semântico a parágrafos e seções** (usando a recursividade para nunca cortar palavras ao meio).

---

#### Utilizaria uma estratégia específica para cada tipo de documento?

**Sim, obrigatoriamente.** Um relatório tático em Markdown, uma tabela estatística em PDF e uma transcrição de reunião de vídeo pedem tratamentos totalmente distintos:

* **Relatórios Táticos em Markdown (`.md`):** `RecursiveCharacterTextSplitter` focado na hierarquia de títulos (`#`, `##`), garantindo que o título do tópico acompanhe o parágrafo descritivo.
* **Transcrições de Vídeo/Reunião (`.json` / `.txt`):** Splitter baseado em **janela temporal/diálogo**, onde o chunk é delimitado pelas falas completas de um analista ou por blocos fixos de tempo (ex: a cada 1 ou 2 minutos de reunião).
* **Relatórios Numéricos / Tabelas Estatísticas (`.pdf`):** Processamento via **HTML/Markdown Table Splitter**, mantendo a tabela inteira dentro de um único chunk estruturado ou convertendo cada linha em um objeto com o cabeçalho concatenado.

---

### 5.2 Respostas às Perguntas de Avaliação do Chunking

#### O que pode acontecer se os chunks forem muito pequenos?

1. **Perda de Contexto Semântico (Sub-contexto):** Um chunk de 50 caracteres contendo apenas *"O Celtics faz dobra no topo"* não explica **quem** faz a dobra, **quando** faz ou **qual é a rotação** defensiva. O vetor gerado fica vago.
2. **Fragmentação da Resposta:** O retriever recupera pedaços isolados que não fornecem ao LLM a explicação completa da jogada, forçando o modelo a responder de forma incompleta ou alucinar os detalhes ausentes.

---

#### O que pode acontecer se os chunks forem muito grandes?

1. **Diluição da Informação (Efeito "Agulha no Palheiro"):** Em um chunk de 2.000 caracteres cobrindo o jogo inteiro, um detalhe crucial de 10 palavras sobre a tendência de infiltração do Jayson Tatum fica "diluído" na média vetorial. O cálculo de similaridade de cosseno cai e o retriever pode ignorar esse chunk.
2. **Poluição do Prompt e Custo Elevado:** Enviar chunks gigantescos para o LLM consome tokens desnecessários da janela de contexto, aumenta o tempo de latência na beira da quadra e pode fazer o modelo sofrer de *Lost in the Middle* (ignorar trechos relevantes situados no meio de um contexto muito longo).

---

#### Como você trataria uma tabela na hora de dividir? Uma tabela cortada ao meio ainda significa alguma coisa? E uma imagem?

* **Tratamento de Tabelas:**
  * **Uma tabela cortada ao meio perde totalmente o sentido.** Se a primeira linha com o cabeçalho das colunas (`Jogador | Aproveitamento 3P | Pontos`) ficar no Chunk 1 e os dados numéricos ficarem no Chunk 2, o Chunk 2 se torna apenas um monte de números sem significado.
  * **Solução na Arquitetura:**
    1. **Tabelas Pequenas/Médias:** Definir uma regra no pipeline de ingestão para **nunca quebrar a tabela**. Ela deve ser tratada como um bloco atômico único (`chunk_size` expandido dinamicamente para comportar a tabela inteira em Markdown).
    2. **Tabelas Grandes:** Converter a tabela para o formato **JSON por Linha (JSON Lines)** ou **Markdown**, onde o cabeçalho das colunas é replicado em cada linha (ex: `{"jogador": "Tatum", "arremesso_3p": "41.6%"}`).

* **Tratamento de Imagens (Diagramas de Prancheta):**
  * Uma imagem cortada ao meio é inutilizável. 
  * **Solução:** A imagem do diagrama tático é convertida em uma **descrição textual analítica via modelo Multimodal (Visão)** antes da etapa de chunking. Essa descrição em texto é anexada ao chunk como um bloco contínuo acompanhado da tag `[Diagrama Tático]`.

---

#### Como saber se a sua escolha de chunking foi boa? Que evidência você juntaria para provar isso?

Para provar a qualidade da escolha de chunking no cenário da NBA, eu juntaria duas formas de evidência:

1. **Avaliação Quantitativa sem Humanos (Métricas RAGAS / TruLens):**
   * **Context Recall:** Medir se o retriever consegue trazer todos os chunks necessários para responder às perguntas táticas de teste.
   * **Context Precision:** Avaliar a proporção de texto relevante recuperado em relação ao ruído trazido nos chunks. Se a precisão for baixa, significa que o `chunk_size` está grande demais.
   * **Faithfulness (Fidelidade):** Verificar se as respostas geradas pelo LLM se baseiam estritamente no contexto recuperado.

2. **Avaliação Qualitativa Prática (Teste de Estresse com a Comissão Técnica):**
   * Montar um conjunto de teste (*Ground Truth*) com **20 perguntas táticas reais** elaboradas pelos analistas de *scouting* do time, pareadas com as respostas ideais extraídas dos relatórios originais.
   * **Evidência Definitiva:** Rodar o benchmark comparando a taxa de acerto do RAG com diferentes tamanhos de chunk (ex: 200 vs 450 vs 1000 caracteres) e provar que a configuração de **450 caracteres** gerou a maior taxa de acerto em perguntas sobre esquemas defensivos e jogadas específicas.


# Parte 6 - Embeddings

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 6.1 Tabela Comparativa e Especificação do Modelo

| Item | Especificação no Cenário da NBA |
| :--- | :--- |
| **Modelo escolhido** | **`text-embedding-3-small` (OpenAI)** / *Alternativa Local:* `BAAI/bge-m3` |
| **Dimensão do embedding** | **1.536 dimensões** (configurável até 512 via Matryoshka) |
| **Suporta português?** | **Sim** (desempenho elevado em múltiplos idiomas) |
| **É multilíngue?** | **Sim** (treinado em mais de 100 idiomas) |
| **Tamanho máximo de entrada** | **8.191 tokens** (~6.000 palavras) |
| **É open source?** | **Não** (Proprietário - OpenAI) |
| **Pode ser executado localmente?** | **Não** (Apenas via chamada de API) |
| **Possui API?** | **Sim** (OpenAI Embeddings API) |
| **Custo aproximado** | **$0.00002 por 1.000 tokens** (~$0,02 para 1 milhão de tokens) |
| **Fonte da informação (link)** | [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings) |

---

### 6.2 Justificativa: Por que esse modelo é adequado ao cenário?

O `text-embedding-3-small` oferece um equilíbrio ideal de **alta precisão semântica e custo extremamente baixo** para a comissão técnica da NBA. 

Análises táticas misturam inglês (linguagem padrão do basquete mundial, como *"Pick and Roll"*, *"Drop Coverage"*, *"Corner 3"*) com notas de analistas em português. A capacidade multilíngue do modelo garante que termos técnicos mantêm alta similaridade vetorial independentemente do idioma das notas do analista. Além disso, as 1.536 dimensões fornecem resolução suficiente para distinguir detalhes táticos sutis (como a diferença entre uma dobra na cabeça do garrafão e uma dobra na linha de fundo) com latência de busca inferior a 50 ms.

---

### 6.3 Respostas às Perguntas de Análise

#### Considerou algum modelo alternativo e descartou? Qual, e por quê?

* **Modelo Alternativo Considerado:** **`text-embedding-ada-002`** (modelo anterior da OpenAI) e **`all-MiniLM-L6-v2`** (Open Source / Hugging Face).
* **Por que foram descartados?**
  * O `text-embedding-ada-002` foi descartado por ser mais caro e apresentar desempenho semântico inferior ao `text-embedding-3-small` no benchmark MTEB (*Massive Text Embedding Benchmark*).
  * O `all-MiniLM-L6-v2` foi descartado para o ambiente principal por ter uma janela de contexto muito reduzida (**256 tokens**), o que limitaria o tamanho dos *chunks* e cortaria a interpretação semântica de parágrafos táticos mais longos.

---

#### Se o cenário envolve documentos sigilosos, isso muda sua escolha entre modelo local e API? Como?

**Sim, muda significativamente a arquitetura e a governança de dados.**

* **Cenário de Nuvem Privada / API (Escolha Principal):** 
  Se a franquia utilizar a API da OpenAI sob **contrato Enterprise**, os Termos de Serviço da OpenAI garantem expressamente que os dados enviados via API **não são utilizados para treinamento de modelos públicos**. Além disso, o tráfego é criptografado e seguro.
* **Cenário 100% On-Premise / Air-Gapped (Fallback de Segurança):** 
  Se a diretoria da franquia proibir qualquer envio de estratégias sigilosas para servidores de terceiros, a escolha muda para o **`BAAI/bge-m3`** executado **100% localmente** nos servidores da própria arena/centro de treinamento. O `bge-m3` é Open Source, possui janela de 8.192 tokens, suporte multilíngue nativo e pode rodar em uma GPU local sem tráfego de dados para a internet.

---

#### O tamanho máximo de entrada do modelo tem relação com a sua decisão de chunking da Parte 5? Explique.

**Sim, totalmente.** O tamanho máximo de entrada do modelo de embedding estabelece o **teto técnico absoluto** para o tamanho do *chunk*.

* O `text-embedding-3-small` aceita até **8.191 tokens**, enquanto nossa estratégia de *chunking* definida na Parte 5 utiliza blocos de **350 a 500 caracteres** (~100 tokens).
* **Por que operar tão abaixo do limite do modelo?** 
  Embora o modelo suporte entradas gigantes, criar *chunks* próximos do limite de 8.191 tokens causaria o fenômeno de **diluição do embedding**: o vetor representaria a média geral de várias páginas e perderia a capacidade de encontrar detalhes específicos (ex: uma rotação de ajuda na linha de fundo). A decisão da Parte 5 garante que cada vetor de 1.536 dimensões fique totalmente denso e focado em uma única instrução tática.


  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  Aqui está o bloco completo da **Parte 1 - Identificação dos Problemas** adaptado para o **Cenário B: Recomendador e Assistente de Leitura / Curadoria Editorial de Livros**, seguindo exatamente a mesma estrutura detalhada e profissional aplicada ao cenário da NBA.

---

# Parte 1 - Identificação dos Problemas

## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária

### 1.1 Descrição do Problema

#### Qual é o problema que você deseja resolver?
A busca e recomendação de livros em grandes acervos editoriais ou bibliotecas digitais sofre com limitações de busca por palavras-chave tradicionais (*Keyword Search*). leitores e editores frequentemente buscam obras com base em **nuances temáticas, estilo de escrita, arcos de personagens, tom emocional ou similaridade de enredo**, elementos que não aparecem em metadados simples como título ou autor.
Além disso, equipes editoriais lidam com centenas de manuscritos, resenhas e relatórios de leitura (*reader reports*), tornando lento o processo de identificar quais obras do catálogo atendem ao perfil de determinado leitor ou se alinham a uma tendência de mercado.

---

#### Quem utilizaria a aplicação? (Descrição concreta do usuário)

* **Perfil 1: Curador Editorial / Editor de Aquisições**
* **Cargo:** Editor de Literatura ou Curador de Clube de Leitura.
* **Contexto de Uso:** Durante reuniões de pauta ou ao responder demandas de leitores, buscando obras do catálogo que se encaixem em recortes específicos (ex: *"fiquei com vontade de ler algo parecido com a atmosfera de suspense de 'A Hora da Estrela'"*).
* **Nível Técnico:** Baixo em TI; alto domínio em teoria literária e análise textual.


* **Perfil 2: Leitor Final / Assinante de Plataforma Literária**
* **Cargo:** Leitor comum / Assinante de e-commerce ou biblioteca digital.
* **Contexto de Uso:** Busca por próximas leituras via aplicativo mobile ou web no momentos de lazer.
* **Nível Técnico:** Leigo.



---

#### Que tipo de informação o usuário gostaria de consultar?

* Sinopses analíticas e resenhas críticas profundas.
* Trechos, capítulos de amostra e citações marcantes das obras.
* Relatórios de leitura interna (*reader reports*) com avaliação de tom, ritmo e temas sensíveis (*trigger warnings*).
* Metadados editoriais (gênero, subgênero, número de páginas, prêmios recebidos, época retratada, ambientação geográfica).

---

#### De onde vêm essas informações?

1. **Arquivos de Livros Digitais (`.epub`, `.pdf`):** Texto integral ou capítulos de amostragem.
2. **Relatórios Editoriais (`.md`, `.docx`):** Análises internas feitas por pareceristas sobre o manuscrito.
3. **Catálogo de Metadados (`.json`, `.csv`):** Informações estruturadas de publicação (ISBN, autor, ano, prêmios, classificação indicativa).

---

#### Por que utilizar um LLM sozinho não seria suficiente?

* **Alucinação de Obras e Detalhes:** LLMs tendem a inventar plots, fundir histórias de livros diferentes ou citar personagens que não existem no livro consultado.
* **Falta de Acesso ao Acervo Privado:** O LLM genérico não conhece o catálogo exclusivo de uma editora específica, nem os relatórios de leitura internos mantidos em sigilo comercial.
* **Custo e Limite de Contexto:** Injetar o texto integral de dezenas de livros inteiros de 300 páginas diretamente no *prompt* a cada pergunta do leitor inviabilizaria o sistema financeiramente e excederia as janelas de contexto.

---

#### Como o usuário vai utilizar o sistema?

O sistema será disponibilizado via **Interface Web (Dashboard do Editor)** para a equipe da editora e via **Aplicativo Mobile (Widget de Recomendação)** para o leitor final.

---

#### Três Perguntas Reais de Usuários (Casos Concretos)

1. *"Quero um romance de ficção científica ambientado em um futuro distópico, mas que foque nas relações familiares e não em guerras. Qual livro do nosso catálogo se encaixa nisso?"*
2. *"Tem algum livro de suspense no acervo com a mesma atmosfera claustrofóbica de 'O Iluminado', mas escrito por uma autora latina?"*
3. *"Quais obras publicadas entre 2020 e 2024 abordam o tema do luto na infância sem usar uma linguagem muito pesada?"*

### 1.2 Por que RAG?

#### Por que RAG é adequado para esse problema?

O RAG é a solução ideal porque conecta a capacidade de raciocínio e síntese do LLM a uma base de conhecimento factual e delimitada. Em curadoria editorial, o modelo precisa navegar por análises de leitores pareceristas, enredos detalhados, subtextos temáticos e metadados de catálogo. O RAG permite que a busca traga os trechos e relatórios exatos para o contexto do prompt, garantindo recomendações fundamentadas no acervo real da editora.

---

#### Que tipo de conhecimento precisa ser fornecido ao modelo?

* **Relatórios de Leitura e Pareceres Editoriais (*Reader Reports*):** Avaliações internas sobre tom, ritmo, arcos de personagens, temas centrais e alertas de conteúdo (*trigger warnings*).
* **Capítulos e Trechos Amostrais das Obras:** Texto integral ou excertos dos livros (`.epub`, `.pdf`, `.md`) para análise de estilo literário e linguagem.
* **Catálogo Estruturado de Metadados:** Título, autor, ISBN, gênero, subgênero, ano de publicação, público-alvo, premiações e status de direitos autorais.

---

#### Esse conhecimento muda com que frequência?

* **Semanal a Mensal:** O acervo é atualizado continuamente à medida que novos manuscritos são avaliados por pareceristas, novos contratos de publicação são assinados ou novos títulos entram no catálogo oficial da editora.

---

#### Existe necessidade de utilizar documentos privados ou específicos da organização?

* **Sim.** Relatórios de leitura interna, pareceres críticos de manuscritos ainda não publicados e dados estratégicos de aquisição de direitos autorais são documentos altamente confidenciais da editora e jamais estiveram expostos na internet para treinamento de modelos públicos.

---

#### Que problemas poderiam ocorrer se o LLM respondesse apenas com seu conhecimento pré-treinado? (Com Exemplo Concreto)

Se o LLM dependesse apenas de seu treino original, ele sofreria de **alucinação de catálogo** e **cegueira de acervo privado**:

1. Recomendaria livros populares do mercado geral de outras editoras em vez do catálogo próprio do cliente.
2. Inventaria enredos, misturando personagens de livros diferentes.
3. Não saberia avaliar manuscritos inéditos que acabaram de chegar à casa editorial.

* **Exemplo Concreto de Resposta Errada (Apenas LLM Pré-Treinado):**

> **Pergunta do Editor:**
> *"Qual livro de suspense do nosso catálogo possui uma narrativa não linear focada em trauma familiar, recomendado para leitores que gostaram de 'A Garota no Trem'?"*

> ❌ **Resposta Errada do LLM Sem RAG:**
> *"Recomendo o livro **'O Segredo da Casa Amarela'**, de Juliana Mendes, publicado pela sua editora em 2023. É um suspense claustrofóbico que conta a história de uma mulher com amnésia tentando recuperar as memórias de sua infância através de diários encontrados no sótão."*
> ⚠️ **O Erro:** O livro *"O Segredo da Casa Amarela"* **não existe** no catálogo da editora (o LLM alucinou o título e a autora), e o enredo descrito é uma fusão genérica de clichês do gênero que não corresponde a nenhuma obra do acervo real.

### 1.3 Limitações — Quando RAG Não É a Resposta

#### Em quais situações RAG não seria a melhor solução para esse problema?

Apesar das suas vantagens para busca semântica e síntese de enredos, a arquitetura RAG pura apresenta limitações em cenários de consulta que exigem exatidão numérica, checagem direta de dados cadastrais ou regras de negócio estritas.

Abaixo estão três alternativas analíticas para este cenário:

1. **Consultas SQL em Banco de Dados Estruturado (Relacional):**
* *Aplicações:* Para obter metadados exatos de catálogo (ex: filtrar por ISBN, preço, data de publicação, quantidade de cópias em estoque ou formato do arquivo).
* *Por que supera o RAG:* O RAG pode falhar ao tentar recuperar um ISBN exato via busca por similaridade de vetores (*cosine similarity*), enquanto uma consulta SQL executada diretamente sobre um banco relacional entrega o resultado exato em milissegundos.


2. **Busca Tradicional por Palavra-Chave (*Keyword Search* / BM25 / Full-Text Search):**
* *Aplicações:* Para localizar nomes próprios raros de autores, termos específicos de edições especiais ou títulos exatos no acervo.
* *Por que supera o RAG:* Modelos de embedding nem sempre convertem nomes próprios raros ou códigos comerciais para representações vetoriais precisas. A busca por palavra-chave garante correspondência exata para termos específicos sem dependência de interpretação semântica.


3. **Combinação de Busca Híbrida (BM25 + RAG) com Roteamento SQL (Text-to-SQL / Multi-Agent):**
* *Aplicações:* Para responder a perguntas complexas do leitor ou editor que combinem necessidades semânticas ("livros com atmosfera melancólica") com restrições estruturadas ("publicados entre 2021 e 2023 com menos de 300 páginas").
* *Como funciona:* Um agente roteador identifica o tipo de intenção do usuário: direciona filtros de metadados rígidos para a camada SQL/Filtros e a busca de enredo/tom para o índice vetorial, combinando os resultados antes de enviar o prompt ao LLM.



---

#### Existe alguma pergunta, dentro do seu próprio cenário, que RAG responderia mal e um banco de dados relacional responderia bem? Qual, e por quê?

* **Exemplo de Pergunta em que o RAG Falharia:**
> *"Quantos livros do gênero ficção científica publicados após 2020 temos no catálogo e qual é o preço médio dessas obras?"*


* **Por que o RAG responderia mal?**
O RAG precisaria recuperar dezenas ou centenas de *chunks* espalhados pelo banco vetorial contendo metadados de cada livro de ficção científica, enviar todos esses blocos de texto na janela de contexto do LLM e "esperar" que o modelo conte os livros um a um e faça a média aritmética dos preços no texto. Isso gera alto custo de tokens, alta latência e, fundamentalmente, risco de **erro de contagem e cálculo estatístico** (o LLM não é um motor de execução aritmética garantido).
* **Por que o Banco Relacional (SQL) responderia bem?**
Uma simples consulta SQL do tipo:
```sql
SELECT COUNT(*), AVG(preco) 
FROM catalogo_livros 
WHERE genero = 'Ficção Científica' AND ano_publicacao > 2020;

```


Retorna o valor exato, determinístico e instantâneo em microssegundos sem dependência de modelos de linguagem.

---

#### O que aconteceria se a pergunta do usuário exigisse contar, somar ou ordenar informação espalhada por muitos documentos?

Se o usuário fizesse uma pergunta como *"Ordene todos os pareceres de leitura da temporada pelo nível de recomendação do parecerista"*, ocorreriam três falhas estruturais na arquitetura RAG tradicional:

1. **Truncamento de Contexto (*Top-K Limit*):** O *retriever* RAG opera limitando a busca aos top-$K$ *chunks* mais similares (ex: $K=5$ ou $K=10$). Ele não trará **todos** os documentos do catálogo para a resposta, omitindo dados e gerando uma ordenação/contagem incompleta.
2. **Efeito *Lost in the Middle*:** Mesmo se os $K$ *chunks* fossem expandidos para cobrir centenas de páginas, o LLM perde capacidade de atenção em contextos excessivamente longos, ignorando dados localizados no meio do prompt.
3. **Incapacidade de Agregação e Ordenação Precisa:** LLMs realizam previsão probabilística do próximo token; eles não possuem um motor interno de ordenação estruturada ou agregação de dados. A chance de o modelo "alucinar" a ordem correta ou pular itens na contagem é extremamente alta.


# Parte 2 - Organização dos Documentos

## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária

### 2.1 Descrição e Especificação dos Arquivos

* **Tipos de arquivo:**
  * **Markdown (`.md`) e Word (`.docx`):** Formato padrão dos relatórios de leitura (*reader reports*), pareceres críticos e resenhas internas elaboradas por editores e pareceristas.
  * **EPUB (`.epub`) e PDF (`.pdf`):** Arquivos contendo o texto integral dos livros publicados, amostras de capítulos ou manuscritos submetidos para avaliação de aquisição.
  * **JSON (`.json`):** Fichas catalográficas estruturadas contendo metadados oficiais (ISBN, autor, gênero, prêmios, data de publicação, palavras-chave e status de direitos autorais).

* **Volume aproximado:**
  * **Milhares de documentos.** O acervo de uma editora de médio/grande porte conta com **2.000 a 5.000 títulos publicados**, associados a cerca de **10.000 a 15.000 relatórios de leitura** (considerando pareceres de obras aprovadas e rejeitadas ao longo dos anos).

* **Tamanho típico de cada documento:**
  * **Relatórios de Leitura e Pareceres (`.md` / `.docx`):** De **2 a 5 páginas** (aproximadamente **20 KB a 80 KB** por arquivo).
  * **Livros Integrais / Manuscritos (`.epub` / `.pdf`):** De **150 a 500 páginas** (aproximadamente **500 KB a 10 MB** por arquivo, dependendo da presença de ilustrações).
  * **Fichas Catalográficas (`.json`):** De **5 KB a 20 KB** por título.

* **Frequência de entrada e ciclo de vida:**
  * **Entrada de novos arquivos:** **Semanal ou mensal.** Novos manuscritos e pareceres entram semanalmente no fluxo de avaliação; novos títulos publicados entram conforme o cronograma do plano editorial (de 5 a 20 lançamentos por mês).
  * **Atualização/Substituição:** Livros publicados raramente têm o texto alterado, mas recebem novas edições. Relatórios de leitura são **atualizados incrementalmente** caso o manuscrito passe por reescrita ou revisões editoriais antes do lançamento.

---

### 2.2 Proposta da Estrutura de Pastas

```text
acervo_editorial/
├── catalogo_publicado/
│   ├── ficcao/
│   │   ├── romance/
│   │   │   ├── 9788535900001_a_hora_da_estrela/
│   │   │   │   ├── texto_integral.epub
│   │   │   │   ├── ficha_catalografica.json
│   │   │   │   └── parecer_editorial_v1.md
│   │   │   └── ...
│   │   └── ficcao_cientifica/
│   └── nao_ficcao/
├── manuscritos_em_avaliacao/
│   └── 2026/
│       ├── avaliacao_inicial/
│       └── reader_reports/
│           └── report_ms_8921_versao_final.md
└── metadados_gerais/
    └── taxonomia_tematica_2026.json


Aqui está o bloco completo da **Parte 2 - Organização dos Documentos** adaptado para o **Cenário B: Assistente de Curadoria Editorial e Recomendação Literária**, mantendo a linguagem técnica, direta e alinhada ao mercado editorial:

```markdown
# Parte 2 - Organização dos Documentos

## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária

### 2.1 Descrição e Especificação dos Arquivos

* **Tipos de arquivo:**
  * **Markdown (`.md`) e Word (`.docx`):** Formato padrão dos relatórios de leitura (*reader reports*), pareceres críticos e resenhas internas elaboradas por editores e pareceristas.
  * **EPUB (`.epub`) e PDF (`.pdf`):** Arquivos contendo o texto integral dos livros publicados, amostras de capítulos ou manuscritos submetidos para avaliação de aquisição.
  * **JSON (`.json`):** Fichas catalográficas estruturadas contendo metadados oficiais (ISBN, autor, gênero, prêmios, data de publicação, palavras-chave e status de direitos autorais).

* **Volume aproximado:**
  * **Milhares de documentos.** O acervo de uma editora de médio/grande porte conta com **2.000 a 5.000 títulos publicados**, associados a cerca de **10.000 a 15.000 relatórios de leitura** (considerando pareceres de obras aprovadas e rejeitadas ao longo dos anos).

* **Tamanho típico de cada documento:**
  * **Relatórios de Leitura e Pareceres (`.md` / `.docx`):** De **2 a 5 páginas** (aproximadamente **20 KB a 80 KB** por arquivo).
  * **Livros Integrais / Manuscritos (`.epub` / `.pdf`):** De **150 a 500 páginas** (aproximadamente **500 KB a 10 MB** por arquivo, dependendo da presença de ilustrações).
  * **Fichas Catalográficas (`.json`):** De **5 KB a 20 KB** por título.

* **Frequência de entrada e ciclo de vida:**
  * **Entrada de novos arquivos:** **Semanal ou mensal.** Novos manuscritos e pareceres entram semanalmente no fluxo de avaliação; novos títulos publicados entram conforme o cronograma do plano editorial (de 5 a 20 lançamentos por mês).
  * **Atualização/Substituição:** Livros publicados raramente têm o texto alterado, mas recebem novas edições. Relatórios de leitura são **atualizados incrementalmente** caso o manuscrito passe por reescrita ou revisões editoriais antes do lançamento.

---

### 2.2 Proposta da Estrutura de Pastas

```text
acervo_editorial/
├── catalogo_publicado/
│   ├── ficcao/
│   │   ├── romance/
│   │   │   ├── 9788535900001_a_hora_da_estrela/
│   │   │   │   ├── texto_integral.epub
│   │   │   │   ├── ficha_catalografica.json
│   │   │   │   └── parecer_editorial_v1.md
│   │   │   └── ...
│   │   └── ficcao_cientifica/
│   └── nao_ficcao/
├── manuscritos_em_avaliacao/
│   └── 2026/
│       ├── avaliacao_inicial/
│       └── reader_reports/
│           └── report_ms_8921_versao_final.md
└── metadados_gerais/
    └── taxonomia_tematica_2026.json

```

#### Justificativa da Estrutura:

A organização por **`Status de Publicação -> Gênero -> Subgênero -> Obra (ISBN_Título)`** foi projetada para refletir o fluxo de trabalho da equipe editorial e otimizar os filtros de busca no RAG:

1. **Separação entre `catalogo_publicado/` e `manuscritos_em_avaliacao/` (Isolamento de Contexto):**
Garante que consultas de leitores finais no aplicativo recebam apenas recomendações de livros disponíveis no mercado (`catalogo_publicado/`), impedindo que o RAG recomende manuscritos não publicados ou obras cujos direitos autorais ainda não foram adquiridos.
2. **Hierarquia por Gênero e Subgênero (`ficcao/romance/...`):**
Espelha a taxonomia clássica das livrarias e editoras. Permite a extração automática de metadados de categoria diretamente do caminho da pasta (*folder-based metadata extraction*), facilitando filtros pré-busca quando o leitor solicita restrições específicas (ex: *"buscar apenas em Ficção Científica"*).
3. **Agrupamento por Obra (`9788535900001_a_hora_da_estrela/`):**
Isola em uma única pasta o livro completo (`.epub`), os pareceres internos (`.md`) e os metadados oficiais (`.json`). Essa centralização permite relacionar o texto original das obras com as análises feitas pelos editores sem risco de misturar pareceres de títulos diferentes.

---

### 2.3 Respostas às Perguntas de Gestão e Segurança

#### Existe documento que NÃO deve entrar na base? Como você impediria a entrada?

* **Documentos proibidos na base de RAG:**
1. **Dados Contratuais e Financeiros:** Contratos de cessão de direitos autorais, relatórios de *royalties*, adiantamentos pagos a autores e valores de vendas/margens de lucro.
2. **Dados Pessoais Sensíveis de Autores e Pareceristas (LGPD):** Endereços pessoais, dados bancários, números de documentos e contatos privados arquivados no cadastro do autor.
3. **Anotações Informais e Rascunhos Não Aprovados:** Notas pessoais de pareceristas que não passaram pelo crivo do editor sênior.


* **Mecanismos de Prevenção:**
* **Validação por Schema no Pipeline de Carga:** O script de ingestão aceita apenas arquivos localizados dentro dos diretórios homologados (`/catalogo_publicado/` e `/manuscritos_em_avaliacao/reader_reports/`).
* **Filtro de Front-Matter e Tags:** Arquivos com o cabeçalho contendo `sigiloso: true` ou `status: rascunho` são ignorados automaticamente pela rotina de ingestão.
* **Varredura por Regex de Dados Pessoais:** O pipeline aplica expressões regulares para detectar e bloquear arquivos contendo padrões de CPF, e-mail, telefone ou valores monetários/dados bancários.



#### Como você lidaria com VERSÕES do mesmo documento?

* **O Problema no Cenário:** Um manuscrito em avaliação pode passar por edições do autor (Versão 1 vs. Versão 2 final). Se o RAG recuperar um parecer ou capítulo da Versão 1 (onde um personagem ainda não existia ou o final era diferente), o editor tomará decisões com base em informações obsoletas.
* **Solução na Arquitetura:**
1. **Versionamento Obrigatório nos Metadados (`versao` + `is_latest`):** Todos os *chunks* gravados na Vector Store carregam a tag de versão e o campo booleano `is_latest`.
2. **Depreciação por Soft-Delete:** Quando a versão 2 de um relatório ou manuscrito é ingerida, a pipeline atualiza os vetores da versão anterior alterando `is_latest` de `true` para `false` e definindo `status: arquivado`.
3. **Filtro Padrão no Pre-Retrieval:** As buscas do sistema aplicam, por padrão, o filtro rígido `is_latest == true`. A versão antiga só é recuperada se o editor solicitar explicitamente um histórico de revisões (ex: *"O que mudou do primeiro parecer para a versão final do manuscrito?"*).



```

```

# Parte 3 - Pipeline de Ingestão

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA


[ Documentos Brutos ] ──► [ 1. Extração ] ──► [ 2. Limpeza ] ──► [ 3. Metadados ]
• EPUBs (Obras)           • ebooklib / BS4    • Normaliza UTF-8  • LLM Structured Output
• PDFs (Manuscritos)      • pdfplumber        • Remov. Cabeçalhos• JSON Schema Pydantic
• Markdown (Pareceres)    • python-frontmatter• Stripping Copyright
                                                                       │
                                                                       ▼
[ Banco Vetorial ] ◄── [ 6. Armazenamento ] ◄── [ 5. Embeddings ] ◄── [ 4. Chunking ]
• ChromaDB / Qdrant    • Upsert por SHA-256   • text-embedding-   • Recursive Splitter
• Indice HNSW          • Payload de Metadados   3-small (1536d)   • 800-1200 chars / Overlap 100

# Parte 3.1 - Detalhamento da Extração de Documentos

## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária

### 1. Estratégia Geral de Extração por Formato

A extração transforma arquivos heterogêneos de entrada em texto limpo, estruturado e padronizado em **Markdown**, preservando a hierarquia original da obra e dos relatórios pareceristas.

* **Arquivos EPUB (`.epub`):** Processados via `ebooklib` + `BeautifulSoup4`. Extrai-se o conteúdo XHTML das seções, convertendo tags de estrutura (`<h1>`, `<h2>`, `<p>`) em títulos e parágrafos Markdown.
* **Arquivos Word/Markdown (`.docx`, `.md`):** Pareceres de leitura em `.docx` são extraídos com `python-docx` para mapear estilos de cabeçalho e parágrafos. Arquivos `.md` têm o *front-matter* (YAML) separado do corpo do texto.

---

### 2. Tratamento de PDFs com Texto Selecionável

PDFs nativos de manuscritos e provas de imprensa são extraídos via **`pdfplumber`**.

* **Preservação de Leitura:** Utiliza-se a extração geométrica de caixas de texto (`layout=True`) para evitar que textos dispostos em duas colunas (ex: layouts de revistas literárias ou edições especiais) sejam fundidos horizontalmente de forma incorreta.
* **Detecção de Elementos Estruturais:** Mapeia tamanhos e pesos de fontes para identificar títulos de capítulos e seções, convertendo-os nativamente para sintaxe Markdown (`#`, `##`).

---

### 3. Tratamento de PDFs Digitalizados (Escaneados / Sem Camada de Texto)

Para manuscritos antigos ou pareceres físicos digitalizados sem camada de texto:

1. **Verificação Inicial:** O pipeline calcula a densidade de texto nativo por página (`len(text) / page_area`). Se a densidade for próxima de zero, a página é classificada como imagem rasterizada.
2. **Pipelines de OCR:**
* **Fluxo Padrão (Alto Volume):** Renderização da página em 300 DPI via `pdf2image` e aplicação do **`Tesseract OCR`** configurado para o idioma português (`lang='por'`).
* **Fluxo de Alta Complexidade (Caligrafia/Fontes Raras):** Envio da imagem da página para modelos de visão (**`GPT-4o`** ou **`Claude 3.5 Sonnet`**) solicitando transcrição direta e estruturação sintática em Markdown.



---

### 4. Tratamento de Tabelas

**É fundamental manter a estrutura das tabelas.** No ambiente editorial, tabelas aparecem em fichas catalográficas, cronogramas de lançamentos e tabelas comparativas de vendas/público nos *reader reports*.

* **Extração:** `pdfplumber` identifica as linhas e colunas de grade da tabela.
* **Conversão:** A tabela extraída é convertida para **Markdown Table** ou um objeto **JSON inline** dentro do texto do *chunk*:

```markdown
| Parâmetro | Avaliação do Parecerista |
| :--- | :--- |
| Ritmo de Leitura | Rápido / Flutuante |
| Público-Alvo | Jovem Adulto (16-24 anos) |
| Potencial Comercial | Alto |

```

* **Justificativa:** Representar tabelas como texto puro desalinhado faz com que o LLM perca a associação entre chave e valor (ex: associar "Ritmo de Leitura" à nota "Alto" em vez de "Rápido").

---

### 5. Tratamento de Imagens Soltas e Capas

Imagens brutas em pixels não podem ser convertidas diretamente em embeddings vetoriais de texto. A estratégia de descarte/aproveitamento inclui:

* **Ilustrações Decorativas e Vinhetas Internas:** **Descartadas.** Vinhetas de início de capítulo, bordas e marca-páginas não agregam valor semântico à análise literária e poluem o pipeline.
* **Capas de Livros e Ilustrações de Enredo:** **Processadas via Vision LLM.** A capa de um livro contém informações cruciais de design, paleta de cores e elementos visuais que transmitem o tom da obra.
* *Ação:* A imagem da capa é enviada a um modelo multimodal para gerar uma descrição textual (*captioning*) gravada no metadado da obra:
> *"Descrição Visual da Capa: Ilustração vetorial em tons escuros de azul e violeta, mostrando uma silhueta feminina diante de uma casa isolada sob neblina. Transmite tom de suspense, mistério e isolamento."*





---

### 6. Tratamento de Documentos Multimodais

Muitas campanhas editoriais modernas acompanham materiais audiovisuais (audiolivros, entrevistas de autores em podcasts, vídeos de *booktrailers*).

* **Áudios (Entrevistas / Audiolivros):** Processados pelo **`Whisper`** (OpenAI) para gerar a transcrição textual completa com marcação de tempo (*timestamps*). O texto transcrito entra no pipeline como um relatório secundário da obra.
* **Vídeos (Booktrailers / Entrevistas Gravadas):**
1. O áudio é extraído via `ffmpeg` e transcrito pelo `Whisper`.
2. Frames-chave do vídeo (amostrados a cada 5 segundos ou em mudanças de cena) são analisados por um modelo de visão para descrever o apelo visual da campanha de marketing.



---

### 7. Problemas Comuns e Caso Concreto de Falha

#### Problemas Potenciais na Extração:

* **Hifenização de Quebra de Linha:** Palavras divididas no final da linha (ex: `recomen- / dação`) viram dois tokens desconexos (`recomen` e `dação`) se não forem higienizadas.
* **Lixo de OCR em Páginas Amareladas:** Manuscritos antigos escaneados geram caracteres aleatórios (ex: `1ívr0`, `@ut0r`).
* **Fusão de Cabeçalho/Rodapé no Texto:** Títulos de capítulos repetidos no topo de todas as páginas são extraídos no meio de frases, quebrando o sentido do parágrafo.

#### Caso Concreto de Falha em Atividades Anteriores:

> **O Cenário:** Ao extrair um relatório editorial em PDF formatado em duas colunas, uma ferramenta de extração simples (`pypdf` sem análise geométrica) leu a página da esquerda para a direita cobrindo a largura total da folha.
> **O Resultado:** O sistema fundiu a linha 1 da Coluna A com a linha 1 da Coluna B, criando frases sem nexo semântico (ex: *"O protagonista caminha pela floresta quando o mercado editorial em 2024 encontrou um destino trágico projetou um crescimento de 5%"*).
> **A Solução:** Substituição da biblioteca por `pdfplumber` com agrupamento de palavras por caixa delimitadora (*bounding box*), forçando a extração vertical da Coluna A completa antes de iniciar a extração da Coluna B.


# Parte 3.2 - Limpeza e Normalização

## Cenário B: Assistente de Curadoria Editorial e Recomendação Literária

### 1. O que precisa ser removido?

* **Cabeçalhos e Rodapés Repetidos:** Títulos da obra, nome do autor e nome da editora impressos na margem superior ou inferior de cada página de provas e manuscritos em PDF.
* **Numeração de Página Física:** Números isolados no início ou fim das páginas (ex: *"Página 142 de 380"* ou apenas *"142"*), que perdem a utilidade após a fragmentação em *chunks*.
* **Marcas d'Água de Segurança:** Frases de segurança sobrepostas ao texto em provas e manuscritos não publicados (ex: *"CÓPIA CONFIDENCIAL - USO INTERNO EDITORIAL"*, *"PROVA NÃO REVISADA"* ou dados de identificação do parecerista).
* **Páginas Pré-Textuais e Pós-Textuais Irrelevantes:** Páginas em branco, dados de licenças de fontes tipográficas, avisos legais de marca registrada, informações sobre a gráfica/impressão (colofão) e listas de agradecimentos comerciais.
* **Sumários e Índices Remissivos Rígidos:** A listagem estática de capítulos vinculada a páginas físicas (ex: *"Capítulo 4: O Encontro .................... 89"*). Manter o sumário numérico confunde o motor vetorial, pois cria correspondências com números de página que não existirão no banco de vetores.
* **Lixo de OCR e Caracteres de Controle:** Caracteres de quebra de página (`\f`), símbolos aleatórios gerados no escaneamento de manuscritos antigos (ex: `1ívr0`, `@ut0r`, `|`, `°`) e artefatos visuais de bordas digitalizadas.

---

### 2. O que precisa ser padronizado?

* **Codificação de Texto (*Encoding*):** Conversão estrita de 100% do acervo para o padrão **UTF-8**, eliminando falhas de renderização de caracteres (*mojibake*).
* **Normalização Unicode e Acentuação:** Aplicação da normalização Unicode (NFC) para garantir representação idêntica em bytes para caracteres acentuados em português (`ç`, `ã`, `é`) e nomes próprios estrangeiros.
* **Pontuação Tipográfica e Caracteres Literários:**
* Aspas tipográficas (`“` e `”`) padronizadas para aspas simples ou duplas padrão (`"`).
* Travessões longos de diálogo (`—` ou `–`) convertidos para um padrão único (`-` ou `—`), garantindo que o tokenizador identifique trocas de turno em diálogos de forma consistente.
* Reticências tipográficas (`…`) expandidas para três pontos (`...`).


* **Quebras de Linha e Estrutura de Parágrafos:**
* Remoção de quebras de linha artificiais geradas pelas margens fixas do PDF (reunindo linhas que pertencem ao mesmo parágrafo).
* Preservação estrita das quebras duplas de linha (`\n\n`), fundamentais para delimitar parágrafos e transições narrativas.


* **Hifenização de Margem:** Reconstrução de palavras divididas no fim da linha via expressões regulares acopladas a dicionários ortográficos em português (ex: `recomen- \n dação` -> `recomendação`).
* **Espaçamento em Branco:** Eliminação de espaços múltiplos consecutivos (`"   "` -> `" "`) e remoção de tabulações desnecessárias (`\t`).

---

### 3. Informações em Risco de Perda por Sobre-limpeza (*Over-cleaning Risks*)

* **Perda de Mudanças de Cena e Ritmo Narrativo:** Na literatura, a transição entre cenários ou saltos temporais é sinalizada por asteriscos isolados (`* * *`) ou por uma linha em branco dupla sem texto. Se a rotina de limpeza remover esses delimitadores por considerá-los "caracteres soltos" ou "espaço em branco excessivo", o pipeline fundirá duas cenas distintas no mesmo *chunk*, misturando locais e tempos narrativos.
* **Descaracterização do Estilo e Voz do Autor:** Determinados autores utilizam intencionalmente ortografia arcaica, neologismos, falta de pontuação (técnica de fluxo de consciência) ou escrita em caixa baixa. Corrigir ou "normalizar" a gramática desses textos elimina a identidade estilística da obra, impedindo que o assistente responda a perguntas sobre o tom ou estilo literário do autor.
* **Eliminação de Notas de Rodapé Relevantes:** Em ensaios, biografias, edições críticas e ficções históricas, as notas de rodapé do tradutor ou do editor contêm explicações contextuais vitais. Apagar notas de rodapé na limpeza faz com que o modelo perca o contexto histórico de termos e eventos narrados.
* **Perda de Ambiguidade de Diálogos:** A remoção de marcações de margem ou nomes de personagens em notas laterais pode tornar confuso quem é o locutor em sequências de diálogos curtos, fazendo o LLM atribuir falas ao personagem errado no momento da geração.


### 3.3 Detalhamento da Frequência de Ingestão e Ciclo de Vida

No ambiente editorial, a ingestão de dados precisa acompanhar o ritmo de produção de novos lançamentos e o fluxo continuo de avaliação de manuscritos, equilibrando o tempo de processamento com o custo de chamadas de API.

---

#### Como o pipeline roda e com que frequência chegam novos documentos?

* **Modo de Execução:** O pipeline opera de forma **híbrida: Orientada a Eventos (*Event-Driven*) e Agendada (*Cron Job*)**.
1. **Orientada a Eventos (Sob Demanda via File Watcher / Webhook do CMS):** Quando um parecerista envia um novo relatório de leitura (`.md` ou `.docx`) para a pasta de avaliação, ou quando o time de produção envia a versão final de um livro (`.epub`), um serviço monitor (*File Watcher*) detecta a adição do arquivo e dispara o pipeline imediatamente para aquele documento específico.
2. **Agendada (Noturna / Batch Cron Job):** Um *Cron Job* roda diariamente às 02:00 AM para sincronizar o banco de metadados do ERP da editora (preços, status de catálogo, atualizações de ISBN) com as fichas `.json` e verificar eventuais falhas de sincronização na Vector Store.


* **Frequência de Chegada de Novos Documentos:**
* **Relatórios de Leitura e Manuscritos (*Fluxo Contínuo*):** Chegada de 15 a 30 novos relatórios (*reader reports*) por semana, enviados pela equipe de pareceristas.
* **Novos Livros Publicados (*Lançamentos*):** Entrada de 5 a 20 novos títulos finalizados por mês, conforme o cronograma do plano editorial.



---

#### Reprocessamento: Apenas o documento atualizado ou a base inteira?

* **Estratégia Escolhida:** Reprocessamento **Incremental (Apenas o Documento Alterado)**.
* **Por que não reprocessar a base inteira?** Reprocessar um acervo de milhares de livros (centenas de milhares de *chunks*) a cada nova edição ou alteração de parecer geraria um custo altíssimo e desnecessário com APIs de Embeddings e extração de metadados via LLM, além de aumentar desnecessariamente a latência da busca.

---

#### Como o sistema sabe qual documento reprocessar?

O controle de alteração e idempotência é feito por **Hash de Conteúdo (SHA-256) + Manifesto de Ingestão**:

1. **Cálculo do Hash no Início da Carga:**
Quando a rotina de ingestão lê um arquivo no acervo, ela gera uma assinatura digital única com base no seu conteúdo (`SHA-256`).
2. **Checagem na Tabela de Controle (Manifesto de Ingestão em SQLite/Redis):**
O sistema consulta o manifesto de ingestão da editora:
* **Arquivo Novo (Hash inexistente):** Executa a esteira completa (extração de texto, LLM de metadados, chunking, embedding e gravação de novos vetores).
* **Arquivo Idêntico (Hash e caminho idênticos):** O arquivo é ignorado pela rotina de carga (*noop*).
* **Arquivo Modificado (Mesmo `document_id` / ISBN, mas Hash diferente):**
* O sistema busca na Vector Store (Qdrant/ChromaDB) todos os vetores antigos vinculados àquele `document_id` ou `isbn`.
* Executa a **deleção lógica/física dos vetores antigos** daquela versão específica.
* Gera os novos *chunks*, recalcula os embeddings da nova versão e realiza a inserção dos vetores atualizados (*Upsert*), atualizando a tag `is_latest: true`.


# Parte 4 - Metadados

## Cenário A: Assistente de Scouting e Análise Tática para Franquia da NBA

### 4.1 Metadados do Documento
Os metadados em nível de documento registram as propriedades bibliográficas e administrativas do arquivo no momento da ingestão. Eles funcionam como a camada primária de filtragem pré-busca (Pre-Retrieval Filtering), permitindo isolar o acervo por status de publicação, gênero, público-alvo ou nível de acesso antes da execução da busca por similaridade vetorial.

Aqui está o detalhamento completo dos **Metadados do Documento (Parte 4.1)** adaptado especificamente para os livros da saga **Harry Potter**:

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

---

### Justificativa dos Campos Escolhidos

* **Campos Padrão (`document_id`, `title`, `author`, `source`, `document_type`, `created_at`, `updated_at`, `category`):** Mantêm a rastreabilidade administrativa e garantem a integridade das chamadas de *upsert*, atualização ou exclusão no banco de vetores.
* **`isbn` (`string`):** Código comercial da edição (ex: `9788532511010` para a edição da Editora Rocco). Permite cruzar dados com sistemas externos da editora (vendas, estoque, direitos).
* **`genero_principal` e `subgeneros` (`string` / `list`):** Permitem filtrar o acervo por categorias amplas (ex: *"Fantasia"*) ou específicas (ex: *"Aventura"*, *"Magia"*).
* **`ordem_serie` e `nome_serie` (`integer` / `string`):** Cruciais para sagas literárias. Garantem que o sistema saiba a cronologia correta da história (Volume 1 de *Harry Potter*), evitando *spoilers* de livros posteriores e permitindo consultas ordenadas.
* **`ano_publicacao` e `idioma_original` (`integer` / `string`):** Registram o ano de lançamento original (`1997`) e a variante do idioma (`en-GB`), ajudando no rastreio de edições e adaptações.
* **`tradutor` (`string`):** Identifica o responsável pela versão em português (ex: *Lya Wyler*). Importante para garantir a consistência de termos adaptados na tradução oficial do Brasil (ex: *Quadribol*, *Sonserina*, *Dementadores*).
* **`status_direitos` (`string`):** Indica se os direitos de publicação estão `ativo`. Impede o sistema de recomendar obras cujo contrato com a marca já tenha expirado.
* **`publico_alvo` (`string`):** Classificação indicativa (`Infantojuvenil`). Garante que as recomendações respeitem a faixa etária do leitor.
* **`is_latest` e `nivel_acesso` (`boolean` / `string`):** `is_latest: true` assegura que a busca só retorne a edição mais recente revisada, enquanto `nivel_acesso: "publico_geral"` libera o documento para consultas de leitores no aplicativo final.


# Parte 4.2 - Metadados do Chunk (Caso "Harry Potter")

## 1. Schema JSON Final do Chunk

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

---

## 2. Justificativa de Cada Metadado Escolhido

* **`document_id` (`string`):** Vínculo com o documento pai no acervo. Permite rastrear a qual livro exato o trecho pertence.
* **`chunk_id` (`string`):** Identificador único do vetor na Vector Store (formato `<doc_id>-c<index>`). Essencial para operações de atualização (*upsert*) e exclusão direcionada.
* **`chunk_index` (`integer`):** Índice sequencial do bloco na narrativa. Permite buscar os blocos anterior e posterior (*Adjacent Chunk Retrieval*) para reconstruir cenas longas sem perda de contexto.
* **`page` (`integer`):** Número da página física correspondente na edição de referência. Indispensável para citação precisa da fonte.
* **`section` (`string`):** Nome/número do capítulo de onde o trecho foi retirado (ex: *"Capítulo 7: O Chapéu Seletor"*). Dá contexto imediato de em qual ponto do livro o evento ocorre.
* **`document_type` (`string`):** Identifica a natureza da fonte (`livro_integral`, `reader_report`, `ficha_catalografica`). Evita misturar texto do livro com pareceres de editores.
* **`nome_serie` / `ordem_serie` (`string` / `integer`):** Permite filtrar a busca por saga e volume (ex: apenas o Volume 1 de *Harry Potter*). Evita misturar acontecimentos de livros diferentes da mesma série e previne *spoilers*.
* **`genero_principal` / `publico_alvo` (`string`):** Herdados do documento para permitir filtros booleanos de alta performance diretamente no índice vetorial.
* **`temas_chave` (`list[string]`):** Tópicos conceituais abordados no trecho. Permite localizar cenas por afinidade temática (ex: *"Pertencimento"*).
* **`elementos_mágicos` (`list[string]`):** Entidades, feitiços, artefatos ou locais citados no trecho (ex: *"Chapéu Seletor"*, *"Gryffindor"*). Aumenta dramaticamente a precisão ao buscar termos do universo bruxo.
* **`tom_narrativo` (`string`):** A atmosfera emocional da cena (ex: *"Mágico, Misterioso"*). Permite buscar trechos por clima e ritmo.
* **`is_latest` (`boolean`):** Garante a recuperação apenas de edições e pareceres vigentes/homologados.
* **`nivel_acesso` (`string`):** Controla quem pode visualizar o trecho, impedindo que leitores finais no aplicativo acessem dados sigilosos da editora.

---

## 3. Respostas às Perguntas do Projeto

### Quais metadados você usaria para filtrar a busca? Dê um exemplo de pergunta em que o filtro é indispensável.

* **Metadados de Filtro:** `nome_serie`, `ordem_serie`, `publico_alvo`, `genero_principal`, `document_type`, `is_latest` e `nivel_acesso`.
* **Exemplo de Pergunta em que o Filtro é Indispensável:**
> *"No primeiro livro de Harry Potter, em qual cena e capítulo o protagonista descobre a qual casa de Hogwarts ele pertence?"*


* **Por que o filtro é indispensável?**
Sem os filtros `nome_serie == "Harry Potter"`, `ordem_serie == 1` e `document_type == "livro_integral"`, a busca por similaridade vetorial traria trechos do livro 5 ou 7 (onde a seleção do Chapéu é relembrada em *flashbacks* ou conversas) ou pareceres críticos de editores analisando o capítulo. Com o filtro, a busca foca **exclusivamente** no texto original do Volume 1 (*Pedra Filosofal*).

---

### Quais metadados você usaria para citar a fonte ao usuário? O que exatamente apareceria na tela junto da resposta?

* **Metadados para Citação:** `document_id` (via pai -> `title` e `author`), `section`, `page` e `ordem_serie`.
* **O que apareceria na tela do usuário (Exemplo de Interface):**

> **Resposta do Assistente:**
> *"Harry descobre sua casa durante a cerimônia de abertura em Hogwarts, quando o Chapéu Seletor pondera entre a Sonserina e a Grifinória, decidindo finalmente enviá-lo para a Grifinória após ouvir o desejo do garoto."*
> 📌 **Fonte Consultada:**
> 📖 **Obra:** *Harry Potter e a Pedra Filosofal* (Volume 1) — J.K. Rowling
> 📍 **Localização:** *Capítulo 7: O Chapéu Seletor* (Pág. 108)
> 🏷️ **Categoria:** *Texto Integral — Catálogo Publicado*

---

### Que metadado seria caríssimo de acrescentar depois que a base já estivesse indexada? Por quê?

* **Metadado Caríssimo:** **`temas_chave`**, **`elementos_mágicos`** e **`tom_narrativo`**.
* **Por quê?**
Metadados estruturados (como `page` ou `section`) podem ser lidos dos arquivos originais por scripts em instantes. No entanto, preencher retroativamente os campos `temas_chave`, `elementos_mágicos` e `tom_narrativo` exige reprocessar o texto de cada *chunk* individual através de um LLM treinado com *Structured Outputs*.
Considerando que os 7 livros de *Harry Potter* geram cerca de **4.500 chunks**, reanalisar toda a saga exigiria **4.500 chamadas de API de LLM**, gerando um custo considerável em tokens, alto tempo de execução e a necessidade de atualizar o payload de todos os vetores no banco vetorial.

---

### Como você vai extrair esses metadados?

1. **Herança do Documento e Caminho do Arquivo (Automático via Script):**
* `document_id`, `document_type`, `nome_serie`, `ordem_serie` e `publico_alvo` são herdados diretamente dos metadados do documento pai no início do processo.


2. **Parsing Estrutural do Arquivo `.epub` (Parsing de Tags):**
* `section` (título do capítulo) e `chunk_index` são extraídos inspecionando a hierarquia de tags HTML do arquivo EPUB (`<h1>`, `<section>`).
* `page` é calculada com base no mapa de páginas estáticas ou marcadores de quebra de página do EPUB.


3. **Extração Semântica por LLM (Structured Output):**
* Cada bloco de texto extraído é enviado a um LLM leve (`gpt-4o-mini`) configurado com **Pydantic / JSON Schema**, que lê o trecho e extrai automaticamente as listas `temas_chave`, `elementos_mágicos` e a string `tom_narrativo` para popular o registro antes da vetorização.

# Parte 5 - Chunking / Splitting

No contexto de um assistente de acervo editorial e recomendação literária focado na saga **Harry Potter** e em outros manuscritos do catálogo, o processo de *chunking* (fragmentação) é a ponte crucial entre o texto original e a capacidade da busca vetorial de recuperar passagens com alta precisão semântica e narrativa.

---

## Estratégia de Splitting Definia

### 1. Qual estratégia de splitting você utilizaria?

Utilizaremos o **Recursive Character Text Splitter estruturado por separadores literários e semânticos**. Para obras literárias e manuscritos editoriais, a fragmentação não pode quebrar cenas, diálogos ou descrições no meio de frases. Por isso, a divisão respeita a hierarquia natural do texto (capítulos, parágrafos e pontuação de diálogos).

### 2. Qual tamanho aproximado dos chunks?

* **Tamanho Alvo:** **1.000 a 1.200 caracteres** (~150 a 200 palavras).
* **Justificativa Literária:** Em obras como *Harry Potter*, um parágrafo longo ou um bloco de diálogo descritivo tem em média de 100 a 200 palavras. Esse tamanho é suficiente para capturar a essência de uma cena curta (ex: o Chapéu Seletor ponderando sobre a casa de Harry, a descrição do Salão Principal ou o primeiro feitiço na aula de Poções) sem diluir o significado nem ultrapassar o limite de contexto dos modelos de embedding.

### 3. Utilizaria overlap? Quanto?

* **Sim, overlap de 150 a 200 caracteres** (~15% a 20% do tamanho do chunk).
* **Justificativa:** Em narrativas, a continuidade causal entre frases e diálogos é fundamental. O *overlap* garante que a transição entre dois blocos não 'corte' o sujeito de uma ação, a resposta de um diálogo (ex: a fala de Hagrid respondendo a Harry) ou o modificador de uma cena.

### 4. A divisão seria por caracteres, palavras, sentenças, parágrafos ou seções?

A divisão é **hierárquica**, priorizando seções e parágrafos, e caindo para sentenças ou caracteres apenas em casos estritos:

1. **Primeira prioridade:** Quebra por seções/capítulos (`\n\nCapítulo`, `\n\n#`).
2. **Segunda prioridade:** Quebra por parágrafos duplos (`\n\n`).
3. **Terceira prioridade:** Quebra por linhas/falas de diálogo (`\n`).
4. **Quarta prioridade:** Quebra por sentenças/pontuação final (`. `, `! `, `? `).
5. **Último recurso:** Quebra por palavras/espaços (` `).

### 5. Utilizaria um splitter recursivo?

**Sim.** O `RecursiveCharacterTextSplitter` tenta fragmentar o texto no maior divisor semântico possível (como parágrafos duplos). Se o parágrafo ultrapassar os 1.200 caracteres, o splitter recursivamente tenta quebrá-lo no divisor menor seguinte (linhas, depois frases), garantindo que nenhum bloco ultrapasse o limite máximo estabelecido.

### 6. Utilizaria uma estratégia específica para cada tipo de documento? Um contrato e uma transcrição de call center pedem o mesmo tratamento?

**Com certeza. Cada tipo de documento exige um pipeline e um tratamento de chunking completamente diferentes.**

* **Livros Literários (ex: *Harry Potter*):** Chunking **semântico/narrativo recursivo** (1.000–1.200 caracteres) baseado em capítulos e parágrafos. Foco na preservação da cena e do tom.
* **Pareceres Editoriais / Reader Reports:** Chunking **baseado em seções Markdown/JSON**. O parecer já possui subseções rígidas (ex: *"Resumo da Trama"*, *"Análise de Personagens"*, *"Potencial Comercial"*). O chunking deve respeitar cada subseção inteira para não misturar a análise técnica com o resumo da história.
* **Contratos Literários / Contratos de Direitos Autorais:** Chunking **estruturado por cláusulas/artigos** (ex: *Cláusula 1ª - Da Cessão de Direitos*). Cortar uma cláusula ao meio anula seu sentido jurídico e gera riscos de alucinação jurídica.
* **Transcriações de Call Center / Reuniões Editoriais:** Chunking **baseado em turnos de fala (*Turn-taking Chunking*)**. Cada bloco agrupa a fala do interlocutor e a resposta do atendente/editor, mantendo o contexto da interação humana.

---

## Respostas às Perguntas do Projeto

### 1. O que pode acontecer se os chunks forem muito pequenos?

* **Perda de Contexto Semântico:** Chunks de 50 a 100 caracteres (ex: apenas a frase *"— Sonserina não, eh?"*) perdem a informação de **quem** está falando, **onde** está falando e **por quê**.
* **Ruído na Busca Vetorial:** O vetor gerado fica fraco e ambíguo, gerando correspondências falsas-positivas (*false positives*) durante a busca.
* **Respostas Incompletas da IA:** A LLM recebe apenas pedaços desconexos e fica incapaz de fornecer uma explicação rica e fundamentada sobre a obra.

### 2. O que pode acontecer se os chunks forem muito grandes?

* **Efeito "Agulha no Paliteiro" (*Diluição Semântica*):** Se o chunk tiver 8.000 caracteres (um capítulo inteiro de *Harry Potter*), a representação vetorial representará a média de todos os assuntos do capítulo. Uma busca por um detalhe específico (ex: *"Qual o nome do sapo de Neville?"*) terá uma pontuação de similaridade muito baixa porque o detalhe se perdeu no meio de milhares de palavras.
* **Custo Elevado de Tokens e Latência:** O envio de chunks gigantescos para a LLM consome a janela de contexto desnecessariamente e aumenta o tempo de resposta e a fatura da API.
* **Citação Imprecisa:** Ao citar a fonte na interface, o sistema indicará um bloco enorme em vez de apontar para a cena exata.

### 3. Como você trataria uma tabela na hora de dividir? Uma tabela cortada ao meio ainda significa alguma coisa? E uma imagem?

* **Tratamento de Tabelas:**
* **Uma tabela cortada ao meio perde totalmente seu significado relacionacional** (as colunas perdem a associação com os cabeçalhos).
* **Solução:**
1. **Conversão para Markdown / HTML:** Converter a tabela para texto estruturado.
2. **Chunking de Tabela Inteira (*Atomic Table Chunking*):** Tratar a tabela como um objeto atômico indivisível.
3. **Injeção de Cabeçalho (*Header Injection*):** Se a tabela for inevitavelmente maior que o limite do chunk, repetir a linha de cabeçalho (`Header`) em **todos** os sub-chunks da tabela para preservar o contexto das colunas.




* **Tratamento de Imagens e Ilustrações (ex: mapas de Hogwarts, ilustrações de capítulos):**
* **Uma imagem pura não possui vetor de texto.**
* **Solução:**
1. **Descrição Visual por Multimodalidade (Vision LLM / Image-to-Text):** Durante a ingestão, a imagem (como o mapa dos Marotos ou a capa do livro) passa por um modelo visual que gera uma descrição textual detalhada (`caption`).
2. **Armazenamento:** A descrição em texto é indexada no chunk com o metadado `is_image: true` e a URL/caminho do arquivo de imagem original, permitindo que a imagem seja recuperada e exibida na interface do usuário quando a cena for citada.





---

### 4. Como saber se a sua escolha de chunking foi boa? Que evidência você juntaria para provar isso?

Para provar que a escolha do chunking foi boa, juntaríamos evidências quantitativas e qualitativas atreladas a um **Framework de Avaliação RAG (ex: Ragas / TruLens)**:

#### 1. Métricas Quantitativas de Retrieval (Evidência Numérica)

* **Hit Rate / Recall@K:** Medir a porcentagem de vezes que o chunk correto (contendo a resposta exata sobre o livro) aparece entre os Top-K resultados recuperados. Um chunking ideal eleva o *Recall@5* para acima de 90%.
* **Context Precision (Precisão de Contexto):** Medir a proporção de texto útil vs. texto irrelevante nos chunks recuperados. Chunks bem dimensionados têm alta densidade de informação relevante.
* **MRR (Mean Reciprocal Rank):** Avaliar se o chunk mais relevante aparece na primeira posição da busca vetorial.

#### 2. Testes de Estresse com Consultas Reais (Dataset de Teste / Golden Dataset)

Montaríamos um *Golden Dataset* com 100 perguntas representativas do acervo de *Harry Potter*, divididas em três níveis de complexidade:

* **Perguntas Fatuais/Pontuais:** *"Qual o número da plataforma de trem em King's Cross?"* (Mede se o chunk não diluiu o detalhe).
* **Perguntas de Diálogo/Cena:** *"O que Dumbledore disse a Harry em frente ao Espelho de Ojesed?"* (Mede se o chunk preservou a continuidade do diálogo).
* **Perguntas Temáticas/Sintéticas:** *"Como é descrita a atmosfera da casa Sonserina ao longo do primeiro livro?"* (Mede se os chunks recuperados cobrem o tema sem trazer ruído).

#### 3. Evidência de Ausência de Fragmentação de Informação (*Boundary Failure Rate*)

Coletaríamos métricas de respostas geradas pela LLM avaliando se houve **cortes na resposta** por falta de contexto (ex: a LLM responder *"O texto não menciona quem ganhou a partida porque a frase é cortada"*). Uma taxa de falha de borda (*boundary failure*) próxima de **0%** é a evidência definitiva de que o tamanho do chunk e o *overlap* foram configurados corretamente.


# Parte 6 - Embeddings

Para atender ao ecossistema da editora (aplicativo de recomendação literária para leitores finais e dashboard de avaliação editorial interna com foco na saga *Harry Potter* e manuscritos), adotamos uma estratégia baseada em dois cenários funcionais: **Cenário A (Público/Catálogo Recomendação)** e **Cenário B (Interno/Avaliação Editorial e Manuscritos Sigilosos)**.

---

### Tabela Comparativa de Modelos de Embeddings

| Item | Cenário A: Recomendação Literária (Público) | Cenário B: Avaliação de Manuscritos & Sigilo (Interno) |
| --- | --- | --- |
| **Modelo escolhido** | **text-embedding-3-large** (OpenAI) | **multilingual-e5-large** (Microsoft) |
| **Dimensão do embedding** | 3.072 (configurável via *Matryoshka* para 1.536 ou 256) | 1.024 |
| **Suporta português?** | Sim (suporte nativo e otimizado) | Sim (desempenho elevado em PT-BR) |
| **É multilíngue?** | Sim | Sim (suporta mais de 100 idiomas) |
| **Tamanho máximo de entrada** | 8.191 tokens | 512 tokens (~1.500 a 2.000 caracteres) |
| **É open source?** | Não (Proprietário) | Sim (Licença MIT) |
| **Pode ser executado localmente?** | Não | Sim (via Hugging Face / ONNX / vLLM) |
| **Possui API?** | Sim (API oficial da OpenAI) | Sim (via Inference Endpoints ou servidor próprio) |
| **Custo aproximado** | US$ 0,00013 / 1.000 tokens | Gratuito (custo apenas de infraestrutura GPU) |
| **Fonte da informação (link)** | [OpenAI Embeddings Documentation](https://platform.openai.com/docs/guides/embeddings) | [Hugging Face - intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large) |

---

### Por que cada modelo é adequado ao seu cenário?

* **Cenário A (`text-embedding-3-large`):** É ideal para a interface de recomendação literária do público geral. Oferece alta capacidade semântica para capturar nuances estilísticas e temáticas da saga *Harry Potter* e de outros romances em português. Suas dimensões flexíveis via *Matryoshka Representation Learning* permitem reduzir a dimensão para 1.536 sem perda significativa de precisão, economizando memória e custos de armazenamento no banco de vetores.
* **Cenário B (`multilingual-e5-large`):** É a escolha perfeita para o ambiente interno da editora (análise de pareceres e manuscritos inéditos). Por ser um modelo *open source* executável localmente, garante **privacidade total e conformidade com a LGPD**, impedindo o vazamento de obras não publicadas para APIs de terceiros. Além disso, apresenta desempenho no Benchmark MTEB (*Massive Text Embedding Benchmark*) para tarefas multilíngues e de recuperação de documentos em português.

---

### Respostas às Perguntas do Projeto

#### 1. Considerou algum modelo alternativo e descartou? Qual, e por quê?

* **Alternativa Considerada:** `text-embedding-ada-002` (OpenAI) e `bge-large-en-v1.5` (BAAI).
* **Motivos do Descarte:**
* O `text-embedding-ada-002` foi descartado por ser um modelo de geração anterior, apresentando desempenho inferior em testes multilíngues em português se comparado ao `text-embedding-3-large`, além de possuir dimensões fixas sem suporte a redução dinâmica.
* O `bge-large-en-v1.5` foi descartado porque sua otimização primária é focada no idioma inglês, apresentando degradação ao lidar com expressões idiomáticas e nuances do português do Brasil presente nas traduções de *Harry Potter* e nos relatórios de leitura nacionais.



#### 2. Se o cenário envolve documentos sigilosos, isso muda sua escolha entre modelo local e API? Como?

* **Sim, altera fundamentalmente a arquitetura.**
* **Mudança Prática:** Manuscritos inéditos e contratos de direitos autorais envolvem propriedade intelectual sensível e acordos de confidencialidade (NDA). Para o Cenário B, **o uso de APIs de terceiros é descartado em favor de modelos executados localmente (`multilingual-e5-large`)**.
* Ao hospedar o modelo localmente (em servidores *on-premises* ou em uma VPC privada na nuvem), nenhum texto não publicado sai da infraestrutura controlada pela editora, eliminando o risco de vazamento de dados ou uso indevido para treinamento de LLMs comerciais.

#### 3. O tamanho máximo de entrada do modelo tem relação com a sua decisão de chunking da Parte 5? Explique.

* **Sim, existe uma relação de limite absoluto e otimização semântica.**
* **Explicação:**
* No **Cenário A** (`text-embedding-3-large`), a janela de entrada é de **8.191 tokens**, permitindo absorver facilmente nossos *chunks* literários de 1.000 a 1.200 caracteres (~200 tokens).
* No **Cenário B** (`multilingual-e5-large`), o limite máximo de entrada é de **512 tokens** (~1.500 a 2.000 caracteres em português).
* A decisão tomada na Parte 5 de definir os *chunks* entre **1.000 e 1.200 caracteres** garante que o texto fique confortavelmente abaixo do limite de 512 tokens do `multilingual-e5-large`. Isso evita que o modelo trunque (*truncate*) o final das frases e perca informações cruciais de contexto durante o processo de geração do vetor.

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Comparação entre os Dois Cenários

A conclusão do projeto exige colocar lado a lado as escolhas feitas para o **Cenário A (Aplicativo de Recomendação Literária — Público Geral)** e para o **Cenário B (Avaliação Editorial e Manuscritos Sigilosos — Interno)**. A análise a seguir detalha onde as arquiteturas se distanciam, onde convergem e a justificativa estratégica para cada decisão.

---

## 1. Em que pontos as decisões foram diferentes? Por quê?

| Etapa | Cenário A (Público / Recomendação) | Cenário B (Interno / Manuscritos) | Por que são diferentes? |
| --- | --- | --- | --- |
| **Infraestrutura e Execução** | Cloud / SaaS (APIs comerciais da OpenAI e Qdrant Cloud) | *On-Premises* / VPC Privada (Docker, vLLM e Qdrant Local) | **Garantia de Sigilo e LGPD:** O Cenário B lida com manuscritos inéditos e propriedade intelectual sensível. NENHUM dado não publicado pode trafegar para APIs de terceiros. |
| **Modelo de Embeddings** | `text-embedding-3-large` (Proprietário) | `multilingual-e5-large` (Open Source / Local) | **Desempenho Comercial vs. Privacidade:** O Cenário A busca a máxima riqueza semântica e flexibilidade de dimensão (Matryoshka); o Cenário B prioriza o processamento local sem perda de qualidade em português. |
| **Granularidade do Chunking** | 1.000 a 1.200 caracteres (baseado em cenas e diálogos) | 800 a 1.000 caracteres (baseado em seções e pareceres) | **Estrutura dos Documentos:** Romances possuem fluxo narrativo contínuo que exige blocos maiores; pareceres e relatórios de leitura possuem seções técnicas curtas (*Análise de Trama*, *Potencial Mercadológico*) que se perdem se misturadas. |
| **Controle de Acesso e Metadados** | Foco em categorização de público (`publico_alvo`, `genero_principal`, `temas_chave`) | Foco em controle de autorização rígida (`nivel_acesso`, `status_direitos`, `autor_pseudonimo`) | **Perfil do Usuário Final:** O leitor quer descobrir livros por afinidade temática; o comitê editorial precisa de governança para evitar vazamentos e conflitos de interesse. |

---

## 2. Em que pontos foram iguais? Isso é sinal de boa prática geral ou de repetição sem pensar?

As arquiteturas compartilham quatro pilares fundamentais:

1. **Estratégia de Chunking Recursivo (`RecursiveCharacterTextSplitter`)**
2. **Adição de Overlap Semântico (150 a 200 caracteres)**
3. **Uso de Busca Híbrida (Vetor Denso + BM25 Esdorso)**
4. **Extração de Metadados Ricos e Estruturados**

### Análise: Boa prática geral ou repetição sem pensar?

**É um sinal de boa prática geral da arquitetura RAG moderna**, e não de repetição impensada, pelos seguintes motivos:

* **O Chunking Recursivo com Overlap** é um padrão universal para evitar a perda de contexto nas bordas do texto (*boundary failures*). Seja em um diálogo de *Harry Potter* ou em um parecer técnico, cortar uma frase no meio degrada a qualidade da busca vetorial.
* **A Busca Híbrida (Dense + BM25)** é indispensável no domínio editorial. Enquanto os vetores densos capturam o *conceito* ("livro sobre amizade em escola mágica"), o BM25 é essencial para capturar *termos exatos* do universo bruxo (ex: *"Dementador"*, *"Horcrux"*, *"Gryffindor"*). Depender apenas de vetores densos causaria falhas na busca por nomes próprios inventados.
* **A Filtragem Pré-Busca (*Pre-Retrieval Filtering*)** via metadados garante eficiência computacional. Buscar em todo o banco vetorial para depois descartar resultados é ineficiente; aplicar filtros prévios (`is_latest: true`) é uma boa prática fundamental de sistemas RAG em produção.

---

## 3. Se você tivesse que construir apenas um dos dois, qual escolheria, e por quê?

**Escolha: Cenário B (Sistema Interno de Avaliação Editorial e Gestão de Manuscritos)**

### Justificativa do Negócio e de Engenharia:

1. **Maior Retorno Financeiro e Defesa de Negócio (ROI):**
* Avaliar manuscritos e decidir publicações é a atividade-fim mais crítica de uma editora. Um erro de avaliação (rejeitar um novo fenômeno literário ou aprovar uma obra sem apelo comercial) custa centenas de milhares de reais.
* Um assistente RAG focado no comitê editorial otimiza o tempo dos pareceristas em até 60%, acelera a tomada de decisão sobre novos títulos e cria uma memória de inteligência editorial histórica.


2. **Desafio de Engenharia de IA Mais Robusto:**
* O Cenário B exige resolver o problema do **RAG On-Premises/Privado**, que é o maior desafio atual das empresas (IA com privacidade total).
* A implementação de pipelines locais de parsing, embeddings *open source*, vector stores em containers fechados e LLMs locais (*Llama 3*) cria uma infraestrutura de dados madura e proprietária que se torna um ativo valioso para a empresa.


3. **Validação Antes do Lançamento Externo:**
* Construir primeiro o sistema interno permite homologar a taxonomia de metadados, testar os algoritmos de limpeza e validar o banco vetorial dentro de casa, com usuários especialistas (editores). Uma vez consolidada essa base, estendê-la para o aplicativo público do leitor (Cenário A) torna-se um passo natural e muito mais seguro.


Como toda a arquitetura, diagramas, schemas de metadados, estratégias de *chunking* e comparações apresentadas ao longo da atividade foram construídos **de forma autônoma e analítica** a partir dos conceitos de Engenharia de RAG (*Retrieval-Augmented Generation*), não houve necessidade de realizar pesquisas externas para gerar o conteúdo.

No entanto, para que você tenha a documentação oficial dos recursos, modelos e bibliotecas de mercado citados no projeto, aqui está a **Seção de Referências e Documentações Técnicas**:

---

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



