import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class OutputFormatter:
    @staticmethod
    def format_results(results, keywords_count, output_format):
        if output_format == "1":
            for file, keywords_found in results.items():
                if keywords_found:
                    print(f"Arquivo: {file}")
                    print(f"Palavras-chave encontradas ({keywords_count[file]}): {', '.join(keywords_found)}")
                    print()
                else:
                    print(f"Arquivo: {file}")
                    print("Nenhuma palavra-chave encontrada.")
                    print()
        elif output_format == "2":
            output_file = "output.txt"
            with open(output_file, 'w') as out_file:
                for file, keywords_found in results.items():
                    out_file.write(f"Arquivo: {file}\n")
                    if keywords_found:
                        out_file.write(f"Palavras-chave encontradas: {', '.join(keywords_found)}\n\n")
                    else:
                        out_file.write("Nenhuma palavra-chave encontrada.\n\n")
            print(f"Os resultados foram salvos em '{output_file}'.")
        elif output_format == "3":
            csv_output_file = "output.csv"
            with open(csv_output_file, 'w', newline='') as csv_out_file:
                csv_writer = csv.writer(csv_out_file)
                csv_writer.writerow(["Arquivo", "Palavras-chave Encontradas"])
                for file, keywords_found in results.items():
                    if keywords_found:
                        csv_writer.writerow([file, ', '.join(keywords_found)])
                    else:
                        csv_writer.writerow([file, "Nenhuma palavra-chave encontrada"])
            print(f"Os resultados foram salvos em '{csv_output_file}' (CSV).")
        elif output_format == "4":
            pdf_output_file = "output.pdf"
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.drawString(100, 750, "Resultados da Busca em PDF (Rankeados):")
            y_position = 730
            for file, keywords_found in results.items():
                c.drawString(100, y_position, f"Arquivo: {file}")
                y_position -= 15
                if keywords_found:
                    c.drawString(100, y_position, f"Palavras-chave encontradas: {', '.join(keywords_found)}")
                else:
                    c.drawString(100, y_position, "Nenhuma palavra-chave encontrada.")
                y_position -= 15
                y_position -= 15  # Espaço adicional entre os resultados
            c.save()
            with open(pdf_output_file, 'wb') as pdf_out_file:
                pdf_out_file.write(buffer.getvalue())
            print(f"Os resultados foram salvos em '{pdf_output_file}' (PDF).")
        else:
            print("Escolha de formato inválida.")
