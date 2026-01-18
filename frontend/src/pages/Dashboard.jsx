import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { challengeAPI, tradingAPI, marketAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

function Dashboard() {
  const { user } = useAuth();
  const { t } = useTranslation();
  const [challenges, setChallenges] = useState([]);
  const [activeChallenge, setActiveChallenge] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
    // Update watchlist every 15 seconds (instead of 10)
    const interval = setInterval(() => {
      marketAPI.getWatchlist()
        .then(res => setWatchlist(res.data.data || []))
        .catch(err => console.error('Watchlist update failed:', err));
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      // Load challenges - FAST (no external API)
      const challengesRes = await challengeAPI.getChallenges();
      const userChallenges = challengesRes.data.challenges || [];
      setChallenges(userChallenges);

      // Find active challenge
      const active = userChallenges.find(c => c.status === 'ACTIVE');
      setActiveChallenge(active);
      
      // Stop loading here to show UI faster
      setLoading(false);

      // Load metrics in background (non-blocking)
      if (active) {
        tradingAPI.getMetrics(active.id)
          .then(res => setMetrics(res.data.metrics))
          .catch(err => console.error('Error loading metrics:', err));
      }

      // Load watchlist in background (non-blocking)
      marketAPI.getWatchlist()
        .then(res => setWatchlist(res.data.data || []))
        .catch(err => console.error('Error loading watchlist:', err));
        
    } catch (error) {
      console.error('Error loading dashboard:', error);
      setError(t('loadingError', 'Loading error. Please refresh the page.'));
      setChallenges([]);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader">{t('loading')}</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1>{t('welcome')}, {user?.full_name} 👋</h1>
          <p className="subtitle">{t('hereIsYourTradingOverview', 'Here is your trading overview')}</p>
        </div>
      </div>

        {error && (
          <div className="alert alert-danger">
            {error}
          </div>
        )}

        {activeChallenge ? (
          <div className="dashboard-grid">
            {/* Challenge Stats */}
            <div className="card challenge-overview">
              <div className="card-header">
                <h2 className="card-title">{t('activeChallenge', 'Active Challenge')}</h2>
                <span className={`badge badge-${getStatusBadge(activeChallenge.status)}`}>
                  {t(activeChallenge.status.toLowerCase())}
                </span>
              </div>
              
              <div className="challenge-stats">
                <div className="stat-item">
                  <span className="stat-label">{t('currentBalance', 'Current Balance')}</span>
                  <span className="stat-value">${activeChallenge.current_balance.toFixed(2)}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('initialBalance', 'Initial Balance')}</span>
                  <span className="stat-value">${activeChallenge.initial_balance.toFixed(2)}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('pnl', 'P&L')}</span>
                  <span className={`stat-value ${getPnLClass(activeChallenge.current_balance - activeChallenge.initial_balance)}`}>
                    ${(activeChallenge.current_balance - activeChallenge.initial_balance).toFixed(2)}
                  </span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">{t('profitTarget', 'Profit Target')}</span>
                  <span className="stat-value">${activeChallenge.profit_target.toFixed(2)}</span>
                </div>
              </div>

              {metrics && (
                <div className="metrics-details">
                  <div className="metric-row">
                    <span>Progression vers objectif:</span>
                    <span className="text-primary">{metrics.target.progress_pct.toFixed(1)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{width: `${Math.min(metrics.target.progress_pct, 100)}%`}}
                    ></div>
                  </div>
                  
                  <div className="metric-row mt-2">
                    <span>P&L Journalier:</span>
                    <span className={getPnLClass(metrics.daily.pnl)}>
                      {metrics.daily.pnl.toFixed(2)} DH ({metrics.daily.pnl_pct.toFixed(2)}%)
                    </span>
                  </div>
                  
                  <div className="metric-row">
                    <span>Buffer perte totale:</span>
                    <span className={metrics.total.remaining_loss_buffer > 100 ? 'text-success' : 'text-warning'}>
                      {metrics.total.remaining_loss_buffer.toFixed(2)} DH
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="card quick-actions">
              <h2 className="card-title">{t('quickActions', 'Quick Actions')}</h2>
              <div className="actions-grid">
                <a href="/trading" className="action-btn">
                  <span className="action-icon">💱</span>
                  <span className="action-text">{t('startTrading', 'Start Trading')}</span>
                </a>
                <a href="/challenges" className="action-btn">
                  <span className="action-icon">🎯</span>
                  <span className="action-text">{t('myChallenges', 'My Challenges')}</span>
                </a>
                <a href="/leaderboard" className="action-btn">
                  <span className="action-icon">🏆</span>
                  <span className="action-text">{t('leaderboard', 'Leaderboard')}</span>
                </a>
              </div>
            </div>

            {/* Watchlist */}
            <div className="card watchlist-card">
              <div className="card-header">
                <h2 className="card-title">{t('realTimePrices', 'Real Time Prices')} 🔴</h2>
                <span className="live-indicator">{t('live', 'LIVE')}</span>
              </div>
              
              <div className="watchlist">
                {watchlist.length === 0 ? (
                  <div className="empty-watchlist">
                    <small>{t('loadingPrices', 'Loading prices...')}</small>
                  </div>
                ) : (
                  watchlist.map((item, index) => (
                    <div key={index} className="watchlist-item">
                      <div className="symbol-info">
                        <span className="symbol">{item.symbol}</span>
                        <span className="market-badge">{item.market}</span>
                      </div>
                      <div className="price-info">
                        <span className="price">{item.price.toFixed(2)}</span>
                        <span className={`change ${item.change_percent >= 0 ? 'positive' : 'negative'}`}>
                          {item.change_percent >= 0 ? '+' : ''}{item.change_percent.toFixed(2)}%
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="no-challenge">
            <div className="card text-center">
              <div className="empty-state">
                <span className="empty-icon">🎯</span>
                <h2>{t('noActiveChallenge', 'No Active Challenge')}</h2>
                <p>{t('startJourney', 'Start your prop trader journey by creating a challenge!')}</p>
                <a href="/challenges" className="btn btn-primary">
                  {t('createChallenge', 'Create Challenge')}
                </a>
              </div>
            </div>
          </div>
        )}

        {/* Recent Challenges - Limited to 3 */}
        {challenges.length > 1 && (
          <div className="card mt-3">
            <div className="card-header">
              <h2 className="card-title">{t('recentChallenges', 'Recent Challenges')}</h2>
              <a href="/challenges" className="view-all-link">{t('viewAll', 'View All')} →</a>
            </div>
            <div className="challenges-list">
              {challenges.slice(0, 3).map(challenge => (
                <div key={challenge.id} className="challenge-item">
                  <div className="challenge-info">
                    <span className="challenge-type">{challenge.plan_type.toUpperCase()}</span>
                    <span className="challenge-date">
                      {new Date(challenge.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="challenge-metrics">
                    <span>{t('balance', 'Balance')}: ${challenge.current_balance.toFixed(2)}</span>
                    <span className={getPnLClass(challenge.current_balance - challenge.initial_balance)}>
                      {t('pnl', 'P&L')}: ${(challenge.current_balance - challenge.initial_balance).toFixed(2)}
                    </span>
                  </div>
                  <span className={`badge badge-${getStatusBadge(challenge.status)}`}>
                    {challenge.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
  );
}

// Helper functions
const getStatusBadge = (status) => {
  const statusMap = {
    'ACTIVE': 'primary',
    'PASSED': 'success',
    'FAILED': 'danger'
  };
  return statusMap[status] || 'warning';
};

const getPnLClass = (value) => {
  if (value > 0) return 'text-success';
  if (value < 0) return 'text-danger';
  return '';
};

export default Dashboard;
