import math

def distancia_cosseno(embedding_a, embedding_b):
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Os dois embeddings devem ter a mesma dimensão.")
    
    produto_escalar = sum(a * b for a, b in zip(embedding_a, embedding_b))
    
    norma_a = math.sqrt(sum(a ** 2 for a in embedding_a))
    norma_b = math.sqrt(sum(b ** 2 for b in embedding_b))
    
    if norma_a == 0 or norma_b == 0:
        raise ValueError("Não é possível calcular a distância com um vetor nulo.")
    
    similaridade = produto_escalar / (norma_a * norma_b)
    return 1 - similaridade

embedding_a = [1.5, 2.0, 3.5]
embedding_b = [4.0, 5.0, 6.0]

distancia = distancia_cosseno(embedding_a, embedding_b)
print(distancia)