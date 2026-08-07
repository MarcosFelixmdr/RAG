import os
import re
from pathlib import Path


def carregar_arquivos_md(diretorio: str = ".") -> dict[str, str]:
    """Lê todos os arquivos .md do diretório e retorna um dicionário {nome_arquivo: conteudo}."""
    documentos = {}
    path = Path(diretorio)
    for filepath in path.glob("*.md"):
        if filepath.name.lower() != "readme.md":
            with open(filepath, "r", encoding="utf-8") as f:
                documentos[filepath.name] = f.read()
    return documentos

def dividir_por_linhas(texto: str) -> list[str]:
    """Divide o texto linha por linha, removendo linhas vazias."""
    return [linha.strip() for linha in texto.split("\n") if len(linha.strip()) > 10]

def dividir_por_paragrafos(texto: str) -> list[str]:
    """Divide o texto por parágrafos (blocos separados por duas quebras de linha)."""
    paragrafos = texto.split("\n\n")
    return [p.strip().replace("\n", " ") for p in paragrafos if len(p.strip()) > 20]

def dividir_por_capitulos(texto: str) -> list[str]:
    """Divide o texto com base nos cabeçalhos Markdown (# ou ##)."""
    capitulos = re.split(r'\n(?=#+\s)', texto)
    return [cap.strip().replace("\n", " ") for cap in capitulos if len(cap.strip()) > 30]


def busca_semantica(query: str, trechos: list[tuple[str, str]], top_k: int = 3) -> list[dict]:
    """
    Recebe a query e uma lista de tuplas (nome_arquivo, texto_trecho).
    Retorna os top_k trechos mais similares.
    """
    vec_query = np.array(get_embedding(query), dtype=np.float32)
    
    resultados = []
    for arquivo, trecho in trechos:
        vec_trecho = np.array(get_embedding(trecho), dtype=np.float32)
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
        trecho_exibicao = res['Trecho'][:200] + "..." if len(res['Trecho']) > 200 else res['Trecho']
        print(f"Conteúdo: {trecho_exibicao}")


documentos = carregar_arquivos_md(".")
query = "O que é autonomia e opacidade algorítmica?"

if not documentos:
    print("Nenhum arquivo .md encontrado na pasta atual.")
else:
    trechos_linhas = []
    for nome, conteudo in documentos.items():
        for linha in dividir_por_linhas(conteudo):
            trechos_linhas.append((nome, linha))

    top3_linhas = busca_semantica(query, trechos_linhas, top_k=3)
    exibir_resultados("Divisão por LINHAS", query, top3_linhas)

    trechos_paragrafos = []
    for nome, conteudo in documentos.items():
        for paragrafo in dividir_por_paragrafos(conteudo):
            trechos_paragrafos.append((nome, paragrafo))

    top3_paragrafos = busca_semantica(query, trechos_paragrafos, top_k=3)
    exibir_resultados("Divisão por PARÁGRAFOS", query, top3_paragrafos)

    trechos_capitulos = []
    for nome, conteudo in documentos.items():
        for capitulo in dividir_por_capitulos(conteudo):
            trechos_capitulos.append((nome, capitulo))

    top3_capitulos = busca_semantica(query, trechos_capitulos, top_k=3)
    exibir_resultados("Divisão por CAPÍTULOS / SEÇÕES", query, top3_capitulos)