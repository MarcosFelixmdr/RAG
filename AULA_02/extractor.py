import json
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

env_file = find_dotenv(usecwd=True)
if env_file:
    load_dotenv(env_file)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A variável OPENAI_API_KEY não foi encontrada no arquivo .env!")

class DocumentMetadata(BaseModel):
    titulo: str = Field(description="Título completo e principal do artigo ou trabalho")
    autores: list[str] = Field(description="Lista com os nomes de todos os autores identificados")
    ano: int = Field(description="Ano de publicação do trabalho (ex: 2024)")

client = OpenAI(api_key=api_key)

def extrair_metadados(caminho_md: Path) -> DocumentMetadata:
    with open(caminho_md, "r", encoding="utf-8") as f:
        conteudo = f.read()

    trecho_inicial = conteudo[:4000]

    modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    completion = client.beta.chat.completions.parse(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente especializado em extrair metadados de documentos acadêmicos."
            },
            {
                "role": "user",
                "content": f"Extraia os metadados (título, autores e ano de publicação) do seguinte conteúdo:\n\n{trecho_inicial}"
            }
        ],
        response_format=DocumentMetadata,
    )

    return completion.choices[0].message.parsed

arquivos_md = [
    "bioetica_e_ia.md",
    "escrita_academica_ia.md",
    "twitter_algoritmo.md"
]

print("Iniciando a extração de metadados...\n")

for md_file_str in arquivos_md:
    md_path = Path(md_file_str)

    if md_path.exists():
        print(f"Processando: {md_path.name}...")
        
        metadados = extrair_metadados(md_path)
        json_data = metadados.model_dump()
        
        json_filename = Path(f"output_{md_path.stem}.json")
        
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            
        print(f"✓ JSON salvo com sucesso: {json_filename}\n")
    else:
        print(f"✗ Erro: O arquivo '{md_file_str}' não foi encontrado na pasta.\n")

print("Processo finalizado!")