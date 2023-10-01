import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class OutputFormatter:
    @staticmethod
    def format_results(results, output_format):
        if output_format == "1":
            for file, keywords_found in results.items():
                if keywords_found:
                    print(f"Arquivo: {file}")
                    print(f"Palavras-chave encontradas: {', '.join(keywords_found)}")
                    print()
        elif output_format == "2":
            output_file = "output.txt"
            with open(output_file, 'w') as out_file:
                for file, keywords_found in results.items():
                    out_file.write(f"Arquivo: {file}\n")
                    out_file.write(f"Palavras-chave encontradas: {', '.join(keywords_found)}\n\n")
            print(f"Os resultados foram salvos em '{output_file}'.")
        elif output_format == "3":
            csv_output_file = "output.csv"
            with open(csv_output_file, 'w', newline='') as csv_out_file:
                csv_writer = csv.writer(csv_out_file)
                csv_writer.writerow(["Arquivo", "Palavras-chave Encontradas"])
                for file, keywords_found in results.items():
                    csv_writer.writerow([file, ', '.join(keywords_found)])
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
                c.drawString(100, y_position, f"Palavras-chave encontradas: {', '.join(keywords_found)}")
                y_position -= 15
                y_position -= 15  # Espaço adicional entre os resultados
            c.save()
            with open(pdf_output_file, 'wb') as pdf_out_file:
                pdf_out_file.write(buffer.getvalue())
            print(f"Os resultados foram salvos em '{pdf_output_file}' (PDF).")
        else:
            print("Escolha de formato inválida.")
