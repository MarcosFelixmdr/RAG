1 Tabela com o Schema Final de Metadados

Campo                           Tipo de Dado                    Descrição
fonte,                          string                          Nome do arquivo .md de origem (ex: attention_is_all_you_need.md).
documento_id                    string                          Identificador único do documento (ex: doc_attention_01).
chunk_indexv                    integer                         "Posicionamento sequencial do chunk dentro do documento (ex: 0, 1, 2...)."
estrategia                      string                          "Estratégia de chunking utilizada (ex: fixo_overlap, recursivo, paragrafo)."
chunk_size                      integer                         Configuração de tamanho máximo utilizada na divisão (ex: 500).
chunk_overlap                   integer                         Configuração de sobreposição (overlap) utilizada (ex: 50).
n_caracteres                    integer                         Contagem real do total de caracteres presentes no chunk.
secao_heading (próprio)         string                          O título ou seção do Markdown onde o trecho está localizado.
data_processamento (próprio)    string                          Data e hora em que a conversão/chunking foi executada.
idioma (próprio)                string                          "Idioma detectado no texto original do chunk (ex: pt, en)."











2. Justificativa dos Campos Próprios
secao_heading:

    Pergunta respondida: "Em qual capítulo ou seção do documento original este conceito foi mencionado?"

    Utilidade: Permite realizar filtros por tópicos específicos (ex: buscar apenas dentro de "Introdução" ou "Metodologia") e fornece um contexto mais claro para o modelo na etapa de geração.

data_processamento:

    Pergunta respondida: "Qual versão do pipeline de ingestão e chunking foi responsável por gerar este vetor?"

    Utilidade: Permite identificar chunks defasados ou reprocessar apenas documentos indexados antes de uma data específica sem precisar refazer toda a base de dados.

idioma:

    Pergunta respondida: "Este trecho está escrito em inglês, português ou em outro idioma?"

    Utilidade: Permite aplicar filtros para responder dúvidas na língua nativa do usuário ou direcionar a busca para modelos de embeddings específicos para cada idioma.




Responder:
Qual campo você incluiria se precisasse citar a fonte na resposta final do RAG, informando ao usuário exatamente de onde veio a informação?

    Eu incluiria o campo secao_heading em conjunto com fonte (e, caso o divisor capture, o número da página pagina_origem).

    Com esses dados, na hora de gerar a resposta, o sistema RAG pode formatar a citação exatamente no formato:

    "Fonte: attention_is_all_you_need.pdf, Seção '1 Introduction' (ou Página 1)."

Por que chunk_index é útil? Pense no caso em que o trecho recuperado está cortado no meio de uma explicação.

    Como o chunk_index indica a ordem sequencial exata do texto no documento original, se um trecho recuperado for cortado no meio, a aplicação RAG pode simplesmente fazer uma busca rápida no banco de dados pelos vizinhos chunk_index - 1 (chunk anterior) e chunk_index + 1 (chunk posterior).

    Isso permite implementar técnicas avançadas de RAG como a janela de contexto expansível (Parent-Child Retriever / Small-to-Big Retrieval), onde se busca por vetores menores, mas entrega-se ao LLM o contexto circundante completo.