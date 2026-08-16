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



