from langchain_core.documents import Document

documentos = [
    Document(
        page_content="Embeddings são representações vetoriais densas de texto em um espaço multidimensional.",
        metadata={
            "fonte": "aula01_embeddings.md",
            "pagina": 1,
            "tipo": "teoria",
            "tema": "embeddings",
            "autor": "Marco"
        }
    ),
    Document(
        page_content="Chunking é o processo de dividir textos longos em trechos menores e mais fáceis de processar.",
        metadata={
            "fonte": "aula02_chunking.md",
            "pagina": 3,
            "tipo": "pratica",
            "tema": "chunking",
            "autor": "Marco"
        }
    ),
    Document(
        page_content="Retrieval-Augmented Generation (RAG) recupera informações externas para enriquecer o contexto dos LLMs.",
        metadata={
            "fonte": "aula03_rag.md",
            "pagina": 5,
            "tipo": "teoria",
            "tema": "rag",
            "autor": "Marco"
        }
    ),
    Document(
        page_content="A tokenização converte sequências de texto em IDs numéricos legíveis pelos modelos de linguagem.",
        metadata={
            "fonte": "aula01_tokenizacao.md",
            "pagina": 2,
            "tipo": "teoria",
            "tema": "tokenizacao",
            "autor": "Marco"
        }
    ),
    Document(
        page_content="A divisão de documentos por parágrafos ajuda a preservar a coesão semântica original do texto.",
        metadata={
            "fonte": "aula02_chunking.md",
            "pagina": 8,
            "tipo": "pratica",
            "tema": "chunking",
            "autor": "Marco"
        }
    )
]
print("=== LISTA DE DOCUMENTOS CRIADOS ===\n")
for i, doc in enumerate(documentos, 1):
    print(f"--- Documento {i} ---")
    print(f"page_content : {doc.page_content}")
    print(f"metadata     : {doc.metadata}\n")

print(f"Resultado len(documentos): {len(documentos)}")