from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_definition(word):
    # URL du site avec le mot recherché
    url = f"https://www.le-dictionnaire.com/definition.php?mot={word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraction des données
    try:
        definition = soup.find("div", class_="definition").text.strip()  # Adaptez la classe selon la structure HTML réelle
        genre = soup.find("div", class_="genre").text.strip()  # Adaptez la classe selon la structure HTML réelle
    except AttributeError:
        definition = "Définition non trouvée"
        genre = "Genre non spécifié"

    # Structuration en JSON
    data = {
        "mot": word,
        "definition": definition,
        "genre": genre
    }
    
    return data

@app.route('/api', methods=['GET'])
def api():
    word = request.args.get('mot')
    if not word:
        return jsonify({"error": "Le paramètre 'mot' est requis"}), 400
    
    data = get_definition(word)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
