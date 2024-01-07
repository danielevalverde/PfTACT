from results_classifier import ResultsClassifier
from output_formatter import OutputFormatter

def main():
    pdf_files_input = input("Insira os nomes dos arquivos PDF separados por espaços: ")
    pdf_files = pdf_files_input.split()

    strings_input = input("Insira as strings de busca separadas por vírgulas: ")
    filter_strings = [filter_string.strip() for filter_string in strings_input.split(',')]
    
    qtd_strings = len(filter_strings)

    operator = input("Escolha o operador da busca: e/ou or not: ")
    if operator == "not":
        not_strings_input = input("Insira as strings de busca separadas por vírgulas: ")
        not_strings = [not_string.strip() for not_string in not_strings_input.split(',')]
    else:
        not_strings = None

    results_classifier = ResultsClassifier(pdf_files, filter_strings, operator, not_strings)
    results, keywords_count = results_classifier.classify_results()

    output_format = input("Escolha o formato de saída:\n"
                      "1. Terminal\n"
                      "2. Arquivo de Texto\n"
                      "3. Arquivo CSV\n"
                      "4. Arquivo PDF\n"
                      "Digite o número correspondente ao formato desejado: ")

    output_formatter = OutputFormatter()
    output_formatter.format_results(results, keywords_count, output_format, operator, qtd_strings)

if __name__ == "__main__":
    main()
