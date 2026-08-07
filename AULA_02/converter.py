import os
import warnings

os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

from pathlib import Path
from docling.document_converter import DocumentConverter

arquivos_pdf = [
    "bioetica_e_ia.pdf",
    "escrita_academica_ia.pdf",
    "twitter_algoritmo.pdf"
]

converter = DocumentConverter()

print("Iniciando a conversão dos arquivos...\n")

for pdf_str in arquivos_pdf:
    pdf_path = Path(pdf_str)

    if pdf_path.exists():
        print(f"Convertendo: {pdf_path.name}...")
        
        result = converter.convert(pdf_path)
        markdown_content = result.document.export_to_markdown()
        
        md_filename = pdf_path.with_suffix(".md")
        
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
            
        print(f"✓ Sucesso! Criado: {md_filename}\n")
    else:
        print(f"✗ Erro: O arquivo '{pdf_str}' não foi encontrado na pasta.\n")

print("Processo finalizado!")