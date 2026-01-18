import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  register: (full_name, email, password) => api.post('/api/auth/register', { full_name, email, password }),
  getMe: () => api.get('/api/auth/me'),
};

// Market Data API
export const marketAPI = {
  getPrice: (symbol, market = 'US') => api.get(`/api/market/price/${symbol}?market=${market}`),
  getWatchlist: () => api.get('/api/market/watchlist'),
  getMoroccoStocks: () => api.get('/api/market/morocco/stocks'),
  search: (query) => api.get(`/api/market/search?q=${query}`),
};

// Trading API
export const tradingAPI = {
  executeTrade: (tradeData) => api.post('/api/trade/execute', tradeData),
  buyTrade: (tradeData) => api.post('/api/trade/buy', tradeData),
  sellTrade: (tradeData) => api.post('/api/trade/sell', tradeData),
  getTrades: (challengeId) => api.get(`/api/trades${challengeId ? `?challenge_id=${challengeId}` : ''}`),
  getMetrics: (challengeId) => api.get(`/api/challenge/${challengeId}/metrics`),
};

// Challenge API
export const challengeAPI = {
  getChallenges: () => api.get('/api/challenges'),
  createChallenge: (planType) => api.post('/api/challenges/create', { plan_type: planType }),
  getChallenge: (id) => api.get(`/api/challenges/${id}`),
};

// Payment API
export const paymentAPI = {
  getPlans: () => api.get('/api/payment/plans'),
  mockPayment: (planId) => api.post('/api/payment/mock', { plan_id: planId }),
  getHistory: () => api.get('/api/payment/history'),
};

// PayPal API
export const paypalAPI = {
  createPayment: (planId) => api.post('/api/paypal/create-payment', { plan_id: planId }),
  executePayment: (paymentId, payerId, planId) => 
    api.post('/api/paypal/execute-payment', { payment_id: paymentId, payer_id: payerId, plan_id: planId }),
};

// Leaderboard API
export const leaderboardAPI = {
  getLeaderboard: () => api.get('/api/leaderboard'),
  getTopPerformer: () => api.get('/api/leaderboard/top-performer'),
};

export default api;
