import PyPDF2

class PDFFileReader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        with open(self.pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text()
            return extracted_text
