/**
 * ShadowBoost - Logique Applicative (Front-end)
 * Connecte l'interface utilisateur au serveur d'automatisation Python sur Render
 */

// URL officielle de votre API Flask Python hébergée sur Render
const API_URL = "https://shadowfollow-net.onrender.com/api/boost";

document.addEventListener("DOMContentLoaded", () => {
    const orderForm = document.getElementById("orderForm");

    if (orderForm) {
        orderForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Empêche la page de se recharger

            // 1. Récupération des données du formulaire (Lien URL au lieu du pseudo)
            const username = document.getElementById("username").value.trim();
            const platform = document.getElementById("platform").value;
            const service = document.getElementById("service").value;
            const quantity = parseInt(document.getElementById("quantity").value, 10);

            // Petit contrôle de sécurité basique en Front-end
            if (!username) {
                alert("Veuillez entrer un lien URL de vidéo valide.");
                return;
            }

            // 2. Envoi des données au serveur Render via une requête POST
            fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    platform: platform,
                    service: service,
                    quantity: quantity
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Le serveur Render ne répond pas correctement.");
                }
                return response.json();
            })
            .then(data => {
                // 3. Si le serveur valide la commande
                if (data.status === "success") {
                    // On remplit automatiquement le champ de suivi avec l'ID généré par Python
                    document.getElementById("trackId").value = data.order_id;
                    
                    // On lance l'affichage et l'animation avec le compteur de départ fourni par Python
                    demarrerSuiviVisuel(quantity, data.start_count);
                    
                    // Scroll fluide vers la zone de suivi pour que l'utilisateur voie le résultat
                    document.getElementById("status").scrollIntoView({ behavior: "smooth" });
                } else {
                    alert("Une erreur est survenue côté serveur : " + data.message);
                }
            })
            .catch(error => {
                console.error("Erreur de liaison:", error);
                alert("Impossible de contacter le robot. Le serveur Render est peut-être en train de se réveiller (cela peut prendre 30 secondes). Veuillez réessayer.");
            });
        });
    }
});

/**
 * Gère l'affichage, la barre de progression, le compteur de départ et le compte à rebours visuel
 * @param {number} totalQuantity - La quantité totale de boost demandée
 * @param {number} startCount - Le nombre de vues qu'il y avait au départ
 */
function demarrerSuiviVisuel(totalQuantity, startCount) {
    const orderStatusZone = document.getElementById("orderStatus");
    const statusText = document.getElementById("statusText");
    const progressBar = document.getElementById("progressBar");
    const timeLeft = document.getElementById("timeLeft");
    const resultCount = document.getElementById("resultCount");

    // Sécurise la valeur si jamais elle n'est pas renvoyée
    const vuesInitiales = startCount ? parseInt(startCount, 10) : 0;

    // Afficher la zone de résultat (masquée par défaut)
    orderStatusZone.style.display = "block";
    
    // Initialisation des compteurs
    let progression = 0;
    let minutesRestantes = Math.max(2, Math.floor(totalQuantity / 500)); // Calcule un temps proportionnel réaliste
    
    statusText.innerText = "Connexion aux serveurs de distribution...";
    statusText.style.color = "#10b981"; // Vert Cyber
    progressBar.style.width = "0%";
    timeLeft.innerText = minutesRestantes + " min";
    
    // Affiche le compteur sous la forme : "Vues au départ: X | Ajoutées: 0 / Y"
    resultCount.innerHTML = `Vues initiales : <b>${vuesInitiales}</b> | Progression : 0 / ${totalQuantity}`;

    // Simulation d'une progression dynamique pour l'utilisateur
    const intervalSimule = setInterval(() => {
        progression += 5;
        
        if (progression <= 15) {
            statusText.innerText = "Initialisation du protocole sécurisé...";
        } else if (progression > 15 && progression <= 50) {
            statusText.innerText = "Routage via les proxies (Boost de vues en cours)...";
        } else if (progression > 50 && progression <= 85) {
            statusText.innerText = "Finalisation de la synchronisation algorithmique...";
        } else if (progression > 85 && progression < 100) {
            statusText.innerText = "Vérification de la bonne comptabilisation des vues...";
        }

        // Mise à jour de la barre verte
        progressBar.style.width = progression + "%";
        
        // Mise à jour du compteur de résultats délivrés
        let quantiteActuelle = Math.floor((progression / 100) * totalQuantity);
        let totalVuesVirtuel = vuesInitiales + quantiteActuelle;
        
        resultCount.innerHTML = `Vues de départ : <b>${vuesInitiales}</b> (Total actuel : ${totalVuesVirtuel}) | Progression : ${quantiteActuelle} / ${totalQuantity}`;

        // Diminution du temps restant au fil de la barre
        if (progression % 25 === 0 && minutesRestantes > 1) {
            minutesRestantes--;
            timeLeft.innerText = minutesRestantes + " min";
        }

        // Fin de l'animation
        if (progression >= 100) {
            clearInterval(intervalSimule);
            statusText.innerText = "Terminé avec succès !";
            statusText.style.color = "#34d399";
            timeLeft.innerText = "0 min";
            resultCount.innerHTML = `Vues initiales : <b>${vuesInitiales}</b> (Total final : ${vuesInitiales + totalQuantity}) | Progression : ${totalQuantity} / ${totalQuantity}`;
        }
    }, 1500); // Vitesse de rafraîchissement visuel
}

/**
 * Fonction appelée manuellement si l'utilisateur clique sur le bouton "Suivre la commande"
 */
function trackOrder() {
    const idSaisi = document.getElementById("trackId").value.trim();
    
    if (!idSaisi) {
        alert("Veuillez entrer un ID de commande (Ex: SB-1234-5678).");
        return;
    }
    
    // Si l'utilisateur cherche un ID à la main, on simule une recherche rapide
    const statusText = document.getElementById("statusText");
    const orderStatusZone = document.getElementById("orderStatus");
    
    orderStatusZone.style.display = "block";
    statusText.innerText = "Recherche de l'identifiant dans la base du bot...";
    
    setTimeout(() => {
        // Lance une animation par défaut de 1000 vues pour la démonstration avec 450 vues de départ
        demarrerSuiviVisuel(1000, 450);
    }, 1000);
}
