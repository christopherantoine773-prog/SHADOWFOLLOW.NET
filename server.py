import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import random
import time
import os
import requests

app = Flask(__name__)
CORS(app)

VALID_CODES_FILE = "valid_apple_codes.txt"

def recuperer_vues_initiales(video_url, platform):
    """
    Simule la récupération du compteur actuel de la vidéo avant le boost.
    Dans une version de production, cela nécessiterait une API officielle 
    ou un outil de scraping comme Lyve/RapidAPI pour lire le vrai compteur.
    """
    # On simule un nombre de vues de départ aléatoire pour le test
    return random.randint(150, 2500)

@app.route('/api/boost', methods=['POST'])
def receive_boost():
    data = request.json
    username = data.get('username') # Contient généralement l'URL ou l'identifiant
    platform = data.get('platform')
    service = data.get('service')
    quantity = data.get('quantity')
    
    # 1. Récupération du nombre de vues qu'il y avait avant le début du boost
    vues_depart = recuperer_vues_initiales(username, platform)
    
    # 2. Génération de l'identifiant de commande unique
    order_id = f"SB-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # 3. Écriture dans le fichier de transmission pour le bot
    with open(VALID_CODES_FILE, 'a') as f:
        f.write(f"ORDER_{order_id}_{username}_{platform}_{quantity}_{vues_depart}\n")
        
    # 4. On renvoie les informations au site web (app.js) pour affichage
    return jsonify({
        "status": "success",
        "order_id": order_id,
        "start_count": vues_depart, # Transmet le nombre de vues initial
        "message": f"Commande reçue. Compteur de départ : {vues_depart} vues. Transmission au robot..."
    })

if __name__ == "__main__":
    port_render = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port_render, debug=True)
