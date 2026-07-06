import time
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

VALID_CODES_FILE = "valid_apple_codes.txt"
PUBLISHED_CODES_FILE = "published_codes.txt"
PROXIES_FILE = "proxies.txt"  # Fichier contenant vos 1000 proxies

def load_proxies():
    """Lit automatiquement le fichier proxies.txt et charge la liste en mémoire"""
    try:
        with open(PROXIES_FILE, 'r') as f:
            # Récupère chaque ligne, retire les espaces et ignore les lignes vides
            proxies = [line.strip() for line in f if line.strip()]
        print(f"[Système] {len(proxies)} proxies chargés avec succès depuis {PROXIES_FILE}.")
        return proxies
    except FileNotFoundError:
        print(f"[Attention] Le fichier {PROXIES_FILE} n'a pas été trouvé. Fonctionnement sans proxy.")
        return []

def load_published():
    try:
        with open(PUBLISHED_CODES_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def simuler_comportement_humain(driver):
    try:
        actions = ActionChains(driver)
        scroll_distance = random.randint(100, 300)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(1.5, 3.0))
        driver.execute_script(f"window.scrollBy(0, -{scroll_distance});")
        time.sleep(random.uniform(1.0, 2.5))
        
        body = driver.find_element(By.TAG_NAME, 'body')
        actions.move_to_element_with_offset(body, random.randint(10, 500), random.randint(10, 500)).perform()
    except Exception as e:
        pass

def visionner_video_avec_proxy(video_url, proxy_choisi):
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    if proxy_choisi:
        print(f"[Proxy] Routage via : {proxy_choisi}")
        options.add_argument(f'--proxy-server={proxy_choisi}')
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.set_page_load_timeout(25) 
        print(f"[Bot] Ouverture de la vidéo : {video_url}")
        driver.get(video_url)
        
        time.sleep(random.randint(5, 8))
        simuler_comportement_humain(driver)
        
        temps_regard = random.randint(18, 28)
        print(f"[Bot] Visionnage en cours ({temps_regard}s)...")
        
        time.sleep(temps_regard / 2)
        simuler_comportement_humain(driver)
        time.sleep(temps_regard / 2)
        
        print("[Bot] Vue validée.")
        
    except Exception as e:
        print(f"[Erreur Navigateur] Session interrompue : {e}")
    finally:
        driver.quit()

def monitor_and_view():
    published = load_published()
    # Chargement de vos proxies au démarrage du script
    proxies_pool = load_proxies()
    
    print("[Système] Le robot de vues est démarré. En attente de commandes...")
    
    while True:
        try:
            with open(VALID_CODES_FILE, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            new_orders = set(lines) - published
            
            for order in new_orders:
                parts = order.split('_')
                if len(parts) >= 3:
                    video_url = parts[2]
                    
                    # Sélectionne une IP au hasard parmi vos 1000 proxies
                    proxy = random.choice(proxies_pool) if proxies_pool else None

                    threading.Thread(target=visionner_video_avec_proxy, args=(video_url, proxy)).start()
                    
                    published.add(order)
                    with open(PUBLISHED_CODES_FILE, 'a') as f:
                        f.write(f"{order}\n")
                        
                time.sleep(4)
                
            time.sleep(10)
        except Exception as e:
            print(f"[Erreur Système] : {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_and_view()
