// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Check API Status on Load
async function checkAPIStatus() {
    try {
        const response = await fetch(API_BASE_URL);
        const data = await response.json();
        console.log('✅ API Status:', data);
        
        // Update user count with API data if available
        updateUserCount();
    } catch (error) {
        console.error('❌ API Connection Error:', error);
        showNotification('Backend API non disponible. Certaines fonctionnalités sont limitées.', 'warning');
    }
}

// Update user count animation
function updateUserCount() {
    const userCountElement = document.getElementById('userCount');
    let count = 0;
    const target = 10000;
    const duration = 2000;
    const increment = target / (duration / 16);
    
    const counter = setInterval(() => {
        count += increment;
        if (count >= target) {
            userCountElement.textContent = '10,000+';
            clearInterval(counter);
        } else {
            userCountElement.textContent = Math.floor(count).toLocaleString() + '+';
        }
    }, 16);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'warning' ? '#f59e0b' : '#6366f1'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Login Modal
function showLoginModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2>Connexion</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="loginEmail" required placeholder="votre@email.com">
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" id="loginPassword" required placeholder="••••••••">
                </div>
                <button type="submit" class="btn-primary btn-large">Se connecter</button>
            </form>
            <p style="margin-top: 1rem; text-align: center;">
                Pas encore de compte? <a href="#" id="showRegister" style="color: #6366f1;">S'inscrire</a>
            </p>
        </div>
    `;
    
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.cssText = `
        background: #1e293b;
        padding: 2rem;
        border-radius: 20px;
        max-width: 400px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    `;
    
    document.body.appendChild(modal);
    
    // Close modal
    modal.querySelector('.close-modal').onclick = () => modal.remove();
    modal.onclick = (e) => {
        if (e.target === modal) modal.remove();
    };
    
    // Handle login form
    document.getElementById('loginForm').onsubmit = async (e) => {
        e.preventDefault();
        await handleLogin();
    };
    
    // Show register modal
    document.getElementById('showRegister').onclick = (e) => {
        e.preventDefault();
        modal.remove();
        showRegisterModal();
    };
}

// Register Modal
function showRegisterModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close-modal">&times;</span>
            <h2>Créer un compte</h2>
            <form id="registerForm">
                <div class="form-group">
                    <label>Nom complet</label>
                    <input type="text" id="registerName" required placeholder="John Doe">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="registerEmail" required placeholder="votre@email.com">
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" id="registerPassword" required placeholder="••••••••">
                </div>
                <button type="submit" class="btn-primary btn-large">S'inscrire</button>
            </form>
            <p style="margin-top: 1rem; text-align: center;">
                Déjà un compte? <a href="#" id="showLogin" style="color: #6366f1;">Se connecter</a>
            </p>
        </div>
    `;
    
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    `;
    
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.cssText = `
        background: #1e293b;
        padding: 2rem;
        border-radius: 20px;
        max-width: 400px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    `;
    
    document.body.appendChild(modal);
    
    // Close modal
    modal.querySelector('.close-modal').onclick = () => modal.remove();
    modal.onclick = (e) => {
        if (e.target === modal) modal.remove();
    };
    
    // Handle register form
    document.getElementById('registerForm').onsubmit = async (e) => {
        e.preventDefault();
        await handleRegister();
    };
    
    // Show login modal
    document.getElementById('showLogin').onclick = (e) => {
        e.preventDefault();
        modal.remove();
        showLoginModal();
    };
}

// Handle Login
async function handleLogin() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            showNotification('Connexion réussie! Bienvenue ' + data.user.full_name, 'success');
            document.querySelector('.modal').remove();
            updateUIForLoggedInUser(data.user);
        } else {
            showNotification(data.error || 'Erreur de connexion', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Erreur de connexion au serveur', 'error');
    }
}

// Handle Register
async function handleRegister() {
    const fullName = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                full_name: fullName,
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Compte créé avec succès! Connectez-vous maintenant.', 'success');
            document.querySelector('.modal').remove();
            showLoginModal();
        } else {
            showNotification(data.error || 'Erreur lors de la création du compte', 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showNotification('Erreur de connexion au serveur', 'error');
    }
}

// Update UI for logged in user
function updateUIForLoggedInUser(user) {
    const loginBtn = document.getElementById('loginBtn');
    loginBtn.textContent = user.full_name;
    loginBtn.onclick = (e) => {
        e.preventDefault();
        showUserMenu();
    };
}

// Show user menu
function showUserMenu() {
    showNotification('Menu utilisateur (À implémenter: Dashboard, Profil, Déconnexion)', 'info');
}

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Check API status
    checkAPIStatus();
    
    // Login button
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            showLoginModal();
        });
    }
    
    // Start buttons
    const startBtn = document.getElementById('startBtn');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            showRegisterModal();
        });
    }
    
    const ctaBtn = document.getElementById('ctaBtn');
    if (ctaBtn) {
        ctaBtn.addEventListener('click', () => {
            showRegisterModal();
        });
    }
    
    // Pricing buttons
    document.querySelectorAll('.btn-pricing').forEach(btn => {
        btn.addEventListener('click', () => {
            const token = localStorage.getItem('access_token');
            if (token) {
                showNotification('Redirection vers le paiement...', 'info');
                // Implement payment flow
            } else {
                showNotification('Veuillez vous connecter pour continuer', 'warning');
                showLoginModal();
            }
        });
    });
    
    // Check if user is already logged in
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    if (token && user) {
        updateUIForLoggedInUser(user);
    }
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        color: #94a3b8;
    }
    
    .form-group input {
        width: 100%;
        padding: 0.75rem;
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #f1f5f9;
        font-size: 1rem;
    }
    
    .form-group input:focus {
        outline: none;
        border-color: #6366f1;
    }
    
    .close-modal {
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2rem;
        cursor: pointer;
        color: #94a3b8;
        transition: color 0.3s;
    }
    
    .close-modal:hover {
        color: #f1f5f9;
    }
`;
document.head.appendChild(style);
