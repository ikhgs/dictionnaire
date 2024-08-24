import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/definition', methods=['GET'])
def get_definition():
    # Récupérer le mot à chercher depuis les paramètres de requête
    mot = request.args.get('mot', '')
    
    # URL à interroger (dépend du mot recherché)
    url = f'https://www.le-dictionnaire.com/definition/{mot}'
    
    # Envoyer une requête GET pour obtenir le HTML de la page
    response = requests.get(url)
    
    # Vérifier si la requête a réussi
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve data'}), 500
    
    # Analyser le contenu de la page avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraire les sections de définition à partir de la page
    # Exemple de recherche par classe ou balises spécifiques
    definition_section = soup.find('div', {'class': 'definition'})  # Ajuster en fonction du site
    definition_text = definition_section.get_text(strip=True) if definition_section else 'Définition non trouvée'

    # Vous pouvez ajouter d'autres informations comme des exemples ou synonymes
    result = {
        'mot': mot,
        'definition': definition_text
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
