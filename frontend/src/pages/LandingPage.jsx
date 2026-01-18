import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Bot, Newspaper, Users, GraduationCap, 
  CreditCard, Target, Trophy, 
  Check, Users as UsersIcon, DollarSign, TrendingUp, Globe,
  ChevronDown, Star, Mail, Phone, MapPin,
  Facebook, Twitter, Instagram
} from 'lucide-react';
import './LandingPage.css';

function LandingPage() {
  const [activeFAQ, setActiveFAQ] = useState(null);
  const [stats, setStats] = useState({
    traders: 0,
    distributed: 0,
    successRate: 0,
    countries: 0
  });

  // Animate stats on scroll
  useEffect(() => {
    const timer = setTimeout(() => {
      setStats({
        traders: 1247,
        distributed: 2400000,
        successRate: 68,
        countries: 15
      });
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  const faqs = [
    {
      question: "Je n'ai jamais tradé, puis-je réussir ?",
      answer: "Absolument ! Notre Centre MasterClass commence par les bases. Avec nos cours et l'IA, vous apprendrez progressivement. 40% de nos traders financés étaient débutants."
    },
    {
      question: "C'est quoi un challenge de trading ?",
      answer: "Phase d'évaluation avec argent virtuel. Objectif : +10% sans dépasser limites de perte. Une fois réussi, vous tradez avec notre capital réel !"
    },
    {
      question: "Quels marchés puis-je trader ?",
      answer: "Actions US (Apple, Tesla...), Cryptos (Bitcoin, Ethereum...), Bourse Marocaine (IAM, Attijariwafa...). Tout en temps réel !"
    }
  ];

  const testimonials = [
    {
      name: "Ahmed K.",
      location: "Casablanca",
      text: "Grâce à TradeSense, je suis passé de débutant à trader financé en 2 mois. Les cours sont clairs et l'IA m'aide énormément.",
      rating: 5
    },
    {
      name: "Fatima M.",
      location: "Rabat",
      text: "La communauté est incroyable. J'apprends chaque jour. Le support est très réactif.",
      rating: 5
    },
    {
      name: "Youssef B.",
      location: "Marrakech",
      text: "Meilleure décision de ma vie. Je trade maintenant à temps plein avec leur capital.",
      rating: 5
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <motion.div 
          className="hero-content"
          initial="hidden"
          animate="visible"
          variants={containerVariants}
        >
          <motion.h1 variants={itemVariants} className="hero-title">
            TradeSense AI
          </motion.h1>
          <motion.h2 variants={itemVariants} className="hero-subtitle">
            La Première Prop Firm Assistée par IA pour l'Afrique
          </motion.h2>
          <motion.p variants={itemVariants} className="hero-description">
            Une plateforme de trading de nouvelle génération qui combine l'intelligence artificielle, 
            l'analyse en temps réel et l'éducation pour transformer les traders débutants en professionnels financés
          </motion.p>
          <motion.div variants={itemVariants} className="hero-buttons">
            <Link to="/login" className="btn btn-primary">
              Commencer Maintenant
            </Link>
            <button 
              onClick={() => document.getElementById('how-it-works').scrollIntoView({behavior: 'smooth'})}
              className="btn btn-secondary"
            >
              Voir la Démo
            </button>
          </motion.div>
        </motion.div>
        <div className="hero-animation">
          <div className="floating-elements">
            <div className="element element-1">📈</div>
            <div className="element element-2">🤖</div>
            <div className="element element-3">📊</div>
            <div className="element element-4">💰</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Fonctionnalités Révolutionnaires
          </motion.h2>
          
          <div className="features-grid">
            {[
              {
                icon: <Bot size={40} />,
                title: "Assistance Trading IA",
                text: "Signaux Achat/Vente en temps réel • Plans de trade personnalisés • Alertes de risque automatiques • Tri intelligent des opportunités"
              },
              {
                icon: <Newspaper size={40} />,
                title: "Hub d'Actualités en Direct",
                text: "Actualités financières instantanées • Résumés générés par IA • Alertes événements économiques • Analyses d'impact sur positions"
              },
              {
                icon: <Users size={40} />,
                title: "Zone Communautaire",
                text: "Discussions avec traders • Partage de stratégies • Groupes thématiques • Apprentissage des experts • Réseau professionnel"
              },
              {
                icon: <GraduationCap size={40} />,
                title: "Centre MasterClass",
                text: "Cours débutant à avancé • Analyse technique et fondamentale • Gestion des risques • Webinaires experts • Quiz interactifs"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                className="feature-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.text}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="how-it-works-section">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Votre Parcours vers le Financement
          </motion.h2>
          
          <div className="steps-container">
            {[
              {
                icon: <CreditCard size={32} />,
                title: "Choisir Votre Plan",
                text: "Starter (200 DH - 5,000 DH capital) • Pro (500 DH - 10,000 DH) • Elite (1,000 DH - 25,000 DH)"
              },
              {
                icon: <Target size={32} />,
                title: "Passer le Challenge",
                text: "Objectif : +10% profit • Perte max journalière : -5% • Perte max totale : -10% • Assistance IA temps réel"
              },
              {
                icon: <Trophy size={32} />,
                title: "Être Financé",
                text: "Devenez trader financé • Tradez avec notre capital • Gardez 80% des profits • Aucune limite de gains"
              }
            ].map((step, index) => (
              <motion.div
                key={index}
                className="step-card"
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
              >
                <div className="step-number">{index + 1}</div>
                <div className="step-icon">{step.icon}</div>
                <h3>{step.title}</h3>
                <p>{step.text}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Why TradeSense Section */}
      <section className="why-tradesense-section">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Ce qui nous rend différents
          </motion.h2>
          
          <div className="benefits-grid">
            {[
              "Plateforme unique : Trading + Apprentissage + Communauté",
              "Signaux IA et alertes en temps réel",
              "Marchés multiples : US, Crypto, Maroc",
              "Formation MasterClass incluse",
              "Pour débutants et expérimentés",
              "Support 24/7 et communauté active"
            ].map((benefit, index) => (
              <motion.div
                key={index}
                className="benefit-item"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Check size={20} className="benefit-icon" />
                <span>{benefit}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            {[
              { icon: <UsersIcon size={32} />, value: stats.traders, label: "Traders Actifs", suffix: "+" },
              { icon: <DollarSign size={32} />, value: stats.distributed, label: "DH Distribués", suffix: "M+" },
              { icon: <TrendingUp size={32} />, value: stats.successRate, label: "Taux de Réussite", suffix: "%" },
              { icon: <Globe size={32} />, value: stats.countries, label: "Pays", suffix: "+" }
            ].map((stat, index) => (
              <motion.div
                key={index}
                className="stat-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="stat-icon">{stat.icon}</div>
                <div className="stat-value">
                  {stat.value.toLocaleString()}{stat.suffix}
                </div>
                <div className="stat-label">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Preview Section */}
      <section className="pricing-preview-section">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Plans Tarifaires
          </motion.h2>
          
          <div className="pricing-grid">
            {[
              {
                name: "Starter",
                price: "200 DH",
                capital: "5,000 DH",
                features: ["Support de base", "Accès communauté"]
              },
              {
                name: "Pro",
                price: "500 DH",
                capital: "10,000 DH",
                features: ["Support prioritaire", "Analyses IA avancées", "Webinaires exclusifs"],
                popular: true
              },
              {
                name: "Elite",
                price: "1,000 DH",
                capital: "25,000 DH",
                features: ["Support VIP 24/7", "Coach personnel", "Accès anticipé"]
              }
            ].map((plan, index) => (
              <motion.div
                key={index}
                className={`pricing-card ${plan.popular ? 'popular' : ''}`}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
              >
                {plan.popular && <div className="popular-badge">Populaire</div>}
                <h3>{plan.name}</h3>
                <div className="price">{plan.price}</div>
                <div className="capital">Capital: {plan.capital}</div>
                <ul className="features-list">
                  {plan.features.map((feature, idx) => (
                    <li key={idx}>
                      <Check size={16} />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link to="/pricing" className="btn btn-outline">
                  Choisir ce plan
                </Link>
              </motion.div>
            ))}
          </div>
          
          <motion.div 
            className="pricing-cta"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            <Link to="/pricing" className="btn btn-primary">
              Voir Tous les Plans
            </Link>
          </motion.div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="faq-section">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Questions Fréquentes
          </motion.h2>
          
          <div className="faq-container">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                className="faq-item"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <button 
                  className="faq-question"
                  onClick={() => setActiveFAQ(activeFAQ === index ? null : index)}
                >
                  <span>{faq.question}</span>
                  <ChevronDown 
                    size={20} 
                    className={`faq-chevron ${activeFAQ === index ? 'rotated' : ''}`} 
                  />
                </button>
                {activeFAQ === index && (
                  <motion.div 
                    className="faq-answer"
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                  >
                    <p>{faq.answer}</p>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <motion.h2 
            className="section-title"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            Ce que disent nos traders
          </motion.h2>
          
          <div className="testimonials-grid">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                className="testimonial-card"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
              >
                <div className="testimonial-rating">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} size={16} fill="#FBBF24" stroke="#FBBF24" />
                  ))}
                </div>
                <p className="testimonial-text">"{testimonial.text}"</p>
                <div className="testimonial-author">
                  <span className="author-name">{testimonial.name}</span>
                  <span className="author-location">{testimonial.location}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="final-cta-section">
        <motion.div 
          className="cta-container"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
        >
          <h2>🚀 Prêt à Devenir Trader Professionnel ?</h2>
          <p>
            Rejoignez des centaines de traders qui ont transformé leur passion en carrière rentable
          </p>
          <Link to="/pricing" className="btn btn-large">
            COMMENCER MAINTENANT
          </Link>
          <p className="cta-subtext">
            Aucune expérience requise • Formation incluse • Support 24/7
          </p>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-grid">
            <div className="footer-column">
              <h3>TRADESENSE</h3>
              <ul>
                <li><a href="#about">À propos</a></li>
                <li><a href="#mission">Notre Mission</a></li>
                <li><a href="#team">Équipe</a></li>
                <li><a href="#contact">Contact</a></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h3>RESSOURCES</h3>
              <ul>
                <li><a href="#masterclass">Centre MasterClass</a></li>
                <li><a href="#blog">Blog</a></li>
                <li><a href="#guides">Guides de Trading</a></li>
                <li><a href="#faq">FAQ</a></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h3>LÉGAL</h3>
              <ul>
                <li><a href="#terms">Conditions d'Utilisation</a></li>
                <li><a href="#privacy">Politique de Confidentialité</a></li>
                <li><a href="#legal">Mentions Légales</a></li>
              </ul>
            </div>
            
            <div className="footer-column">
              <h3>CONTACT</h3>
              <ul className="contact-info">
                <li>
                  <Mail size={16} />
                  <span>contact@tradesense.com</span>
                </li>
                <li>
                  <Phone size={16} />
                  <span>+212 600 000 000</span>
                </li>
                <li>
                  <MapPin size={16} />
                  <span>Casablanca, Maroc</span>
                </li>
              </ul>
              <div className="social-links">
                <a href="#"><Facebook size={20} /></a>
                <a href="#"><Twitter size={20} /></a>
                <a href="#"><Instagram size={20} /></a>
              </div>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>&copy; 2024 TradeSense AI. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;