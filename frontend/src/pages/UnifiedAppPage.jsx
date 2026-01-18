import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './UnifiedAppPage.css';

function UnifiedAppPage() {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [marketData, setMarketData] = useState([]);
  const [positions, setPositions] = useState([]);
  
  // Charger les données du marché
  useEffect(() => {
    // Simulation de données de marché
    const mockMarketData = [
      { symbol: 'AAPL', price: 175.43, change: 2.34, changePercent: 1.35 },
      { symbol: 'TSLA', price: 248.50, change: -3.21, changePercent: -1.27 },
      { symbol: 'GOOGL', price: 138.21, change: 1.87, changePercent: 1.37 },
      { symbol: 'MSFT', price: 375.80, change: 2.15, changePercent: 0.57 },
      { symbol: 'AMZN', price: 178.22, change: 0.89, changePercent: 0.50 },
      { symbol: 'BTC-USD', price: 43250.67, change: 125.43, changePercent: 0.29 },
      { symbol: 'ETH-USD', price: 2650.34, change: -15.67, changePercent: -0.59 },
      { symbol: 'EURUSD', price: 1.0856, change: 0.0023, changePercent: 0.21 }
    ];
    setMarketData(mockMarketData);
    
    // Simulation de positions
    const mockPositions = [
      { id: 1, symbol: 'AAPL', quantity: 10, avgPrice: 170.25, currentPrice: 175.43, pnl: 51.80 },
      { id: 2, symbol: 'BTC-USD', quantity: 0.5, avgPrice: 42500, currentPrice: 43250.67, pnl: 375.34 }
    ];
    setPositions(mockPositions);
  }, []);

  const handleLogout = () => {
    logout();
  };

  // Données factices pour démonstration
  const portfolioData = {
    balance: 10000,
    profit: 1250,
    profitPercent: 12.5,
    trades: 42
  };

  const recentTrades = [
    { id: 1, asset: 'AAPL', type: 'BUY', amount: 100, profit: 25.50, time: '10:30' },
    { id: 2, asset: 'BTC-USD', type: 'SELL', amount: 50, profit: -15.20, time: '11:15' },
    { id: 3, asset: 'GOOGL', type: 'BUY', amount: 75, profit: 42.30, time: '14:20' }
  ];

  const challenges = [
    { id: 1, name: 'Challenge Starter', status: 'Actif', progress: 65, target: '10%', risk: '5%' },
    { id: 2, name: 'Challenge Pro', status: 'En attente', progress: 0, target: '10%', risk: '3%' },
    { id: 3, name: 'Challenge Elite', status: 'Verrouillé', progress: 0, target: '10%', risk: '2%' }
  ];

  const leaderboard = [
    { rank: 1, name: 'Ahmed K.', profit: 2450, trades: 128 },
    { rank: 2, name: 'Fatima M.', profit: 1980, trades: 95 },
    { rank: 3, name: 'Youssef B.', profit: 1750, trades: 112 },
    { rank: 4, name: 'Mohamed T.', profit: 1520, trades: 87 },
    { rank: 5, name: 'Nadia L.', profit: 1340, trades: 103 }
  ];

  return (
    <div className="unified-app">
      {/* Header */}
      <header className="app-header">
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

      {/* Navigation */}
      <nav className="app-nav">
        <div className="container mx-auto px-4">
          <div className="nav-tabs">
            <button 
              className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`nav-tab ${activeTab === 'trading' ? 'active' : ''}`}
              onClick={() => setActiveTab('trading')}
            >
              Trading
            </button>
            <button 
              className={`nav-tab ${activeTab === 'challenges' ? 'active' : ''}`}
              onClick={() => setActiveTab('challenges')}
            >
              Challenges
            </button>
            <button 
              className={`nav-tab ${activeTab === 'payment' ? 'active' : ''}`}
              onClick={() => setActiveTab('payment')}
            >
              Paiement
            </button>
            <button 
              className={`nav-tab ${activeTab === 'leaderboard' ? 'active' : ''}`}
              onClick={() => setActiveTab('leaderboard')}
            >
              Classement
            </button>
          </div>
        </div>
      </nav>

      {/* Contenu principal */}
      <main className="app-main">
        <div className="container mx-auto px-4 py-6">
          {activeTab === 'dashboard' && (
            <div className="dashboard-content">
              <h2 className="text-2xl font-bold mb-6">Tableau de Bord</h2>
              
              {/* Statistiques principales */}
              <div className="stats-grid">
                <div className="stat-card">
                  <h3>Solde</h3>
                  <p className="stat-value">${portfolioData.balance.toLocaleString()}</p>
                </div>
                <div className="stat-card">
                  <h3>Profit</h3>
                  <p className={`stat-value ${portfolioData.profit >= 0 ? 'positive' : 'negative'}`}>
                    {portfolioData.profit >= 0 ? '+' : ''}${portfolioData.profit.toLocaleString()}
                  </p>
                  <p className={`stat-percent ${portfolioData.profitPercent >= 0 ? 'positive' : 'negative'}`}>
                    {portfolioData.profitPercent >= 0 ? '+' : ''}{portfolioData.profitPercent}%
                  </p>
                </div>
                <div className="stat-card">
                  <h3>Total Trades</h3>
                  <p className="stat-value">{portfolioData.trades}</p>
                </div>
              </div>

              {/* Trades récents */}
              <div className="recent-trades">
                <h3>Derniers Trades</h3>
                <table className="trades-table">
                  <thead>
                    <tr>
                      <th>Actif</th>
                      <th>Type</th>
                      <th>Montant</th>
                      <th>Profit</th>
                      <th>Heure</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentTrades.map(trade => (
                      <tr key={trade.id}>
                        <td>{trade.asset}</td>
                        <td className={trade.type === 'BUY' ? 'buy' : 'sell'}>{trade.type}</td>
                        <td>${trade.amount}</td>
                        <td className={trade.profit >= 0 ? 'positive' : 'negative'}>
                          {trade.profit >= 0 ? '+' : ''}{trade.profit.toFixed(2)}
                        </td>
                        <td>{trade.time}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'trading' && (
            <div className="trading-content">
              <h2 className="text-2xl font-bold mb-6">Plateforme de Trading Avancée</h2>
              
              {/* Positions actuelles */}
              <div className="current-positions">
                <h3>Vos Positions</h3>
                <table className="positions-table">
                  <thead>
                    <tr>
                      <th>Actif</th>
                      <th>Qté</th>
                      <th>Prix Moyen</th>
                      <th>Prix Actuel</th>
                      <th>PNL</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {positions.map(position => (
                      <tr key={position.id}>
                        <td>{position.symbol}</td>
                        <td>{position.quantity}</td>
                        <td>${position.avgPrice.toFixed(2)}</td>
                        <td>${position.currentPrice.toFixed(2)}</td>
                        <td className={position.pnl >= 0 ? 'positive' : 'negative'}>
                          ${position.pnl.toFixed(2)}
                        </td>
                        <td>
                          <button className="btn btn-outline btn-small">Fermer</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
              <div className="trading-interface">
                <div className="trading-chart">
                  <div className="chart-placeholder">
                    <p>Graphique de trading avancé (Simulation)</p>
                    <div className="market-data">
                      <h4>Données du Marché</h4>
                      <table className="market-data-table">
                        <thead>
                          <tr>
                            <th>Actif</th>
                            <th>Prix</th>
                            <th>Changement</th>
                          </tr>
                        </thead>
                        <tbody>
                          {marketData.map((item, index) => (
                            <tr key={index}>
                              <td>{item.symbol}</td>
                              <td>{item.price.toLocaleString()}</td>
                              <td className={item.change >= 0 ? 'positive' : 'negative'}>
                                {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)} ({item.changePercent >= 0 ? '+' : ''}{item.changePercent.toFixed(2)}%)
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                
                <div className="trading-controls">
                  <div className="order-form">
                    <h3>Nouvel Ordre</h3>
                    <select className="form-select">
                      <option>AAPL</option>
                      <option>TSLA</option>
                      <option>GOOGL</option>
                      <option>BTC-USD</option>
                      <option>ETH-USD</option>
                      <option>MSFT</option>
                      <option>AMZN</option>
                      <option>EURUSD</option>
                    </select>
                    <div className="order-type">
                      <button className="btn btn-buy">BUY</button>
                      <button className="btn btn-sell">SELL</button>
                    </div>
                    <div className="order-params">
                      <input type="number" placeholder="Quantité" className="form-input" />
                      <input type="number" placeholder="Stop Loss" className="form-input" />
                      <input type="number" placeholder="Take Profit" className="form-input" />
                    </div>
                    <button className="btn btn-primary btn-block">Exécuter l'ordre</button>
                  </div>
                  
                  <div className="quick-actions">
                    <h4>Actions Rapides</h4>
                    <div className="quick-action-buttons">
                      <button className="btn btn-quick">Buy 100</button>
                      <button className="btn btn-quick">Sell 100</button>
                      <button className="btn btn-quick">Buy 1000</button>
                      <button className="btn btn-quick">Sell 1000</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'challenges' && (
            <div className="challenges-content">
              <h2 className="text-2xl font-bold mb-6">Challenges de Trading</h2>
              <div className="challenges-grid">
                {challenges.map(challenge => (
                  <div key={challenge.id} className="challenge-card">
                    <h3>{challenge.name}</h3>
                    <div className="challenge-status">
                      <span className={`status-badge ${challenge.status.toLowerCase().replace(' ', '-')}`}>
                        {challenge.status}
                      </span>
                    </div>
                    <div className="challenge-details">
                      <p><strong>Progression:</strong> {challenge.progress}%</p>
                      <p><strong>Objectif:</strong> {challenge.target} profit</p>
                      <p><strong>Risque Max:</strong> {challenge.risk} par jour</p>
                    </div>
                    <div className="challenge-progress">
                      <div 
                        className="progress-bar" 
                        style={{ width: `${challenge.progress}%` }}
                      ></div>
                    </div>
                    <button className="btn btn-primary btn-block">
                      {challenge.status === 'Actif' ? 'Participer' : 'Démarrer'}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'payment' && (
            <div className="payment-content">
              <h2 className="text-2xl font-bold mb-6">Paiement & Abonnements</h2>
              <div className="payment-options">
                <div className="subscription-plans">
                  <div className="plan-card">
                    <h3>Starter</h3>
                    <p className="price">200 DH</p>
                    <p className="duration">par mois</p>
                    <ul className="plan-features">
                      <li>✅ Capital: 5,000 DH</li>
                      <li>✅ Support de base</li>
                      <li>✅ Accès communauté</li>
                    </ul>
                    <button className="btn btn-outline">Sélectionner</button>
                  </div>
                  
                  <div className="plan-card popular">
                    <div className="popular-badge">Populaire</div>
                    <h3>Pro</h3>
                    <p className="price">500 DH</p>
                    <p className="duration">par mois</p>
                    <ul className="plan-features">
                      <li>✅ Capital: 10,000 DH</li>
                      <li>✅ Support prioritaire</li>
                      <li>✅ Analyses IA avancées</li>
                      <li>✅ Webinaires exclusifs</li>
                    </ul>
                    <button className="btn btn-primary">Sélectionner</button>
                  </div>
                  
                  <div className="plan-card">
                    <h3>Elite</h3>
                    <p className="price">1,000 DH</p>
                    <p className="duration">par mois</p>
                    <ul className="plan-features">
                      <li>✅ Capital: 25,000 DH</li>
                      <li>✅ Support VIP 24/7</li>
                      <li>✅ Coach personnel</li>
                      <li>✅ Accès anticipé</li>
                    </ul>
                    <button className="btn btn-outline">Sélectionner</button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'leaderboard' && (
            <div className="leaderboard-content">
              <h2 className="text-2xl font-bold mb-6">Classement des Traders</h2>
              <div className="leaderboard-table">
                <table className="rankings-table">
                  <thead>
                    <tr>
                      <th>Position</th>
                      <th>Trader</th>
                      <th>Profit ($)</th>
                      <th>Trades</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.map(player => (
                      <tr key={player.rank}>
                        <td className="rank-cell">
                          <span className={`rank-badge rank-${player.rank}`}>
                            {player.rank}
                          </span>
                        </td>
                        <td>{player.name}</td>
                        <td className="positive">{player.profit}</td>
                        <td>{player.trades}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="container mx-auto px-4 py-6">
          <p>© 2024 TradeSense AI. Tous droits réservés.</p>
        </div>
      </footer>
    </div>
  );
}

export default UnifiedAppPage;