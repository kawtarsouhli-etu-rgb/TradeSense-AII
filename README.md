# TradeSense AI - Prop Trading Platform

TradeSense AI est une plateforme de trading avancée qui combine intelligence artificielle, analyse en temps réel et éducation pour transformer les traders débutants en professionnels financés.

## Fonctionnalités

- 🎯 **Challenges de Trading** - Évaluez vos compétences avec des objectifs de profit et des limites de perte
- 📈 **Trading en Temps Réel** - Interface de trading avancée avec données de marché en temps réel
- 🤖 **Assistant IA** - Signaux d'achat/vente et alertes de risque automatisées
- 🏆 **Classement** - Compétition entre traders avec classement en temps réel
- 💰 **Financement Réel** - Devenez trader financé après avoir réussi les challenges
- 📚 **Centre MasterClass** - Cours d'éducation complète sur le trading
- 🌐 **Actualités en Direct** - Hub d'informations financières instantanées
- 👥 **Zone Communautaire** - Discussions avec traders et partage de stratégies

## Technologies Utilisées

- **Backend**: Flask, SQLAlchemy, MySQL
- **Frontend**: React, Vite, Tailwind CSS
- **API**: Yahoo Finance, TradingView Lightweight Charts, BeautifulSoup (pour les données marocaines)
- **Authentification**: JWT Tokens
- **Paiement**: PayPal Sandbox Integration
- **Internationalisation**: i18next pour le support multilingue (français/arabe/anglais)

## Installation

1. Clonez le dépôt:
```bash
git clone https://github.com/kawtarsouhli-etu-rgb/tradesense-ai.git
```

2. Installez les dépendances backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Installez les dépendances frontend:
```bash
cd frontend
npm install
```

4. Configurez la base de données et les variables d'environnement

5. Lancez l'application:
```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm run dev
```

## Structure du Projet

```
TradeSense/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── services/
│   ├── routes/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   └── package.json
├── database/
│   └── schema.sql
└── README.md
```

## Variables d'Environnement

Configurez les variables suivantes dans un fichier `.env`:
- `DATABASE_URL` - URL de la base de données MySQL
- `SECRET_KEY` - Clé secrète pour les JWT
- `PAYPAL_CLIENT_ID` - Identifiant client PayPal
- `PAYPAL_SECRET` - Secret PayPal

## Base de Données

Le fichier `database/schema.sql` contient le schéma complet de la base de données avec :
- Tables pour les utilisateurs, challenges, trades, paiements
- Données initiales pour l'administrateur
- Exemples de données de marché

## License

Ce projet est la propriété de Kawtar Souhli.