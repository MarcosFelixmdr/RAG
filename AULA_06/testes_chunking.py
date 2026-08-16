import re
from pathlib import Path
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

print("Carregando modelo local de embeddings...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    return model.encode(text, convert_to_numpy=True)

def similaridade_cosseno_batch(vec_query: np.ndarray, vecs_chunks: np.ndarray) -> np.ndarray:
    """Calcula a similaridade de cosseno entre a query e todos os chunks de uma vez."""
    norm_query = np.linalg.norm(vec_query)
    norm_chunks = np.linalg.norm(vecs_chunks, axis=1)
    
    norm_chunks[norm_chunks == 0] = 1e-10
    if norm_query == 0:
        norm_query = 1e-10
        
    dot_products = np.dot(vecs_chunks, vec_query)
    return dot_products / (norm_chunks * norm_query)

def carregar_conteudo_md() -> str:
    """Lê e consolida todos os arquivos .md encontrados no projeto."""
    path = Path(".")
    arquivos = list(path.glob("*.md")) + list(path.parent.glob("*.md")) + list(path.parent.glob("*/*.md"))
    textos = []
    for fp in set(arquivos):
        if fp.name.lower() not in ["readme.md", "task.md"]:
            with open(fp, "r", encoding="utf-8") as f:
                textos.append(f.read())
    return "\n\n".join(textos)

def chunk_fixo(texto: str, tamanho: int, overlap: int = 0) -> list[str]:
    chunks = []
    passo = tamanho - overlap
    if passo <= 0:
        raise ValueError("O overlap deve ser menor que o tamanho do chunk.")
    for i in range(0, len(texto), passo):
        trecho = texto[i:i + tamanho].strip()
        if len(trecho) > 10:
            chunks.append(trecho)
    return chunks

def chunk_paragrafos(texto: str) -> list[str]:
    return [p.strip().replace("\n", " ") for p in texto.split("\n\n") if len(p.strip()) > 10]

def chunk_sentencas_agrupadas(texto: str, grupo: int = 3) -> list[str]:
    sentencas = [s.strip() for s in re.split(r'(?<=[.!?])\s+', texto) if len(s.strip()) > 5]
    chunks = []
    for i in range(0, len(sentencas), grupo):
        bloco = " ".join(sentencas[i:i + grupo])
        if len(bloco) > 10:
            chunks.append(bloco)
    return chunks

def chunk_recursivo(texto: str, tamanho_alvo: int = 500) -> list[str]:
    separadores = ["\n\n", "\n", ". ", " "]
    
    def _split(txt, seps):
        if len(txt) <= tamanho_alvo or not seps:
            return [txt.strip()] if txt.strip() else []
        
        sep = seps[0]
        proximos_seps = seps[1:]
        partes = txt.split(sep)
        chunks = []
        atual = ""
        
        for p in partes:
            candidato = atual + (sep if atual else "") + p
            if len(candidato) <= tamanho_alvo:
                atual = candidato
            else:
                if atual:
                    chunks.append(atual.strip())
                if len(p) > tamanho_alvo and proximos_seps:
                    chunks.extend(_split(p, proximos_seps))
                    atual = ""
                else:
                    atual = p
        if atual.strip():
            chunks.append(atual.strip())
        return chunks

    return [c for c in _split(texto, separadores) if len(c) > 10]

def chunk_markdown_headings(texto: str) -> list[str]:
    secoes = re.split(r'\n(?=#+\s)', texto)
    return [s.strip().replace("\n", " ") for s in secoes if len(s.strip()) > 20]



texto_completo = carregar_conteudo_md()

if not texto_completo:
    print("Nenhum arquivo .md foi encontrado para realizar os testes!")
    exit()

query = "O que é autonomia e opacidade algorítmica?"
vec_query = get_embedding(query)

testes = {
    1: ("Fixo 200, sem overlap", lambda t: chunk_fixo(t, 200, 0)),
    2: ("Fixo 500, sem overlap", lambda t: chunk_fixo(t, 500, 0)),
    3: ("Fixo 1000, sem overlap", lambda t: chunk_fixo(t, 1000, 0)),
    4: ("Fixo 2000, sem overlap", lambda t: chunk_fixo(t, 2000, 0)),
    5: ("Fixo 500, overlap 50 (10%)", lambda t: chunk_fixo(t, 500, 50)),
    6: ("Fixo 500, overlap 200 (40%)", lambda t: chunk_fixo(t, 500, 200)),
    7: ("Por Parágrafo", chunk_paragrafos),
    8: ("Por Sentença (Agrupando 3)", chunk_sentencas_agrupadas),
    9: ("Recursivo (Separadores Hierárquicos)", chunk_recursivo),
    10: ("Por Seção / Heading Markdown", chunk_markdown_headings),
}

resultados = []

print(f"\nIniciando avaliação dos 10 testes para a Query: \"{query}\"\n")

for num_teste, (estrategia, func_chunk) in testes.items():
    chunks = func_chunk(texto_completo)
    
    if not chunks:
        continue

    vecs_chunks = model.encode(chunks, convert_to_numpy=True)
    scores = similaridade_cosseno_batch(vec_query, vecs_chunks)
    
    idx_best = np.argmax(scores)
    best_score = scores[idx_best]
    best_chunk = chunks[idx_best]

    resultados.append({
        "Teste": num_teste,
        "Estratégia": estrategia,
        "Total Chunks": len(chunks),
        "Top 1 Score": round(float(best_score), 4),
        "Melhor Trecho Encontrado": best_chunk[:100].replace("\n", " ") + "..."
    })

df_resultados = pd.DataFrame(resultados)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("=== TABELA COMPARATIVA DOS 10 TESTES DE CHUNKING ===")
print(df_resultados.to_string(index=False))