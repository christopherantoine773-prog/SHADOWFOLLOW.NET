import time
import random
import threading
import requests

VALID_CODES_FILE = "valid_apple_codes.txt"
PUBLISHED_CODES_FILE = "published_codes.txt"
PROXIES_FILE = "proxies.txt"

def load_proxies():
    """Charge les proxies bruts de votre fichier et les formate pour la bibliothèque requests"""
    try:
        with open(PROXIES_FILE, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        print(f"[Système] {len(proxies)} proxies chargés pour le réseau.")
        return proxies
    except FileNotFoundError:
        print(f"[Attention] Fichier {PROXIES_FILE} introuvable.")
        return []

def load_published():
    try:
        with open(PUBLISHED_CODES_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def envoyer_requete_vue(video_url, proxy_brut):
    """Envoie une requête de vue directe via le proxy sans ouvrir de navigateur"""
    # Formatage du proxy pour Python (ex: 103.152.127.10:8080)
    proxies_config = {
        "http": f"http://{proxy_brut}",
        "https": f"http://{proxy_brut}"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        print(f"[Bot] Envoi d'une vue via le proxy {proxy_brut} vers {video_url}")
        # On fait une requête réseau ultra-rapide sur la vidéo
        response = requests.get(video_url, proxies=proxies_config, headers=headers, timeout=7)
        if response.status_code == 200:
            print("[Bot] Vue transmise avec succès au serveur cible.")
        else:
            print(f"[Bot Status] Réponse serveur : {response.status_code}")
    except Exception as e:
        print(f"[Proxy Échec] Ce proxy a expiré ou a été rejeté : {proxy_brut}")

def monitor_and_view():
    published = load_published()
    proxies_pool = load_proxies()
    
    print("[Système] Le robot de requêtes réseau est démarré. En attente...")
    
    while True:
        try:
            with open(VALID_CODES_FILE, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            new_orders = set(lines) - published
            
            for order in new_orders:
                parts = order.split('_')
                # Structure : ORDER_orderID_username_platform_quantity
                # Si l'utilisateur met l'URL de sa vidéo dans la case "username" du formulaire :
                if len(parts) >= 3:
                    video_url = parts[2]  # Récupère l'URL transmise
                    
                    # Sélectionne un proxy au hasard
                    proxy = random.choice(proxies_pool) if proxies_pool else None

                    # Lance la requête en tâche de fond pour ne pas bloquer le serveur
                    threading.Thread(target=envoyer_requete_vue, args=(video_url, proxy)).start()
                    
                    published.add(order)
                    with open(PUBLISHED_CODES_FILE, 'a') as f:
                        f.write(f"{order}\n")
                        
                time.sleep(1)
                
            time.sleep(5)
        except Exception as e:
            print(f"[Erreur Système Bot] : {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_and_view()
