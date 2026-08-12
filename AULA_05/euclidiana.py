import math

def distancia_euclidiana(embedding_a, embedding_b):
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Os dois embeddings devem ter a mesma dimensão.")
    
    soma_quadrados = sum((a - b) ** 2 for a, b in zip(embedding_a, embedding_b))
    return math.sqrt(soma_quadrados)

# Exemplo de uso:
embedding_a = [1.5, 2.0, 3.5]
embedding_b = [4.0, 5.0, 6.0]

distancia = distancia_euclidiana(embedding_a, embedding_b)
print(f"Distância Euclidiana: {distancia}")