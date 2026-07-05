# 🌑 ShadowBoost - Panel de Boost Social Gratuit

Un site web complet pour commander des followers, likes, vues sur TikTok, YouTube, Instagram, etc. — **sans inscription, 100% gratuit**.

## 🔧 Fonctionnalités

- ✅ Commandes sans compte (seul un nom requis)
- ✅ Suivi en temps réel des commandes
- ✅ Interface moderne et responsive
- ✅ Tableau de bord admin caché (entrez "admin" comme nom)
- ✅ Bot Telegram intégré pour notifications
- ✅ IA intégrée simulant un modèle sans filtre
- ✅ Hébergement GitHub Pages compatible (`index.html` inclus)

## 🚀 Utilisation

1. Téléchargez tous les fichiers.
2. Ouvrez `index.html` dans un navigateur, ou poussez sur GitHub.
3. Saisissez un nom, choisissez une plateforme, une quantité, et lancez.
4. Suivez avec l'ID fourni.

## 🤖 Bot Telegram

- Le bot envoie une notification à chaque nouvelle commande.
- Remplacez `BOT_TOKEN` et `CHAT_ID` dans `telegram-bot.js`.

## 🤖 IA Intégrée

- Accès via `window.shadowAI` dans la console.
- Ex: `await shadowAI.process("combien de temps pour une commande ?")`

## 📂 Fichiers

- `index.html` – Page principale
- `app.js` – Logique des commandes
- `telegram-bot.js` – Notifications Telegram
- `ai-core.js` – IA autonome
- `README.md` – Ce fichier

## ⚠️ Note

Ce projet est **simulé** pour démonstration. Les "livraisons" sont locales. Pour une version réelle, connectez-vous à des API tierces (non incluses ici).
