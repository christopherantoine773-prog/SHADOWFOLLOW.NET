import requests
import time
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import json

VALID_CODES_FILE = "valid_apple_codes.txt"
PUBLISHED_CODES_FILE = "published_codes.txt"
ACCOUNTS_FILE = "accounts.json"

# Charger les comptes
def load_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

# Charger les codes déjà publiés
def load_published():
    try:
        with open(PUBLISHED_CODES_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

# Publier sur TikTok via Selenium (non détecté)
def post_to_tiktok(account, code):
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = uc.Chrome(options=options)
    
    try:
        driver.get("https://www.tiktok.com/login")
        time.sleep(5)
        
        # Injection des cookies pour rester connecté
        for cookie in account['cookies']:
            driver.add_cookie(cookie)
        
        driver.refresh()
        time.sleep(3)
        
        # Créer un post
        driver.get("https://www.tiktok.com/upload")
        time.sleep(5)
        
        caption = f"🎁 GIFT CARD APPLE DE 10€ !\n\n{code}\n\n#apple #giftcard #free #cadeau #tiktokfr"
        
        caption_input = driver.find_element(By.XPATH, '//textarea[@placeholder="Écrivez une légende..."]')
        caption_input.send_keys(caption)
        
        # Télécharger une vidéo factice (pré-enregistrée)
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys("/path/to/loop-video.mp4")
        
        time.sleep(10)
        
        post_button = driver.find_element(By.XPATH, '//button[contains(text(), "Publier")]')
        post_button.click()
        
        print(f"[TikTok] Code publié : {code} depuis @{account['username']}")
        
    except Exception as e:
        print(f"[Erreur TikTok] {e}")
    finally:
        driver.quit()

# Surveiller les nouveaux codes et publier
def monitor_and_post():
    published = load_published()
    accounts = load_accounts()['tiktok']
    
    while True:
        try:
            with open(VALID_CODES_FILE, 'r') as f:
                codes = [line.strip() for line in f if line.strip()]
            
            new_codes = set(codes) - published
            
            for code in new_codes:
                account = random.choice(accounts)
                threading.Thread(target=post_to_tiktok, args=(account, code)).start()
                published.add(code)
                with open(PUBLISHED_CODES_FILE, 'a') as f:
                    f.write(f"{code}\n")
                time.sleep(2)  # Éviter le spam
            
            time.sleep(10)
        except Exception as e:
            print(f"[Erreur surveillance] {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_and_post()
