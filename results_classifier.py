import pdfplumber
from datetime import datetime

class ResultsClassifier:
    def __init__(self, pdf_files, filter_strings):
        self.pdf_files = pdf_files
        self.filter_strings = [filter_string.strip().lower() for filter_string in filter_strings]

    def extract_metadata(self, pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            metadata = pdf.metadata
        return metadata

    def format_date(self, date_str):
        date_str = date_str.replace("D:", "").replace("'", "").replace("\"", "")
        date_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S%z')
        # Formatar a data em um formato legível
        return date_obj.strftime('%Y-%m-%d %H:%M:%S %Z')

    def classify_results(self):
        files_with_filters = {pdf_path: [] for pdf_path in self.pdf_files}
        keywords_count = {pdf_path: 0 for pdf_path in self.pdf_files}

        for pdf_path in self.pdf_files:
            metadata = self.extract_metadata(pdf_path)
            print("Metadata for", pdf_path)
            for key, value in metadata.items():
                if key == "ModDate":
                    value = self.format_date(value)
                print(f"{key}: {value}")
            print()
            
            with pdfplumber.open(pdf_path) as pdf:
                extracted_text = ""
                for page in pdf.pages:
                    extracted_text += page.extract_text()
                
                extracted_text = extracted_text.lower()

                for i, filter_string in enumerate(self.filter_strings):
                    if filter_string in extracted_text:
                        files_with_filters[pdf_path].append(filter_string.strip())
                        keywords_count[pdf_path] += 1

        sorted_results = {k: v for k, v in sorted(files_with_filters.items(), key=lambda item: len(item[1]), reverse=True)}
        
        return sorted_results, keywords_count
