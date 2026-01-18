import React from 'react';
import { Link } from 'react-router-dom';
import './HelpPage.css';

function HelpPage() {
  return (
    <div className="help-page">
      <div className="container">
        <div className="help-header">
          <h1>Centre d'Aide TradeSense AI</h1>
          <p>Comment pouvons-nous vous aider aujourd'hui ?</p>
        </div>

        <div className="help-categories">
          <div className="help-category">
            <h2>✨ Démarrage</h2>
            <ul>
              <li><a href="#account-setup">Création de compte</a></li>
              <li><a href="#verification">Vérification de compte</a></li>
              <li><a href="#first-trade">Effectuer votre premier trade</a></li>
              <li><a href="#funding">Financement de votre compte</a></li>
            </ul>
          </div>

          <div className="help-category">
            <h2>💼 Trading</h2>
            <ul>
              <li><a href="#markets">Marchés disponibles</a></li>
              <li><a href="#orders">Types d'ordres</a></li>
              <li><a href="#risk">Gestion des risques</a></li>
              <li><a href="#analysis">Analyse technique</a></li>
            </ul>
          </div>

          <div className="help-category">
            <h2>🎯 Challenges</h2>
            <ul>
              <li><a href="#challenge-rules">Règles des challenges</a></li>
              <li><a href="#profit-target">Objectifs de profit</a></li>
              <li><a href="#drawdown">Limites de drawdown</a></li>
              <li><a href="#funding">Comment obtenir un financement</a></li>
            </ul>
          </div>

          <div className="help-category">
            <h2>🔒 Sécurité</h2>
            <ul>
              <li><a href="#security">Mesures de sécurité</a></li>
              <li><a href="#2fa">Authentification à deux facteurs</a></li>
              <li><a href="#password">Changement de mot de passe</a></li>
              <li><a href="#report">Signaler un problème</a></li>
            </ul>
          </div>
        </div>

        <div className="help-faq">
          <h2>Foire aux Questions</h2>
          
          <div className="faq-item">
            <h3>Comment créer un compte TradeSense ?</h3>
            <p>Cliquez sur "S'inscrire" en haut à droite de la page d'accueil et suivez les étapes pour créer votre compte. Vous aurez besoin d'une adresse e-mail valide et d'un mot de passe sécurisé.</p>
          </div>

          <div className="faq-item">
            <h3>Quels sont les frais de plateforme ?</h3>
            <p>TradeSense AI ne facture aucun frais de plateforme. Nous gagnons uniquement lorsque vous réussissez vos challenges de trading.</p>
          </div>

          <div className="faq-item">
            <h3>Comment fonctionne le processus de financement ?</h3>
            <p>Après avoir réussi un challenge de trading, vous pouvez accéder à des comptes financés avec jusqu'à 80% de profits conservés par vous.</p>
          </div>

          <div className="faq-item">
            <h3>Quels marchés puis-je trader ?</h3>
            <p>Nous offrons l'accès aux marchés US (actions, ETFs), cryptomonnaies, Forex, commodités et la bourse marocaine IAM.</p>
          </div>

          <div className="faq-item">
            <h3>Comment contacter le support ?</h3>
            <p>Vous pouvez nous contacter via le formulaire de contact, par e-mail à support@tradesense.ai ou via le chat en direct.</p>
          </div>
        </div>

        <div className="help-contact">
          <h2>Besoin d'aide immédiate ?</h2>
          <p>Contactez notre équipe de support pour une assistance personnalisée.</p>
          <Link to="/contact" className="btn btn-primary">Contacter le Support</Link>
        </div>
      </div>
    </div>
  );
}

export default HelpPage;