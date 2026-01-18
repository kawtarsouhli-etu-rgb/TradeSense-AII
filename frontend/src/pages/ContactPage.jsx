import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './ContactPage.css';

function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Ici, vous implémenteriez l'appel à votre API de contact
    console.log('Formulaire de contact soumis:', formData);
    setIsSubmitted(true);
    // Réinitialiser le formulaire après 3 secondes
    setTimeout(() => {
      setIsSubmitted(false);
      setFormData({
        name: '',
        email: '',
        subject: '',
        message: ''
      });
    }, 3000);
  };

  return (
    <div className="contact-page">
      <div className="container">
        <div className="contact-header">
          <h1>Contactez TradeSense AI</h1>
          <p>Nous sommes là pour vous aider. Envoyez-nous un message et nous vous répondrons rapidement.</p>
        </div>

        <div className="contact-content">
          <div className="contact-info">
            <h2>Informations de Contact</h2>
            
            <div className="contact-method">
              <h3>📧 Email</h3>
              <p>support@tradesense.ai</p>
              <p>info@tradesense.ai</p>
            </div>

            <div className="contact-method">
              <h3>📞 Téléphone</h3>
              <p>+212 600 000 000</p>
              <p>Lundi-Vendredi: 8h - 20h</p>
            </div>

            <div className="contact-method">
              <h3>📍 Adresse</h3>
              <p>TradeSense AI SARL</p>
              <p>Rue Mohammed V, Casablanca</p>
              <p>Maroc</p>
            </div>

            <div className="contact-method">
              <h3>⏱️ Heures d'Ouverture</h3>
              <p>Lundi - Vendredi: 8h00 - 20h00</p>
              <p>Samedi: 9h00 - 17h00</p>
              <p>Dimanche: Fermé</p>
            </div>
          </div>

          <div className="contact-form">
            <h2>Envoyez-nous un Message</h2>
            
            {isSubmitted && (
              <div className="alert alert-success">
                ✅ Merci pour votre message ! Nous vous répondrons dans les plus brefs délais.
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Nom Complet *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="subject">Sujet *</label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="message">Message *</label>
                <textarea
                  id="message"
                  name="message"
                  rows="6"
                  value={formData.message}
                  onChange={handleChange}
                  required
                ></textarea>
              </div>

              <button type="submit" className="btn btn-primary">
                Envoyer le Message
              </button>
            </form>
          </div>
        </div>

        <div className="contact-support">
          <h2>Support Technique</h2>
          <p>Pour les questions techniques, les problèmes de trading ou les questions relatives aux challenges :</p>
          <Link to="/help" className="btn btn-secondary">Aller au Centre d'Aide</Link>
        </div>
      </div>
    </div>
  );
}

export default ContactPage;