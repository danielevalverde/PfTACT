import pdfplumber
from datetime import datetime

class ResultsClassifier:
    def __init__(self, pdf_files, filter_strings, operator_not=None, not_strings=None):
        self.pdf_files = pdf_files
        self.filter_strings = [filter_string.strip().lower() for filter_string in filter_strings]
        self.operator_not = operator_not
        self.not_strings = [not_string.strip().lower() for not_string in not_strings] if not_strings else []

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
            # metadata = self.extract_metadata(pdf_path)
            # print("Metadata for", pdf_path)
            # for key, value in metadata.items():
            #     if key == "ModDate":
            #         value = self.format_date(value)
            #     print(f"{key}: {value}")
            # print()
            
            # Extract text from the PDF
            with pdfplumber.open(pdf_path) as pdf:
                extracted_text = ""
                for page in pdf.pages:
                    extracted_text += page.extract_text().lower()
                
                # tem que contar a qtd de estrings filtradas e do not no for
                
                found_not_string = False
                if self.operator_not == "yes":
                    for not_string in self.not_strings:
                        if not_string in extracted_text:
                            found_not_string = True
                            break  # Se encontrou uma not_string, para a busca

                    if found_not_string:
                        files_with_filters[pdf_path] = ["possui string not"]
                        continue

                # search the string in the PDF
                # Check for 'filter_strings' only if 'not' is not found
                for filter_string in self.filter_strings:
                    if filter_string in extracted_text and found_not_string == False:
                        files_with_filters[pdf_path].append(filter_string.strip())
                        keywords_count[pdf_path] += 1

        sorted_results = {k: v for k, v in sorted(files_with_filters.items(), key=lambda item: len(item[1]), reverse=True)}
        
        return sorted_results, keywords_count
