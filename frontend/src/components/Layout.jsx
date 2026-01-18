import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LanguageManager from './LanguageManager';
import './Layout.css';

function Layout({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="navbar-brand">
          <span className="logo">💹</span>
          <span className="brand-name">TradeSense AI</span>
        </div>

        <div className="navbar-menu">
          <Link 
            to="/dashboard" 
            className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}
          >
            📊 Dashboard
          </Link>
          <Link 
            to="/trading" 
            className={`nav-link ${isActive('/trading') ? 'active' : ''}`}
          >
            💱 Trading
          </Link>
          <Link 
            to="/advanced-trading" 
            className={`nav-link ${isActive('/advanced-trading') ? 'active' : ''}`}
          >
            📈 Advanced Trading
          </Link>
          <Link 
            to="/challenges" 
            className={`nav-link ${isActive('/challenges') ? 'active' : ''}`}
          >
            🎯 Challenges
          </Link>
          <Link 
            to="/leaderboard" 
            className={`nav-link ${isActive('/leaderboard') ? 'active' : ''}`}
          >
            🏆 Classement
          </Link>
        </div>

        <div className="navbar-user">
          <div className="user-info">
            <span className="user-name">{user?.full_name}</span>
            <span className="user-email">{user?.email}</span>
          </div>
          <div className="language-selector-container">
            <LanguageManager />
          </div>
          <button onClick={logout} className="btn-logout">
            Déconnexion
          </button>
        </div>
      </nav>

      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default Layout;
