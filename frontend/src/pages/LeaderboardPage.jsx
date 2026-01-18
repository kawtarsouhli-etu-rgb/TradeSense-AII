import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { leaderboardAPI } from '../services/api';
import './LeaderboardPage.css';

function LeaderboardPage() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
    const interval = setInterval(loadLeaderboard, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadLeaderboard = async () => {
    try {
      const res = await leaderboardAPI.getLeaderboard();
      setLeaderboard(res.data.leaderboard);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loader">Chargement...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="leaderboard-page">
        <div className="leaderboard-header">
          <h1>🏆 Classement des Traders</h1>
          <p>Top traders classés par % de profit</p>
        </div>

        {leaderboard.length === 0 ? (
          <div className="card text-center">
            <p>Aucun trader dans le classement pour le moment</p>
          </div>
        ) : (
          <div className="leaderboard-table card">
            <table>
              <thead>
                <tr>
                  <th>Rang</th>
                  <th>Trader</th>
                  <th>Challenge</th>
                  <th>Balance</th>
                  <th>P&L</th>
                  <th>% Profit</th>
                  <th>Trades</th>
                  <th>Taux de Réussite</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((entry) => (
                  <tr key={entry.rank} className={entry.rank <= 3 ? `top-${entry.rank}` : ''}>
                    <td>
                      <div className="rank">
                        {entry.rank === 1 && '🥇'}
                        {entry.rank === 2 && '🥈'}
                        {entry.rank === 3 && '🥉'}
                        {entry.rank > 3 && `#${entry.rank}`}
                      </div>
                    </td>
                    <td>
                      <div className="trader-info">
                        <strong>{entry.user.full_name}</strong>
                        <small>{entry.user.email}</small>
                      </div>
                    </td>
                    <td>
                      <span className="badge badge-primary">{entry.challenge.plan_type}</span>
                    </td>
                    <td>{entry.challenge.current_balance.toFixed(2)} DH</td>
                    <td className={entry.performance.profit_loss >= 0 ? 'text-success' : 'text-danger'}>
                      {entry.performance.profit_loss >= 0 ? '+' : ''}{entry.performance.profit_loss.toFixed(2)} DH
                    </td>
                    <td className={entry.performance.profit_percentage >= 0 ? 'text-success' : 'text-danger'}>
                      <strong>{entry.performance.profit_percentage.toFixed(2)}%</strong>
                    </td>
                    <td>{entry.performance.total_trades}</td>
                    <td>{entry.performance.win_rate.toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
}

export default LeaderboardPage;
