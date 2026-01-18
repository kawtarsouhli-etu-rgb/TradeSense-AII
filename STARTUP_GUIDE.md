# 🚀 TradeSense AI - Guide de Démarrage Rapide

## 📋 Vue d'ensemble
TradeSense AI est une plateforme de **Prop Trading Firm** complète avec challenge engine, paiement simulé, dashboard temps réel et classement.

## 🛠️ Stack Technologique
- **Backend**: Flask 3.0, SQLAlchemy 3.1.1, PyJWT 2.8.0
- **Frontend**: React 18, Vite, Axios
- **Data**: yfinance 0.2.32 (prix temps réel)
- **Database**: SQLite (développement)

---

## ⚡ Démarrage Backend (Flask)

### 1. Installation des dépendances
```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialisation de la base de données
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

**OU** Importer la base de données existante:
```bash
# Si vous avez database.sql
sqlite3 backend/database.db < backend/database.sql
```

### 3. Lancer le serveur Flask
```bash
cd backend
python app.py
```

✅ **Serveur backend accessible sur**: `http://localhost:5000`

---

## ⚛️ Démarrage Frontend (React)

### 1. Installation des dépendances
```bash
cd frontend
npm install
```

### 2. Lancer le serveur de développement
```bash
npm run dev
```

✅ **Application React accessible sur**: `http://localhost:3000`

---

## 🎯 Utilisation de la Plateforme

### Étape 1 : Inscription
1. Accédez à `http://localhost:3000/register`
2. Créez votre compte utilisateur

### Étape 2 : Connexion
1. Connectez-vous avec vos identifiants
2. Vous êtes redirigé vers le Dashboard

### Étape 3 : Acheter un Challenge
1. Allez dans **Challenges**
2. Choisissez un plan (Starter 200 DH, Pro 500 DH, Elite 1000 DH)
3. Cliquez sur **Acheter** (paiement simulé)

### Étape 4 : Commencer à Trader
1. Allez dans **Trading**
2. Sélectionnez un symbole (AAPL, TSLA, BTC-USD, IAM, ATW...)
3. Entrez un montant
4. Cliquez sur **SELL** (profit) ou **BUY** (dépense)
5. Le challenge est automatiquement évalué après chaque trade

### Étape 5 : Suivre vos Performances
- **Dashboard**: Vue d'ensemble avec métriques en temps réel
- **Challenges**: Historique et statut de vos challenges
- **Classement**: Comparez-vous aux autres traders

---

## 📊 Règles du Challenge Engine

Chaque challenge a des règles strictes :
- **Balance initiale**: 5000 DH (Pro), 1000 DH (Starter), 10000 DH (Elite)
- **Objectif de profit**: +10%
- **Perte journalière max**: -5%
- **Perte totale max**: -10%

### Statuts possibles :
- **ACTIVE**: Challenge en cours
- **PASSED**: Objectif de +10% atteint ✅
- **FAILED**: Limite de perte dépassée ❌

---

## 🔑 Comptes de Test

Vous pouvez créer votre propre compte OU utiliser le compte SuperAdmin :

**SuperAdmin** (accès backend uniquement via API)
- Email: `admin@tradesense.ai`
- Password: `admin123`

---

## 🌐 Endpoints API Principaux

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/me` - Profil utilisateur

### Trading
- `POST /api/trade/execute` - Exécuter un trade
- `GET /api/challenge/{id}/metrics` - Métriques du challenge
- `GET /api/trades` - Historique des trades

### Market Data
- `GET /api/market/price/{symbol}?market=US` - Prix temps réel
- `GET /api/market/watchlist` - Liste de surveillance

### Challenges
- `GET /api/challenges` - Mes challenges
- `POST /api/challenges/create` - Créer un challenge

### Payment
- `GET /api/payment/plans` - Plans disponibles
- `POST /api/payment/mock` - Paiement simulé

### Leaderboard
- `GET /api/leaderboard` - Classement des traders

---

## 🧪 Tester l'API avec curl

```bash
# 1. S'inscrire
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","email":"john@test.com","password":"test123"}'

# 2. Se connecter
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@test.com","password":"test123"}'

# 3. Obtenir un prix (avec token)
curl -X GET "http://localhost:5000/api/market/price/AAPL?market=US" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📁 Structure du Projet

```
TradeSense/
├── backend/
│   ├── app.py                    # Application Flask principale
│   ├── config.py                 # Configuration
│   ├── models.py                 # Modèles SQLAlchemy
│   ├── challenge_engine.py       # Moteur d'évaluation
│   ├── requirements.txt          # Dépendances Python
│   ├── database.sql             # Export de la base de données
│   ├── services/
│   │   ├── auth_service.py      # Service d'authentification
│   │   ├── real_time_data.py    # Service données temps réel
│   │   └── ...
│   └── routes/
│       ├── auth.py              # Routes authentification
│       ├── trading.py           # Routes trading
│       ├── market.py            # Routes market data
│       ├── challenges.py        # Routes challenges
│       ├── payment.py           # Routes paiement
│       ├── leaderboard.py       # Routes classement
│       └── admin.py             # Routes admin
│
└── frontend/
    ├── src/
    │   ├── App.jsx              # Composant principal
    │   ├── main.jsx             # Point d'entrée
    │   ├── context/
    │   │   └── AuthContext.jsx  # Context d'authentification
    │   ├── services/
    │   │   └── api.js           # Services API
    │   ├── components/
    │   │   └── Layout.jsx       # Layout principal
    │   └── pages/
    │       ├── LoginPage.jsx    # Page connexion
    │       ├── Dashboard.jsx    # Dashboard principal
    │       ├── TradingPage.jsx  # Page trading
    │       ├── ChallengesPage.jsx
    │       └── LeaderboardPage.jsx
    ├── package.json
    └── vite.config.js
```

---

## 🚨 Troubleshooting

### Backend ne démarre pas
```bash
# Vérifier que Flask est installé
pip list | grep Flask

# Vérifier le port 5000
netstat -ano | findstr :5000

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Frontend ne démarre pas
```bash
# Supprimer node_modules et réinstaller
rm -rf node_modules package-lock.json
npm install

# Vérifier la version de Node (minimum v16)
node --version
```

### Erreurs CORS
Le backend est configuré avec CORS activé. Si problème :
- Vérifiez que Flask-CORS est installé
- Le proxy Vite est configuré dans `vite.config.js`

---

## 🎬 Prochaines Étapes

1. ✅ **Tester le système complet**
2. ✅ **Créer un compte et trader**
3. 📹 **Enregistrer une vidéo de démonstration**
4. 🚀 **Déployer sur un serveur**
5. 📦 **Créer le repo GitHub**

---

## 📞 Support

Pour toute question, contactez l'équipe TradeSense AI.

**Bon trading ! 💹🚀**
