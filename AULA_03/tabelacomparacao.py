import os
from pathlib import Path
import numpy as np
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

env_file = find_dotenv(usecwd=True)
if env_file:
    load_dotenv(env_file)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env!")

client = OpenAI(api_key=api_key)

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    text = text.replace("\n", " ").strip()
    if not text:
        return [0.0] * 1536
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def distancia_euclidiana(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return float(np.linalg.norm(vec1 - vec2))

def similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    norm_v1 = np.linalg.norm(vec1)
    norm_v2 = np.linalg.norm(vec2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm_v1 * norm_v2))

def distancia_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return float(1.0 - similaridade_cosseno(vec1, vec2))

frase_ancora = "O cachorro correu no parque e brincou com a bola."

frases_comparacao = [
    ("Similar (mesmo sentido, palavras diferentes)", "Um cão estava correndo no jardim e brincando com seu brinquedo."),
    ("Relacionado (mesmo contexto de animais)", "O gato dormiu na almofada da sala durante toda a tarde."),
    ("Diferente (outro domínio - economia)", "A taxa de juros do banco central subiu dois pontos percentuais."),
    ("Oposto/Negação", "Nenhum animal esteve no parque e o cão permaneceu preso em casa.")
]

print("Gerando embedding da frase âncora...")
vec_ancora = np.array(get_embedding(frase_ancora), dtype=np.float32)

resultados = []
print("Comparando com as outras frases...\n")
for tipo, texto in frases_comparacao:
    vec = np.array(get_embedding(texto), dtype=np.float32)
    resultados.append({
        "Categoria": tipo,
        "Texto": texto,
        "Dist. Euclidiana": round(distancia_euclidiana(vec_ancora, vec), 4),
        "Similaridade Cosseno": round(similaridade_cosseno(vec_ancora, vec), 4),
        "Distância Cosseno": round(distancia_cosseno(vec_ancora, vec), 4)
    })

df_resultados = pd.DataFrame(resultados)
print(df_resultados.to_string(index=False))