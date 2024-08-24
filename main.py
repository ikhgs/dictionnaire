from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/definition', methods=['GET'])
def get_definition():
    # Obtenir le mot à partir des paramètres de requête
    mot = request.args.get('mot', '')
    
    # Construire l'URL de l'API
    url = f'https://www.le-dictionnaire.com/definition.php?mot={mot}'
    
    # Envoyer une requête GET à l'URL
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve data'}), 500
    
    # Parser le HTML de la réponse
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraire les données spécifiques (exemple basé sur les données HTML)
    definition = soup.find('div', class_='definition').get_text(strip=True)
    examples = soup.find('div', class_='examples').get_text(strip=True) if soup.find('div', class_='examples') else ''
    synonyms = soup.find('div', class_='synonyms').get_text(strip=True) if soup.find('div', class_='synonyms') else ''
    
    # Construire le résultat JSON
    result = {
        'definition': definition,
        'examples': examples,
        'synonyms': synonyms
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
