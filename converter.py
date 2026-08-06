import os
from docling.document_converter import DocumentConverter

arquivos_pdf = [
    "bioetica_e_ia.pdf",
    "escrita_academica_ia.pdf",
    "twitter_algoritmo.pdf"
]

converter = DocumentConverter()

print("Iniciando a conversão dos arquivos...")

for pdf in arquivos_pdf:

    if os.path.exists(pdf):
        print(f"Convertendo: {pdf}...")
        
        result = converter.convert(pdf)
        
        markdown_content = result.document.export_to_markdown()
        
        md_filename = pdf.replace(".pdf", ".md")
        
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
            
        print(f"✓ Sucesso! Criado: {md_filename}")
    else:
        print(f"✗ Erro: O arquivo '{pdf}' não foi encontrado na pasta.")

print("\nProcesso finalizado!")
