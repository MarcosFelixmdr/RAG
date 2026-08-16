import os
import warnings
from pathlib import Path

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

print("Carregando arquivos Markdown...")
pasta = Path(".")
arquivos_md = list(pasta.glob("*.md"))

documentos = []
for fp in arquivos_md:
    if fp.name.lower() not in ["readme.md", "task.md"]:
        with open(fp, "r", encoding="utf-8") as f:
            documentos.append({"origem": fp.name, "texto": f.read()})

if not documentos:
    print("Nenhum arquivo .md encontrado na pasta!")
    exit()

print(f"✓ Total de arquivos carregados: {len(documentos)}\n")

print("Aplicando o RecursiveCharacterTextSplitter do LangChain...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       
    chunk_overlap=50, 
    length_function=len,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = []
metadados = []

for doc in documentos:
    sub_chunks = text_splitter.split_text(doc["texto"])
    for chunk in sub_chunks:
        chunks.append(chunk)
        metadados.append({"fonte": doc["origem"]})

print(f"✓ Texto total dividido em {len(chunks)} chunks.\n")

print("Carregando o modelo de Embeddings (all-MiniLM-L6-v2)...")

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

print("Gerando os vetores numéricos (embeddings) para cada chunk...")
vetores = embeddings_model.embed_documents(chunks)

print("\n=== RESUMO DO PROCESSAMENTO ===")
print(f"• Total de documentos lidos:  {len(documentos)}")
print(f"• Total de chunks criados:    {len(chunks)}")
print(f"• Total de vetores gerados:   {len(vetores)}")
print(f"• Dimensão do vetor gerado:   {len(vetores[0]) if vetores else 0} números por chunk")

print("\n--- Exemplo do primeiro chunk criado ---")
print(f"Fonte: {metadados[0]['fonte']}")
print(f"Texto: {chunks[0][:150]}...")
print(f"Vetor (primeiros 5 valores): {vetores[0][:5]}")