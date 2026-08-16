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


  