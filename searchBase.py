import PyPDF2
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Solicitar que o usuário insira os nomes dos arquivos PDF separados por espaços
pdf_files_input = input("Insira os nomes dos arquivos PDF separados por espaços: ")

# Dividir os nomes dos arquivos em uma lista
pdf_files = pdf_files_input.split()

# Solicitar que o usuário insira as palavras-chave separadas por espaços
search_input = input("Insira as palavras-chave separadas por espaços: ")

# Dividir as palavras-chave em uma lista
search_words = search_input.split()

# Inicializar um dicionário para armazenar os arquivos que contêm cada palavra-chave
files_with_keywords = {keyword: [] for keyword in search_words}

# Nome do arquivo de saída TXT
output_file = "output.txt"
# Nome do arquivo de saída em PDF
pdf_output_file = "output.pdf"

# Nome do arquivo de saída em CSV
csv_output_file = "output.csv"

# Iterar pelos arquivos PDF
for pdf_path in pdf_files:
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        extracted_text = ''
        
        # Iterar pelas páginas do PDF
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text()

        # Verificar se alguma das palavras-chave está presente no texto extraído
        for keyword in search_words:
            if keyword.lower() in extracted_text.lower():
                files_with_keywords[keyword].append(pdf_path)

## Abrir o arquivo de saída em modo de escrita
with open(output_file, 'w') as out_file:
    # Redirecionar a saída padrão para o arquivo de saída
    import sys
    sys.stdout = out_file
    
    # Verificar quais arquivos contêm as palavras-chave
    for keyword, files in files_with_keywords.items():
        if files:
            print(f"A palavra-chave '{keyword}' foi encontrada nos seguintes arquivos:")
            for file in files:
                print(file)
        else:
            print(f"A palavra-chave '{keyword}' não foi encontrada em nenhum arquivo.")

# Restaurar a saída padrão
sys.stdout = sys.__stdout__