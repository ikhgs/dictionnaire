from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/translate', methods=['GET'])
def translate():
    # Récupérer le texte à traduire depuis les paramètres de requête
    text_to_translate = request.args.get('q', default='', type=str)
    source_lang = request.args.get('sl', default='auto', type=str)  # Langue source (par défaut 'auto' pour autodétection)
    target_lang = request.args.get('tl', default='en', type=str)    # Langue cible (par défaut anglais)

    # Si aucun texte n'est fourni, retourner une erreur
    if not text_to_translate:
        return jsonify({"error": "Veuillez fournir un texte à traduire via le paramètre 'q'."}), 400

    # Paramètres pour la requête de traduction
    params = {
        'client': 'webapp',
        'sl': source_lang,  # Langue source (par défaut autodétection)
        'tl': target_lang,  # Langue cible (par défaut anglais)
        'hl': target_lang,  # Langue de l'interface (correspond à la langue cible)
        'dt': 't',          # Type de données (traduction)
        'q': text_to_translate  # Texte à traduire
    }

    # Requête à l'API de Google Translate
    try:
        res = requests.get('https://translate.google.com/translate_a/single', params=params).json()
        translated_text = res[0][0][0]
    except Exception as e:
        return jsonify({"error": "Erreur lors de la traduction.", "details": str(e)}), 500

    # Retourner la traduction en JSON
    return jsonify({"translated_text": translated_text, "source_lang": source_lang, "target_lang": target_lang})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
