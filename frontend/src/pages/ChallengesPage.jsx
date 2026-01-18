import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { challengeAPI, paymentAPI } from '../services/api';
import './ChallengesPage.css';

function ChallengesPage() {
  const [challenges, setChallenges] = useState([]);
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [paymentModal, setPaymentModal] = useState({ show: false, plan: null });
  const [paymentLoading, setPaymentLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [challengesRes, plansRes] = await Promise.all([
        challengeAPI.getChallenges(),
        paymentAPI.getPlans()
      ]);
      setChallenges(challengesRes.data.challenges);
      setPlans(plansRes.data.plans);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const openPaymentModal = (plan) => {
    setPaymentModal({ show: true, plan });
    setMessage(null);
  };

  const closePaymentModal = () => {
    setPaymentModal({ show: false, plan: null });
    setPaymentLoading(false);
  };

  const handlePayment = async (paymentMethod) => {
    setPaymentLoading(true);
    setMessage(null);
    
    // Simulate payment processing (2-3 seconds)
    setTimeout(async () => {
      try {
        const res = await paymentAPI.mockPayment(paymentModal.plan.id);
        if (res.data) {
          setPaymentLoading(false);
          closePaymentModal();
          setMessage({ 
            type: 'success', 
            text: `✅ Paiement ${paymentMethod} réussi ! Challenge créé avec succès.` 
          });
          
          // Reload challenges
          setTimeout(async () => {
            await loadData();
          }, 1000);
        }
      } catch (error) {
        setPaymentLoading(false);
        setMessage({ 
          type: 'error', 
          text: error.response?.data?.error || 'Erreur lors du paiement' 
        });
      }
    }, 2500); // 2.5 seconds delay
  };

  return (
    <Layout>
      <div className="challenges-page">
        <h1>🎯 Mes Challenges</h1>

        {message && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
          </div>
        )}

        {challenges.length > 0 && (
          <div className="section">
            <h2>Challenges Actifs & Historique</h2>
            <div className="challenges-grid">
              {challenges.map(challenge => (
                <div key={challenge.id} className="card challenge-card">
                  <div className="card-header">
                    <h3>{challenge.plan_type.toUpperCase()}</h3>
                    <span className={`badge badge-${getStatusBadge(challenge.status)}`}>
                      {challenge.status}
                    </span>
                  </div>
                  <div className="challenge-stats">
                    <div className="stat">
                      <span>Balance</span>
                      <strong>{challenge.current_balance.toFixed(2)} DH</strong>
                    </div>
                    <div className="stat">
                      <span>P&L</span>
                      <strong className={getPnLClass(challenge.current_balance - challenge.initial_balance)}>
                        {(challenge.current_balance - challenge.initial_balance).toFixed(2)} DH
                      </strong>
                    </div>
                  </div>
                  <div className="challenge-footer">
                    <small>{new Date(challenge.created_at).toLocaleDateString('fr-FR')}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="section">
          <h2>Acheter un Nouveau Challenge</h2>
          <div className="plans-grid">
            {plans.map(plan => (
              <div key={plan.id} className={`card plan-card ${plan.id === 'pro' ? 'featured' : ''}`}>
                {plan.id === 'pro' && <div className="popular-badge">POPULAIRE</div>}
                <h3>{plan.name}</h3>
                <div className="plan-price">{plan.price} {plan.currency}</div>
                <p className="plan-description">{plan.description}</p>
                <ul className="plan-features">
                  {plan.features.map((feature, idx) => (
                    <li key={idx}>{feature}</li>
                  ))}
                </ul>
                <button 
                  className="btn btn-primary btn-block"
                  onClick={() => openPaymentModal(plan)}
                  disabled={loading}
                >
                  Acheter Maintenant
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Payment Modal */}
      {paymentModal.show && (
        <div className="modal-overlay" onClick={closePaymentModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Choisir un Mode de Paiement</h2>
              <button className="modal-close" onClick={closePaymentModal}>×</button>
            </div>
            
            <div className="modal-body">
              <div className="payment-plan-info">
                <h3>{paymentModal.plan?.name?.toUpperCase()}</h3>
                <div className="payment-amount">{paymentModal.plan?.price} {paymentModal.plan?.currency}</div>
                <p>{paymentModal.plan?.description}</p>
              </div>

              {paymentLoading ? (
                <div className="payment-loading">
                  <div className="spinner"></div>
                  <p>Traitement du paiement en cours...</p>
                  <small>Veuillez patienter quelques instants</small>
                </div>
              ) : (
                <div className="payment-methods">
                  <button 
                    className="payment-btn payment-cmi"
                    onClick={() => handlePayment('CMI')}
                  >
                    <span className="payment-icon">💳</span>
                    <div className="payment-info">
                      <strong>Payer avec CMI</strong>
                      <small>Carte bancaire marocaine</small>
                    </div>
                  </button>

                  <button 
                    className="payment-btn payment-crypto"
                    onClick={() => handlePayment('Crypto')}
                  >
                    <span className="payment-icon">₿</span>
                    <div className="payment-info">
                      <strong>Payer avec Crypto</strong>
                      <small>Bitcoin, USDT, ETH</small>
                    </div>
                  </button>
                </div>
              )}

              <div className="payment-note">
                <small>🔒 Paiement sécurisé - Mode simulation (aucun frais réel)</small>
              </div>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}

const getStatusBadge = (status) => {
  return { 'ACTIVE': 'primary', 'PASSED': 'success', 'FAILED': 'danger' }[status] || 'warning';
};

const getPnLClass = (value) => value > 0 ? 'text-success' : value < 0 ? 'text-danger' : '';

export default ChallengesPage;
