// Fonction pour nettoyer le stockage d'authentification
export const clearAuthStorage = () => {
  try {
    // Supprimer tous les tokens d'authentification
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    // Supprimer d'autres données d'authentification potentielles
    const keysToRemove = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && (key.includes('token') || key.includes('auth'))) {
        keysToRemove.push(key);
      }
    }
    
    keysToRemove.forEach(key => {
      localStorage.removeItem(key);
    });
    
    console.log('Stockage d\'authentification nettoyé');
  } catch (error) {
    console.error('Erreur lors du nettoyage du stockage:', error);
  }
};

// Fonction pour forcer la déconnexion
export const forceLogout = () => {
  clearAuthStorage();
  // Rafraîchir la page pour s'assurer que tous les états sont réinitialisés
  window.location.href = '/';
};