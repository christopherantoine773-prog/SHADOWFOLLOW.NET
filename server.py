import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import random
import time
import os
import requests
import re  # Pour analyser les liens URL

app = Flask(__name__)
CORS(app)

VALID_CODES_FILE = "valid_apple_codes.txt"

def recuperer_vraies_ues_tiktok(video_url):
    """
    Tente de récupérer le vrai nombre de vues public de la vidéo.
    Note : Les réseaux bloquent souvent les serveurs cloud. Si le serveur est bloqué,
    on utilise une valeur par défaut intelligente pour éviter que le site plante.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        # Essai de lecture de la page publique de la vidéo
        reponse = requests.get(video_url, headers=headers, timeout=5)
        if reponse.status_code == 200:
            # Recherche du compteur de vues dans le code source de la page (balise Meta de TikTok)
            match = re.search(r'"playCount":(\d+)', reponse.text)
            if match:
                return int(match.group(1))
            
            match_alt = re.search(r'property="og:description" content="([^"]+)"', reponse.text)
            if match_alt:
                # Analyse le texte alternatif comme "X views" ou "X au vu"
                chiffres = re.findall(r'\d+', match_alt.group(1))
                if chiffres:
                    return int(chiffres[0])
    except Exception as e:
        print(f"[Scraper] Erreur lors de la lecture du compteur réel : {e}")
    
    # Si le serveur Render est bloqué par TikTok, on met 0 ou un chiffre fixe 
    # pour indiquer que la vidéo est bien ciblée mais le compteur protégé
    return 0

@app.route('/api/boost', methods=['POST'])
def receive_boost():
    data = request.json
    username = data.get('username') # Ici, c'est l'URL de la vidéo entrée par l'utilisateur
    platform = data.get('platform')
    service = data.get('service')
    quantity = data.get('quantity')
    
    print(f"[Serveur] Analyse de la vidéo : {username} sur {platform}")
    
    # 1. Tentative de récupération du VRAI compteur de départ
    if "tiktok.com" in username:
        vues_depart = recuperer_vraies_ues_tiktok(username)
    else:
        # Valeur par défaut si c'est une autre plateforme ou si l'URL est incomplète
        vues_depart = 0
    
    # 2. Génération de l'ID de commande unique
    order_id = f"SB-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # 3. Stockage dans le fichier texte pour transmission
    with open(VALID_CODES_FILE, 'a') as f:
        f.write(f"ORDER_{order_id}_{username}_{platform}_{quantity}_{vues_depart}\n")
        
    # 4. Envoi de la réponse exacte au fichier app.js
    return jsonify({
        "status": "success",
        "order_id": order_id,
        "start_count": vues_depart, # Renvoie le vrai compteur (ou 0 si masqué/bloqué)
        "message": "Liaison établie."
    })

if __name__ == "__main__":
    port_render = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port_render, debug=True)
