// Bot Telegram pour notifications et commandes
// Remplacez TOKEN par votre vrai token Telegram Bot
const BOT_TOKEN = '8894926896:AAGdyt8hpLthIf3f2gI-IB3YxXjtq5BcTp4';
const CHAT_ID = '123456789'; // Votre ID Telegram

// Envoyer notification Telegram
function sendTelegramNotification(message) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: CHAT_ID,
      text: message,
      parse_mode: 'HTML'
    })
  }).catch(err => console.error('Telegram send failed:', err));
}

// Intercepter les nouvelles commandes
window.addEventListener('storage', function(e) {
  if (e.key === 'shadowboost_orders') {
    const newOrders = JSON.parse(e.newValue || '[]');
    const oldOrders = JSON.parse(e.oldValue || '[]');
    if (newOrders.length > oldOrders.length) {
      const latest = newOrders[newOrders.length - 1];
      const msg = `
🚀 <b>Nouvelle Commande</b>
• ID: <code>${latest.id}</code>
• Utilisateur: ${latest.username}
• Plateforme: ${latest.platform}
• Service: ${latest.service}
• Quantité: ${latest.quantity.toLocaleString()}
      `.trim();
      sendTelegramNotification(msg);
    }
  }
});

// Fonction pour activer le bot (appelé depuis AI)
function startTelegramBot() {
  console.log('Telegram Bot activé. En attente de commandes...');
  sendTelegramNotification('🟢 ShadowBoost Bot est en ligne.');
}
