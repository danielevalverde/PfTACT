import pdfplumber
import unidecode

class ResultsClassifier:
    def __init__(self, pdf_files, filter_strings):
        self.pdf_files = pdf_files
        self.filter_strings = [unidecode.unidecode(filter_string.strip().lower()) for filter_string in filter_strings]

    def classify_results(self):
        files_with_filters = {pdf_path: [] for pdf_path in self.pdf_files}
        keywords_count = {pdf_path: 0 for pdf_path in self.pdf_files}

        for pdf_path in self.pdf_files:
            with pdfplumber.open(pdf_path) as pdf:
                extracted_text = ""
                for page in pdf.pages:
                    extracted_text += page.extract_text()
                
                extracted_text = unidecode.unidecode(extracted_text.lower())

                for filter_string in self.filter_strings:
                    if filter_string in extracted_text:
                        files_with_filters[pdf_path].append(filter_string.strip())
                        keywords_count[pdf_path] += 1

        sorted_results = {k: v for k, v in sorted(files_with_filters.items(), key=lambda item: len(item[1]), reverse=True)}
        
        return sorted_results, keywords_count
