import PyPDF2
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

pdf_files_input = input("Insira os nomes dos arquivos PDF separados por espaços: ")

pdf_files = pdf_files_input.split()

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

        # Verificar quantas palavras-chave estão presentes no texto extraído
        keywords_found = [keyword for keyword in search_words if keyword.lower() in extracted_text.lower()]

        # Armazenar as palavras-chave encontradas para cada arquivo
        files_with_keywords[pdf_path] = keywords_found

# Classificar os arquivos com base na quantidade de palavras-chave satisfeitas
sorted_files = sorted(pdf_files, key=lambda file: len(files_with_keywords[file]), reverse=True)

# Solicitar que o usuário escolha o formato de saída
print("Escolha o formato de saída:")
print("1. Terminal")
print("2. Arquivo de Texto")
print("3. Arquivo CSV")
print("4. Arquivo PDF")

choice = input("Digite o número correspondente ao formato desejado: ")

if choice == "1":  # Saída no terminal
    for file in sorted_files:
        keywords_found = files_with_keywords[file]
        if keywords_found:
            print(f"Arquivo: {file}")
            print(f"Palavras-chave encontradas: {', '.join(keywords_found)}")
            print()
elif choice == "2":  # Saída em arquivo de texto
    output_file = "output.txt"
    with open(output_file, 'w') as out_file:
        for file in sorted_files:
            keywords_found = files_with_keywords[file]
            out_file.write(f"Arquivo: {file}\n")
            out_file.write(f"Palavras-chave encontradas: {', '.join(keywords_found)}\n\n")
    print(f"Os resultados foram salvos em '{output_file}'.")
elif choice == "3":  # Saída em arquivo CSV
    csv_output_file = "output.csv"
    with open(csv_output_file, 'w', newline='') as csv_out_file:
        csv_writer = csv.writer(csv_out_file)
        csv_writer.writerow(["Arquivo", "Palavras-chave Encontradas"])
        for file in sorted_files:
            keywords_found = files_with_keywords[file]
            csv_writer.writerow([file, ', '.join(keywords_found)])
    print(f"Os resultados foram salvos em '{csv_output_file}' (CSV).")
elif choice == "4":  # Saída em arquivo PDF
    pdf_output_file = "output.pdf"
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Resultados da Busca em PDF (Rankeados):")
    y_position = 730
    for file in sorted_files:
        keywords_found = files_with_keywords[file]
        c.drawString(100, y_position, f"Arquivo: {file}")
        y_position -= 15
        c.drawString(100, y_position, f"Palavras-chave encontradas: {', '.join(keywords_found)}")
        y_position -= 15
        y_position -= 15  # Espaço adicional entre os resultados
    c.save()
    with open(pdf_output_file, 'wb') as pdf_out_file:
        pdf_out_file.write(buffer.getvalue())
    print(f"Os resultados foram salvos em '{pdf_output_file}' (PDF).")
else:
    print("Escolha de formato inválida.")
