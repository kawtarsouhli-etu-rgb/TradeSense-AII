// Preload script for faster trading page loading
console.log('🚀 Initializing Trading Page Optimization...');

// Preload critical assets
const preloadAssets = () => {
  // Preload fonts if any
  const fonts = [
    // Add font URLs here if needed
  ];
  
  fonts.forEach(fontUrl => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'font';
    link.href = fontUrl;
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
  });
};

// Optimize initial render
const optimizeRender = () => {
  // Remove loading indicators quickly
  setTimeout(() => {
    const loaders = document.querySelectorAll('.loading, .spinner');
    loaders.forEach(loader => {
      loader.style.opacity = '0';
      setTimeout(() => loader.remove(), 300);
    });
  }, 500);
  
  // Enable smooth transitions
  document.body.style.transition = 'opacity 0.3s ease';
};

// Cache frequently used data
const setupCache = () => {
  // Setup localStorage for user preferences
  if (!localStorage.getItem('tradingPreferences')) {
    localStorage.setItem('tradingPreferences', JSON.stringify({
      lastSymbol: 'AAPL',
      lastMarket: 'US',
      theme: 'dark'
    }));
  }
};

// Initialize optimizations
document.addEventListener('DOMContentLoaded', () => {
  preloadAssets();
  optimizeRender();
  setupCache();
  
  console.log('✅ Trading page optimizations loaded');
});

// Performance monitoring
const measurePerformance = () => {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.entryType === 'navigation') {
        console.log(`📈 Page load time: ${entry.loadEventEnd - entry.fetchStart}ms`);
      }
    }
  });
  
  observer.observe({ entryTypes: ['navigation'] });
};

measurePerformance();