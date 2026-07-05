// Gestion des commandes
let orders = JSON.parse(localStorage.getItem('shadowboost_orders') || '[]');
let currentId = parseInt(localStorage.getItem('shadowboost_id') || '1000');

// Générer un ID unique
function generateId() {
  return 'SB-' + currentId + '-' + Math.floor(1000 + Math.random() * 9000);
}

// Ajouter une commande
document.getElementById('orderForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const platform = document.getElementById('platform').value;
  const service = document.getElementById('service').value;
  const quantity = parseInt(document.getElementById('quantity').value);

  const orderId = generateId();
  const estimatedTime = Math.max(1, Math.floor(quantity / 100)) * 30; // secondes
  const startTime = new Date().getTime();

  const order = {
    id: orderId,
    username,
    platform,
    service,
    quantity,
    status: 'pending',
    startTime,
    estimatedTime,
    delivered: 0
  };

  orders.push(order);
  currentId++;
  localStorage.setItem('shadowboost_orders', JSON.stringify(orders));
  localStorage.setItem('shadowboost_id', currentId.toString());

  alert(`Commande lancée ! ID: ${orderId}\nSuivez-la dans la section "Suivi de Commande".`);
  simulateDelivery(order);
});

// Simuler la livraison
function simulateDelivery(order) {
  const interval = 1000;
  let elapsed = 0;
  const step = order.quantity / (order.estimatedTime * 2); // 2 livraisons par seconde

  const timer = setInterval(() => {
    elapsed += 1;
    order.delivered += step;
    if (order.delivered >= order.quantity) {
      order.delivered = order.quantity;
      order.status = 'completed';
    } else {
      order.status = 'in_progress';
    }
    order = updateOrder(order);
    if (order.status === 'completed') {
      clearInterval(timer);
      notifyUser(order);
    }
  }, interval);
}

// Mettre à jour la commande
function updateOrder(updatedOrder) {
  orders = orders.map(o => o.id === updatedOrder.id ? updatedOrder : o);
  localStorage.setItem('shadowboost_orders', JSON.stringify(orders));
  updateAdminPanel();
  return updatedOrder;
}

// Suivre une commande
function trackOrder() {
  const trackId = document.getElementById('trackId').value.trim();
  const order = orders.find(o => o.id === trackId);
  if (!order) {
    alert('Commande non trouvée.');
    return;
  }

  document.getElementById('orderStatus').style.display = 'block';
  document.getElementById('statusText').textContent = order.status === 'completed' ? 'Terminée' : 'En cours';
  document.getElementById('resultCount').textContent = order.quantity.toLocaleString();
  const progress = (order.delivered / order.quantity) * 100;
  document.getElementById('progressBar').style.width = progress + '%';
  const remaining = Math.max(0, order.estimatedTime - Math.floor((new Date().getTime() - order.startTime) / 1000));
  document.getElementById('timeLeft').textContent = remaining > 0 ? `${Math.ceil(remaining / 60)} min` : 'Terminé';
}

// Notification utilisateur
function notifyUser(order) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification('Boost Terminé', {
      body: `Votre commande ${order.service} sur ${order.platform} est terminée ! ${order.quantity} unités livrées.`,
      icon: 'https://cdn-icons-png.flaticon.com/512/1793/1793496.png'
    });
  }
}

// Initialisation
function init() {
  if ('Notification' in window && Notification.permission !== 'denied') {
    Notification.requestPermission();
  }
  updateAdminPanel();
}

// Mise à jour du tableau admin
function updateAdminPanel() {
  const table = document.getElementById('statusTable').getElementsByTagName('tbody')[0];
  table.innerHTML = '';
  orders.forEach(order => {
    const row = table.insertRow();
    row.insertCell(0).textContent = order.id;
    row.insertCell(1).textContent = order.username;
    row.insertCell(2).textContent = `${order.platform} - ${order.service}`;
    row.insertCell(3).textContent = order.quantity.toLocaleString();
    row.insertCell(4).textContent = order.status === 'completed' ? '✅ Terminée' : '🔄 En cours';
    const remaining = Math.max(0, order.estimatedTime - Math.floor((new Date().getTime() - order.startTime) / 1000));
    row.insertCell(5).textContent = remaining > 0 ? `${Math.ceil(remaining / 60)} min` : '0 min';
  });
}

// Détecter admin (saisir "admin" comme nom)
document.addEventListener('input', function(e) {
  if (e.target.id === 'username' && e.target.value.toLowerCase() === 'admin') {
    document.getElementById('admin').style.display = 'block';
    updateAdminPanel();
  }
});

window.onload = init;
