import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { I18nextProvider, useTranslation } from 'react-i18next';
import i18n from './i18n';
import { AuthProvider, useAuth } from './context/AuthContext';
import { PriceProvider } from './context/PriceContext';
import { ThemeProvider } from './context/ThemeContext';
import ThemeToggle from './components/ThemeToggle';
import LanguageSwitcher from './components/LanguageSwitcher';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import Dashboard from './pages/Dashboard';
import TradingPage from './pages/TradingPage';
import AdvancedTradingPage from './pages/AdvancedTradingPage';
import LandingPage from './pages/LandingPage';


import PaymentPage from './pages/PaymentPage';
import ChallengesPage from './pages/ChallengesPage';
import LeaderboardPage from './pages/LeaderboardPage';
import './App.css';
import './utils/tradingOptimizer'; // Performance optimizer

// Layout Component with Language Switcher
const Layout = ({ children }) => {
  const { t } = useTranslation();
  
  return (
    <div className="layout">
      {/* Header */}
      <header className="app-header">
        <div className="container mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-bold text-white">
              <span className="text-primary">Trade</span>Sense<span className="text-accent">.AI</span>
            </h1>
            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <LanguageSwitcher />
            </div>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="app-main">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="app-footer">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-gray-400">
            <p>{t('copyright', '© 2024 TradeSense AI. All rights reserved.')}</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <div className="loader">Loading...</div>
      </div>
    );
  }
  
  return (
    <Layout>
      {isAuthenticated ? children : <Navigate to="/login" />}
    </Layout>
  );
};

function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage />} />
      <Route path="/register" element={isAuthenticated ? <Navigate to="/dashboard" /> : <RegisterPage />} />
      
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />
      
      <Route path="/trading" element={
        <ProtectedRoute>
          <TradingPage />
        </ProtectedRoute>
      } />
      
      <Route path="/advanced-trading" element={
        <ProtectedRoute>
          <AdvancedTradingPage />
        </ProtectedRoute>
      } />
      
      <Route path="/challenges" element={
        <ProtectedRoute>
          <ChallengesPage />
        </ProtectedRoute>
      } />
      
      <Route path="/leaderboard" element={
        <ProtectedRoute>
          <LeaderboardPage />
        </ProtectedRoute>
      } />
      

    </Routes>
  );
}

function App() {
  return (
    <ThemeProvider>
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <PriceProvider>
            <Router>
              <AppRoutes />
            </Router>
          </PriceProvider>
        </AuthProvider>
      </I18nextProvider>
    </ThemeProvider>
  );
}

export default App;
