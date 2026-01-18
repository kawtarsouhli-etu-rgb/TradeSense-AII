// Optimiseur de performance pour TradeSense AI

// Désactiver les logs en production
if (process.env.NODE_ENV === 'production') {
  console.log = () => {};
}

// Optimisation du chargement des images
export const lazyLoadImage = (imgElement) => {
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          imageObserver.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }
};

// Optimisation du rendu
export const optimizeRendering = () => {
  // Utiliser requestAnimationFrame pour les animations
  window.requestAnimationFrame = window.requestAnimationFrame || 
                                window.webkitRequestAnimationFrame || 
                                window.mozRequestAnimationFrame || 
                                function(callback) { return window.setTimeout(callback, 16.66); };
  
  // Utiliser cancelAnimationFrame
  window.cancelAnimationFrame = window.cancelAnimationFrame ||
                               window.webkitCancelAnimationFrame ||
                               window.mozCancelAnimationFrame ||
                               function(id) { window.clearTimeout(id); };
};

// Nettoyage du localStorage
export const cleanLocalStorage = () => {
  try {
    // Conserver seulement les données essentielles
    const essentialKeys = ['access_token', 'refresh_token', 'theme', 'language'];
    const allKeys = Object.keys(localStorage);
    
    allKeys.forEach(key => {
      if (!essentialKeys.includes(key)) {
        localStorage.removeItem(key);
      }
    });
  } catch (error) {
    console.warn('Erreur lors du nettoyage du localStorage:', error);
  }
};

// Optimisation des appels API
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Initialisation des optimisations
export const initializePerformanceOptimizations = () => {
  optimizeRendering();
  cleanLocalStorage();
  
  // Désactiver les animations si le système est lent
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.body.classList.add('reduce-motion');
  }
};

// Optimisation du chargement des composants
export const lazyLoadComponent = (importFunc, retries = 3) => {
  return new Promise((resolve, reject) => {
    const doRetry = (attempt) => {
      importFunc()
        .then(module => resolve(module.default || module))
        .catch(error => {
          if (attempt === 0) {
            reject(error);
          } else {
            setTimeout(() => doRetry(attempt - 1), 1000);
          }
        });
    };
    doRetry(retries);
  });
};

// Optimisation du garbage collection
export const optimizeMemory = () => {
  // Planifier le nettoyage périodique
  setInterval(() => {
    // Nettoyer les objets temporaires
    if (window.gc) {
      window.gc();
    }
  }, 30000); // Toutes les 30 secondes
};

// Démarrer les optimisations
initializePerformanceOptimizations();