from pdf_reader import PDFFileReader

class ResultsClassifier:
    def __init__(self, pdf_files, search_words):
        self.pdf_files = pdf_files
        self.search_words = search_words

    def classify_results(self):
        files_with_keywords = {pdf_path: [] for pdf_path in self.pdf_files}
        
        for pdf_path in self.pdf_files:
            pdf_reader = PDFFileReader(pdf_path)
            extracted_text = pdf_reader.extract_text()

            keywords_found = [keyword for keyword in self.search_words if keyword.lower() in extracted_text.lower()]
            files_with_keywords[pdf_path] = keywords_found

        # Classificar o dicionário com base na quantidade de palavras-chave satisfeitas
        sorted_results_list = sorted(files_with_keywords.items(), key=lambda item: len(item[1]), reverse=True)
        
        sorted_results = dict(sorted_results_list)
        
        return sorted_results
