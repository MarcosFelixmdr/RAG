import math

def distancia_euclidiana(embedding_a, embedding_b):
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Os dois embeddings devem ter a mesma dimensão.")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(embedding_a, embedding_b)))

def distancia_cosseno(embedding_a, embedding_b):
    if len(embedding_a) != len(embedding_b):
        raise ValueError("Os dois embeddings devem ter a mesma dimensão.")
    produto_escalar = sum(a * b for a, b in zip(embedding_a, embedding_b))
    norma_a = math.sqrt(sum(a ** 2 for a in embedding_a))
    norma_b = math.sqrt(sum(b ** 2 for b in embedding_b))
    
    if norma_a == 0 or norma_b == 0:
        raise ValueError("Não é possível calcular a distância com vetor nulo.")
        
    similaridade = produto_escalar / (norma_a * norma_b)
    return 1 - similaridade


embeddings = {
    # Animais
    "gato":     [0.90, 0.02, 0.05],
    "felino":   [0.95, 0.01, 0.02],
    "cachorro": [0.85, 0.03, 0.08],
    
    # Veículos
    "carro":    [0.02, 0.90, 0.05],
    "caminhão": [0.01, 0.95, 0.02],
    "moto":     [0.03, 0.85, 0.08],
    
    # Frutas
    "banana":   [0.05, 0.02, 0.90],
    "maçã":     [0.02, 0.01, 0.95],
    "goiaba":   [0.08, 0.03, 0.85]
}


def comparar_termos(termo_a, termo_b):
    vec_a = embeddings[termo_a]
    vec_b = embeddings[termo_b]
    
    d_euc = distancia_euclidiana(vec_a, vec_b)
    d_cos = distancia_cosseno(vec_a, vec_b)
    
    print(f"Comparando '{termo_a}' x '{termo_b}':")
    print(f"  - Distância Euclidiana: {d_euc:.4f}")
    print(f"  - Distância de Cosseno: {d_cos:.4f}\n")


print("=== 1. Mesma Categoria Semântica (Próximos) ===")
comparar_termos("gato", "felino")
comparar_termos("carro", "caminhão")
comparar_termos("banana", "maçã")

print("=== 2. Categorias Diferentes (Afastados) ===")
comparar_termos("gato", "carro")
comparar_termos("cachorro", "goiaba")
comparar_termos("moto", "banana")