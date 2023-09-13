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

# Solicitar que o usuário escolha o formato de saída
print("Escolha o formato de saída:")
print("1. Terminal")
print("2. Arquivo de Texto")
print("3. Arquivo CSV")
print("4. Arquivo PDF")

choice = input("Digite o número correspondente ao formato desejado: ")

if choice == "1":  # Saída no terminal
    for keyword, files in files_with_keywords.items():
        if files:
            print(f"A palavra-chave '{keyword}' foi encontrada nos seguintes arquivos:")
            for file in files:
                print(file)
        else:
            print(f"A palavra-chave '{keyword}' não foi encontrada em nenhum arquivo.")
elif choice == "2":  # Saída em arquivo de texto
    output_file = "output.txt"
    with open(output_file, 'w') as out_file:
        for keyword, files in files_with_keywords.items():
            if files:
                out_file.write(f"A palavra-chave '{keyword}' foi encontrada nos seguintes arquivos:\n")
                for file in files:
                    out_file.write(file + "\n")
            else:
                out_file.write(f"A palavra-chave '{keyword}' não foi encontrada em nenhum arquivo.\n")
    print(f"Os resultados foram salvos em '{output_file}'.")
elif choice == "3":  # Saída em arquivo CSV
    csv_output_file = "output.csv"
    with open(csv_output_file, 'w', newline='') as csv_out_file:
        csv_writer = csv.writer(csv_out_file)
        csv_writer.writerow(["Palavra-chave", "Arquivos"])
        for keyword, files in files_with_keywords.items():
            csv_writer.writerow([keyword, ", ".join(files)])
    print(f"Os resultados foram salvos em '{csv_output_file}' (CSV).")
elif choice == "4":  # Saída em arquivo PDF
    pdf_output_file = "output.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Resultados da Busca em PDF:")
    y_position = 730
    for keyword, files in files_with_keywords.items():
        if files:
            c.drawString(100, y_position, f"Palavra-chave '{keyword}' encontrada nos seguintes arquivos:")
            y_position -= 15
            for file in files:
                c.drawString(120, y_position, file)
                y_position -= 15
        else:
            c.drawString(100, y_position, f"A palavra-chave '{keyword}' não foi encontrada em nenhum arquivo.")
            y_position -= 15
    c.save()
    with open(pdf_output_file, 'wb') as pdf_out_file:
        pdf_out_file.write(buffer.getvalue())
    print(f"Os resultados foram salvos em '{pdf_output_file}' (PDF).")
else:
    print("Escolha de formato inválida.")
