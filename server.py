import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import random
import time

app = Flask(__name__)
CORS(app) # Permet au site HTML de communiquer avec le serveur

VALID_CODES_FILE = "valid_apple_codes.txt"

# Route appelée par le formulaire HTML
@app.route('/api/boost', methods=['POST'])
def receive_boost():
    data = request.json
    username = data.get('username')
    platform = data.get('platform')
    service = data.get('service')
    quantity = data.get('quantity')
    
    # Ici, au lieu d'un simple code Apple, on simule une génération
    # de "code" de commande unique pour le bot TikTok
    order_id = f"SB-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # Écrire l'action requise dans votre fichier texte pour que le bot la lise
    with open(VALID_CODES_FILE, 'a') as f:
        f.write(f"ORDER_{order_id}_{username}_{platform}_{quantity}\n")
        
    return jsonify({
        "status": "success",
        "order_id": order_id,
        "message": "Commande reçue et transmise au robot TikTok"
    })

# Insérer ici votre logique de boucle 'monitor_and_post()' originale
# en tâche de fond...

if __name__ == "__main__":
    # Lancer le serveur Flask sur le port 5000
    app.run(port=5000, debug=True)
