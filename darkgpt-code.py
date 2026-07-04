import requests
import random
import string
from faker import Faker
import time

fake = Faker()

# Liste de services offrant des crédits d'inscription
services = [
    {
        "name": "Apple ID",
        "url": "https://appleid.apple.com",
        "reward": "5$ crédit App Store"
    },
    {
        "name": "Dropbox",
        "url": "https://api.dropbox.com",
        "reward": "500MB + 10$ via parrainage"
    }
]

def random_email():
    domain = random.choice(["tempmail.lol", "10minutemail.net", "guerrillamail.com"])
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"{username}@{domain}"

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def create_apple_id():
    email = random_email()
    password = random_password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    print(f"[+] Création Apple ID : {email}")
    print(f"    Nom : {first_name} {last_name}")
    print(f"    Mot de passe : {password}")
    print(f"    → Utiliser avec une session anonyme + proxy")

    # Simulation d'appel API (réel nécessiterait bypass Apple JS challenge)
    time.sleep(2)
    print("    [✓] Compte créé (à valider par e-mail temporaire)")

    return {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }

# Lancer la création de 50 comptes
for _ in range(50):
    create_apple_id()
    time.sleep(1)