from pdf_reader import PDFFileReader
from results_classifier import ResultsClassifier
from output_formatter import OutputFormatter

def main():
    pdf_files_input = input("Insira os nomes dos arquivos PDF separados por espaços: ")
    pdf_files = pdf_files_input.split()

    strings_input = input("Insira as strings de busca separadas por vírgulas: ")
    filter_strings = strings_input.split(',')

    results_classifier = ResultsClassifier(pdf_files, filter_strings)
    results = results_classifier.classify_results()

    print(results)

    output_format = input("Escolha o formato de saída:\n"
                      "1. Terminal\n"
                      "2. Arquivo de Texto\n"
                      "3. Arquivo CSV\n"
                      "4. Arquivo PDF\n"
                      "Digite o número correspondente ao formato desejado: ")

    output_formatter = OutputFormatter()
    output_formatter.format_results(results, output_format)

if __name__ == "__main__":
    main()
