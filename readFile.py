import PyPDF2

# Caminho para o arquivo PDF
pdf_path = 'exemplo.pdf'
search_string = "Pesquisa"

with open(pdf_path, 'rb') as pdf_file:
  pdf_reader = PyPDF2.PdfReader(pdf_file)
  
  extracted_text = ''
  
  # Iterar pelas páginas do PDF
  for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    extracted_text += page.extract_text()
        
# Imprimir o texto extraído
# print(extracted_text)

if search_string.lower() in extracted_text.lower():
  print(f"O texto do arquivo '{pdf_path}' contém a string '{search_string}':")
  # print(extracted_text)
else:
  print(f"A string '{search_string}' não foi encontrada no texto do arquivo '{pdf_path}'.")
