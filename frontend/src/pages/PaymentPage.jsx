import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { paymentAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';
import './PaymentPage.css';

function PaymentPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [paymentStep, setPaymentStep] = useState(1); // 1: Select plan, 2: Enter details, 3: Confirm, 4: Success

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await paymentAPI.getPlans();
      setPlans(response.data.plans);
      setLoading(false);
    } catch (err) {
      setError('Impossible de charger les plans. Veuillez réessayer.');
      setLoading(false);
    }
  };

  const handlePlanSelect = (plan) => {
    setSelectedPlan(plan);
    setPaymentStep(2);
    setError('');
  };

  const handlePaymentConfirm = async () => {
    try {
      setLoading(true);
      // Simuler le paiement
      await paymentAPI.mockPayment(selectedPlan.id);
      setPaymentStep(4);
      setLoading(false);
    } catch (err) {
      setError('Erreur lors du paiement. Veuillez réessayer.');
      setLoading(false);
    }
  };

  const handleBack = () => {
    if (paymentStep > 1) {
      setPaymentStep(paymentStep - 1);
      setError('');
    }
  };

  if (loading && paymentStep === 1) {
    return (
      <div className="payment-page">
        <div className="payment-container">
          <div className="loading-spinner">Chargement...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="payment-page">
      <div className="payment-container">
        <div className="payment-header">
          <h1>💳 Paiement Sécurisé</h1>
          <p>Finalisez votre achat pour accéder à nos services de trading</p>
        </div>

        {/* Progress Steps */}
        <div className="payment-progress">
          <div className={`progress-step ${paymentStep >= 1 ? 'active' : ''}`}>
            <span>1</span>
            <p>Choix du Plan</p>
          </div>
          <div className={`progress-step ${paymentStep >= 2 ? 'active' : ''}`}>
            <span>2</span>
            <p>Détails</p>
          </div>
          <div className={`progress-step ${paymentStep >= 3 ? 'active' : ''}`}>
            <span>3</span>
            <p>Confirmation</p>
          </div>
          <div className={`progress-step ${paymentStep >= 4 ? 'active' : ''}`}>
            <span>4</span>
            <p>Succès</p>
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Step 1: Plan Selection */}
        {paymentStep === 1 && (
          <div className="payment-step">
            <h2> Sélectionnez votre Plan de Trading</h2>
            <div className="plans-grid">
              {plans.map((plan) => (
                <div 
                  key={plan.id} 
                  className={`plan-card ${selectedPlan?.id === plan.id ? 'selected' : ''}`}
                  onClick={() => handlePlanSelect(plan)}
                >
                  <h3>{plan.name}</h3>
                  <div className="plan-price">{plan.price} DH</div>
                  <div className="plan-capital">Capital: {plan.balance} DH</div>
                  <ul className="plan-features">
                    {plan.features.map((feature, index) => (
                      <li key={index}>✓ {feature}</li>
                    ))}
                  </ul>
                  <button className="select-plan-btn">
                    Choisir ce plan
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Payment Details */}
        {paymentStep === 2 && selectedPlan && (
          <div className="payment-step">
            <h2>Détails de Paiement</h2>
            <div className="selected-plan-summary">
              <h3>Plan Sélectionné: {selectedPlan.name}</h3>
              <p>Prix: {selectedPlan.price} DH</p>
              <p>Capital: {selectedPlan.balance} DH</p>
            </div>
            
            <div className="payment-form">
              <div className="form-group">
                <label htmlFor="cardNumber">Numéro de Carte</label>
                <input 
                  type="text" 
                  id="cardNumber" 
                  placeholder="1234 5678 9012 3456"
                  maxLength="19"
                />
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="expiryDate">Date d'Expiration</label>
                  <input 
                    type="text" 
                    id="expiryDate" 
                    placeholder="MM/AA"
                    maxLength="5"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="cvv">CVV</label>
                  <input 
                    type="text" 
                    id="cvv" 
                    placeholder="123"
                    maxLength="3"
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label htmlFor="cardHolder">Titulaire de la Carte</label>
                <input 
                  type="text" 
                  id="cardHolder" 
                  placeholder={user?.full_name || user?.email || "Nom complet"}
                />
              </div>
            </div>
            
            <div className="payment-actions">
              <button className="btn-back" onClick={handleBack}>
                ← Retour
              </button>
              <button 
                className="btn-next" 
                onClick={() => setPaymentStep(3)}
              >
                Continuer →
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Confirmation */}
        {paymentStep === 3 && selectedPlan && (
          <div className="payment-step">
            <h2>Confirmer le Paiement</h2>
            <div className="confirmation-details">
              <div className="detail-item">
                <span>Plan:</span>
                <span>{selectedPlan.name}</span>
              </div>
              <div className="detail-item">
                <span>Prix:</span>
                <span>{selectedPlan.price} DH</span>
              </div>
              <div className="detail-item">
                <span>Capital:</span>
                <span>{selectedPlan.balance} DH</span>
              </div>
              <div className="detail-item">
                <span>Utilisateur:</span>
                <span>{user?.full_name || user?.email}</span>
              </div>
            </div>
            
            <div className="payment-warning">
              <p>En confirmant, vous acceptez les conditions générales d'utilisation et autorisez le prélèvement de {selectedPlan.price} DH sur votre carte.</p>
            </div>
            
            <div className="payment-actions">
              <button className="btn-back" onClick={handleBack}>
                ← Retour
              </button>
              <button 
                className="btn-confirm" 
                onClick={handlePaymentConfirm}
                disabled={loading}
              >
                {loading ? 'Traitement...' : 'Confirmer le Paiement'}
              </button>
            </div>
          </div>
        )}

        {/* Step 4: Success */}
        {paymentStep === 4 && selectedPlan && (
          <div className="payment-step">
            <div className="success-message">
              <div className="success-icon">✓</div>
              <h2>Paiement Réussi !</h2>
              <p>Votre plan {selectedPlan.name} a été activé avec succès.</p>
              <p>Vous pouvez maintenant accéder à votre challenge de trading.</p>
            </div>
            
            <div className="payment-actions">
              <button 
                className="btn-success" 
                onClick={() => navigate('/challenges')}
              >
                Accéder aux Challenges →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PaymentPage;