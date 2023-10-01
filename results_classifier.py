from pdf_reader import PDFFileReader

class ResultsClassifier:
    def __init__(self, pdf_files, filter_strings):
        self.pdf_files = pdf_files
        self.filter_strings = filter_strings

    def classify_results(self):
        files_with_filters = {pdf_path: [] for pdf_path in self.pdf_files}
        
        for pdf_path in self.pdf_files:
            pdf_reader = PDFFileReader(pdf_path)
            extracted_text = pdf_reader.extract_text()

            for filter_string in self.filter_strings:
                if filter_string.strip().lower() in extracted_text.lower():
                    files_with_filters[pdf_path].append(filter_string.strip())

        # Classificar o dicionário com base na presença das strings de filtro
        sorted_results = {k: v for k, v in sorted(files_with_filters.items(), key=lambda item: len(item[1]), reverse=True)}
        
        return sorted_results
