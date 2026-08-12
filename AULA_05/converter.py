import os
import warnings
from pathlib import Path

os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore")

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

# 1. Configura o Docling para NÃO usar OCR (evita downloads externos de modelos)
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

arquivos_pdf = [
    "attention_is_all_you_need.pdf",
    "bert_pretraining.pdf",
    "bioetica_e_ia.pdf",
    "escrita_academica_ia.pdf",
    "gpt3_language_models.pdf",
    "gpt4_technical_report.pdf",
    "instruct_gpt.pdf",
    "llama_foundation_models.pdf",
    "lora_low_rank_adaptation.pdf",
    "retrieval_augmented_generation.pdf",
    "scaling_laws_llms.pdf",
    "twitter_algoritmo.pdf"
]

print("Iniciando a conversão dos arquivos (modo rápido sem OCR)...\n")

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