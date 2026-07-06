import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import random
import time
import os
import subprocess  # Ajouté pour pouvoir lancer bot.py

app = Flask(__name__)
CORS(app) # Permet au site HTML de communiquer avec le serveur

VALID_CODES_FILE = "valid_apple_codes.txt"

# --- LOGIQUE DE DÉMARRAGE DU BOT EN TÂCHE DE FOND ---
def lancer_le_bot():
    """Cette fonction tourne en arrière-plan et lance bot.py"""
    print("[SERVEUR] Démarrage du robot d'automatisation (bot.py)...")
    try:
        # Lance le script bot.py comme un processus indépendant
        subprocess.Popen(["python", "bot.py"])
    except Exception as e:
        print(f"[ERREUR] Impossible de lancer bot.py : {e}")

# ----------------------------------------------------

# Route appelée par le formulaire HTML
@app.route('/api/boost', methods=['POST'])
def receive_boost():
    data = request.json
    username = data.get('username')
    platform = data.get('platform')
    service = data.get('service')
    quantity = data.get('quantity')
    
    # Génération d'un "code" de commande unique
    order_id = f"SB-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # Écrire l'action requise dans le fichier texte pour que le bot la lise
    with open(VALID_CODES_FILE, 'a') as f:
        f.write(f"ORDER_{order_id}_{username}_{platform}_{quantity}\n")
        
    return jsonify({
        "status": "success",
        "order_id": order_id,
        "message": "Commande reçue et transmise au robot"
    })

if __name__ == "__main__":
    # 1. On lance d'abord le robot en tâche de fond (thread) pour qu'il surveille le fichier texte
    threading.Thread(target=lancer_le_bot, daemon=True).start()

    # 2. On lance le serveur Flask pour recevoir les requêtes du site web
    port_render = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port_render, debug=True)
