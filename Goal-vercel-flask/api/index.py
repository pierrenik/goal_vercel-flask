from openpyxl import Workbook
from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_file", methods=["POST"])
def process_file():
    file = request.files.get("file")
    if file is None:
        return "No file selected"

    data = []
    file_content = file.read().decode("utf-8") 
    lines = file_content.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    
    # Concaténer chaque 3 lignes en les séparant par une virgule
    for i in range(0, len(non_empty_lines), 3):
        line1 = non_empty_lines[i].strip()
        line2 = non_empty_lines[i+1].strip() if i+1 < len(non_empty_lines) else "" 
        line3 = non_empty_lines[i+2].strip() if i+2 < len(non_empty_lines) else ""
        data.append([line1, line2, line3])

    # Obtenir le chemin du dossier "Téléchargements" par défaut
    downloads_folder = os.path.expanduser("~") + "/Downloads/"

    # Créer un nouveau fichier xlsx
    wb = Workbook()
    ws = wb.active

    # Écrire les données dans le fichier xlsx
    ws.append(["Questions", "Réponse vraies", "Réponses fausses"]) # en-têtes de colonnes
    for row in data:
        ws.append(row)

    # Enregistrer le fichier xlsx dans le dossier "Téléchargements"
    wb.save(downloads_folder + "data.xlsx")

    return "Fichier transformé avec succès."

if __name__ == "__main__":
    app.run(debug=True)
