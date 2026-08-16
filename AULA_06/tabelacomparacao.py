import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

print("Carregando modelo local de embeddings...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embedding(text: str) -> np.ndarray:
    return model.encode(text, convert_to_numpy=True)

# Funções de distância/similaridade
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
vec_ancora = get_embedding(frase_ancora)

resultados = []
print("Comparando com as outras frases...\n")
for tipo, texto in frases_comparacao:
    vec = get_embedding(texto)
    resultados.append({
        "Categoria": tipo,
        "Texto": texto,
        "Dist. Euclidiana": round(distancia_euclidiana(vec_ancora, vec), 4),
        "Similaridade Cosseno": round(similaridade_cosseno(vec_ancora, vec), 4),
        "Distância Cosseno": round(distancia_cosseno(vec_ancora, vec), 4)
    })

df_resultados = pd.DataFrame(resultados)
print(df_resultados.to_string(index=False))