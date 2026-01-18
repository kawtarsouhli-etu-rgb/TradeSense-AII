import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function DashboardPage() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="dashboard-page">
      <header className="dashboard-header">
        <div className="container mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-bold text-white">
              <span className="text-primary">Trade</span>Sense<span className="text-accent">.AI</span>
            </h1>
            <div className="flex items-center space-x-4">
              <span className="text-white">Bonjour, {user?.full_name || user?.email || 'Trader'}</span>
              <button 
                onClick={handleLogout}
                className="btn btn-outline"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="container mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold mb-6">Tableau de bord</h2>
          
          <div className="dashboard-cards">
            <Link to="/trading" className="dashboard-card">
              <h3>Trading</h3>
              <p>Accédez à la plateforme de trading</p>
            </Link>
            
            <Link to="/challenges" className="dashboard-card">
              <h3>Challenges</h3>
              <p>Voir vos challenges de trading</p>
            </Link>
            
            <div className="dashboard-card">
              <h3>Statistiques</h3>
              <p>Vos performances de trading</p>
            </div>
            
            <div className="dashboard-card">
              <h3>Portefeuille</h3>
              <p>Votre capital et profits</p>
            </div>
          </div>
        </div>
      </main>

      <footer className="dashboard-footer">
        <div className="container mx-auto px-4 py-6">
          <p>© 2024 TradeSense AI. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
}

export default DashboardPage;