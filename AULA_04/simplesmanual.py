import os
import re
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

print("Carregando modelo local de embeddings...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    """Gera o embedding para o texto fornecido."""
    return model.encode(text, convert_to_numpy=True)

def similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcula a Similaridade de Cosseno entre dois vetores."""
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm_v1 * norm_v2))


def carregar_arquivos_md(diretorio: str = ".") -> dict[str, str]:
    """Busca e lê os arquivos .md no diretório informado e na pasta pai se necessário."""
    documentos = {}
    path = Path(diretorio)
    
    # Procura na pasta atual e na pasta pai (caso os .md estejam em AULA_02)
    arquivos = list(path.glob("*.md")) + list(path.parent.glob("*.md")) + list(path.parent.glob("*/*.md"))
    
    for filepath in set(arquivos):
        if filepath.name.lower() not in ["readme.md", "task.md"]:
            with open(filepath, "r", encoding="utf-8") as f:
                documentos[filepath.name] = f.read()
    return documentos

def dividir_por_linhas(texto: str) -> list[str]:
    return [linha.strip() for linha in texto.split("\n") if len(linha.strip()) > 10]

def dividir_por_paragrafos(texto: str) -> list[str]:
    paragrafos = texto.split("\n\n")
    return [p.strip().replace("\n", " ") for p in paragrafos if len(p.strip()) > 20]

def dividir_por_capitulos(texto: str) -> list[str]:
    capitulos = re.split(r'\n(?=#+\s)', texto)
    return [cap.strip().replace("\n", " ") for cap in capitulos if len(cap.strip()) > 30]


def busca_semantica(query: str, trechos: list[tuple[str, str]], top_k: int = 3) -> list[dict]:
    vec_query = get_embedding(query)
    
    resultados = []
    for arquivo, trecho in trechos:
        vec_trecho = get_embedding(trecho)
        score = similaridade_cosseno(vec_query, vec_trecho)
        resultados.append({
            "Arquivo": arquivo,
            "Trecho": trecho,
            "Similaridade": score
        })
    
    resultados.sort(key=lambda x: x["Similaridade"], reverse=True)
    return resultados[:top_k]

def exibir_resultados(titulo_etapa: str, query: str, resultados: list[dict]):
    print(f"\n========================================================")
    print(f"ETAPA: {titulo_etapa}")
    print(f"QUERY: \"{query}\"")
    print(f"========================================================")
    for idx, res in enumerate(resultados, 1):
        print(f"\n[#{idx}] Score: {res['Similaridade']:.4f} | Arquivo: {res['Arquivo']}")
        trecho_exibicao = res['Trecho'][:180] + "..." if len(res['Trecho']) > 180 else res['Trecho']
        print(f"Conteúdo: {trecho_exibicao}")


documentos = carregar_arquivos_md(".")
query = "O que é autonomia e opacidade algorítmica?"

if not documentos:
    print("Nenhum arquivo .md foi encontrado para realizar a busca.")
else:
    # 1. Por Linhas
    trechos_linhas = []
    for nome, conteudo in documentos.items():
        for linha in dividir_por_linhas(conteudo):
            trechos_linhas.append((nome, linha))

    top3_linhas = busca_semantica(query, trechos_linhas, top_k=3)
    exibir_resultados("Divisão por LINHAS", query, top3_linhas)

    # 2. Por Parágrafos
    trechos_paragrafos = []
    for nome, conteudo in documentos.items():
        for paragrafo in dividir_por_paragrafos(conteudo):
            trechos_paragrafos.append((nome, paragrafo))

    top3_paragrafos = busca_semantica(query, trechos_paragrafos, top_k=3)
    exibir_resultados("Divisão por PARÁGRAFOS", query, top3_paragrafos)

    # 3. Por Capítulos
    trechos_capitulos = []
    for nome, conteudo in documentos.items():
        for capitulo in dividir_por_capitulos(conteudo):
            trechos_capitulos.append((nome, capitulo))

    top3_capitulos = busca_semantica(query, trechos_capitulos, top_k=3)
    exibir_resultados("Divisão por CAPÍTULOS / SEÇÕES", query, top3_capitulos)