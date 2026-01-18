import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { marketAPI, tradingAPI, challengeAPI } from '../services/api';
import RealTimePriceComponent from '../components/RealTimePriceComponent';
import './TradingPage.css';

function TradingPage() {
  const { t } = useTranslation();
  const [selectedSymbol, setSelectedSymbol] = useState({ 
    symbol: 'AAPL', 
    market: 'US', 
    name: 'Apple Inc.' 
  });
  const [currentPrice, setCurrentPrice] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [trades, setTrades] = useState([]);

  const symbols = [
    // US Stocks
    { symbol: 'AAPL', market: 'US', name: 'Apple Inc.', sector: 'Technology', country: 'USA', currency: 'USD' },
    { symbol: 'TSLA', market: 'US', name: 'Tesla Inc.', sector: 'Automotive', country: 'USA', currency: 'USD' },
    { symbol: 'GOOGL', market: 'US', name: 'Alphabet Inc.', sector: 'Technology', country: 'USA', currency: 'USD' },
    { symbol: 'MSFT', market: 'US', name: 'Microsoft Corp.', sector: 'Technology', country: 'USA', currency: 'USD' },
    { symbol: 'AMZN', market: 'US', name: 'Amazon.com Inc.', sector: 'Retail', country: 'USA', currency: 'USD' },
    { symbol: 'META', market: 'US', name: 'Meta Platforms Inc.', sector: 'Technology', country: 'USA', currency: 'USD' },
    { symbol: 'NVDA', market: 'US', name: 'NVIDIA Corp.', sector: 'Semiconductors', country: 'USA', currency: 'USD' },
    
    // Crypto
    { symbol: 'BTC-USD', market: 'CRYPTO', name: 'Bitcoin', sector: 'Cryptocurrency', country: 'Global', currency: 'USD' },
    { symbol: 'ETH-USD', market: 'CRYPTO', name: 'Ethereum', sector: 'Cryptocurrency', country: 'Global', currency: 'USD' },
    { symbol: 'ADA-USD', market: 'CRYPTO', name: 'Cardano', sector: 'Cryptocurrency', country: 'Global', currency: 'USD' },
    { symbol: 'BNB-USD', market: 'CRYPTO', name: 'Binance Coin', sector: 'Cryptocurrency', country: 'Global', currency: 'USD' },
    
    // Morocco Stocks
    { symbol: 'IAM', market: 'MOROCCO', name: 'Maroc Telecom', sector: 'Telecommunications', country: 'Morocco', currency: 'MAD' },
    { symbol: 'ATW', market: 'MOROCCO', name: 'Attijariwafa Bank', sector: 'Banking', country: 'Morocco', currency: 'MAD' },
    { symbol: 'MAN', market: 'MOROCCO', name: 'MANAGEM', sector: 'Industrial', country: 'Morocco', currency: 'MAD' },
    { symbol: 'CGM', market: 'MOROCCO', name: 'Ciments du Maroc', sector: 'Materials', country: 'Morocco', currency: 'MAD' },
    { symbol: 'MSE', market: 'MOROCCO', name: 'Medi1 Sat', sector: 'Media', country: 'Morocco', currency: 'MAD' },
    
    // European Stocks
    { symbol: 'SAN', market: 'EUR', name: 'Sanofi SA', sector: 'Healthcare', country: 'France', currency: 'EUR' },
    { symbol: 'AIR', market: 'EUR', name: 'Airbus SE', sector: 'Aerospace', country: 'Netherlands', currency: 'EUR' },
    { symbol: 'MC', market: 'EUR', name: 'LVMH Moet Hennessy', sector: 'Luxury', country: 'France', currency: 'EUR' },
    
    // Forex pairs
    { symbol: 'EUR-USD', market: 'FX', name: 'Euro to US Dollar', sector: 'Forex', country: 'Europe/USA', currency: 'USD' },
    { symbol: 'GBP-USD', market: 'FX', name: 'British Pound to US Dollar', sector: 'Forex', country: 'UK/USA', currency: 'USD' },
    { symbol: 'USD-JPY', market: 'FX', name: 'US Dollar to Japanese Yen', sector: 'Forex', country: 'USA/Japan', currency: 'JPY' },
    { symbol: 'EUR-MAD', market: 'FX', name: 'Euro to Moroccan Dirham', sector: 'Forex', country: 'Europe/Morocco', currency: 'MAD' },
    
    // Commodities
    { symbol: 'CL', market: 'COMMODITY', name: 'Crude Oil', sector: 'Energy', country: 'Global', currency: 'USD' },
    { symbol: 'GC', market: 'COMMODITY', name: 'Gold', sector: 'Metals', country: 'Global', currency: 'USD' },
    { symbol: 'XAU', market: 'COMMODITY', name: 'Gold (in EUR)', sector: 'Metals', country: 'Global', currency: 'EUR' },
    
    // Asian Markets
    { symbol: '7203', market: 'TOKYO', name: 'Toyota Motor Corp', sector: 'Automotive', country: 'Japan', currency: 'JPY' },
    { symbol: '2888', market: 'HK', name: 'Bank of China HK', sector: 'Banking', country: 'Hong Kong', currency: 'HKD' },
    
    // Emerging markets
    { symbol: 'PETR4', market: 'SAO_PAULO', name: 'Petrobras PN', sector: 'Energy', country: 'Brazil', currency: 'BRL' },
    { symbol: 'TCS', market: 'BOMBAY', name: 'Tata Consultancy Services', sector: 'IT Services', country: 'India', currency: 'INR' }
  ];

  // Load challenges on component mount - optimized
  useEffect(() => {
    let isMounted = true;
    
    const loadInitialData = async () => {
      try {
        // Load challenges first
        const res = await challengeAPI.getChallenges();
        if (!isMounted) return;
        
        const allChallenges = res.data.challenges;
        const activeChallenges = allChallenges.filter(c => c.status === 'ACTIVE');
        const otherChallenges = allChallenges.filter(c => c.status !== 'ACTIVE');
        const sortedChallenges = [...activeChallenges, ...otherChallenges];
        
        setChallenges(sortedChallenges);
        
        // Auto-select first active challenge
        let challengeId = null;
        if (activeChallenges.length > 0) {
          challengeId = activeChallenges[0].id;
        } else if (sortedChallenges.length > 0) {
          challengeId = sortedChallenges[0].id;
        }
        
        if (challengeId) {
          setSelectedChallenge(challengeId);
          // Load trades for selected challenge
          try {
            const tradesRes = await tradingAPI.getTrades(challengeId);
            if (isMounted) {
              setTrades(tradesRes.data.trades || []);
            }
          } catch (error) {
            console.warn('Could not load trades initially:', error);
          }
        }
      } catch (error) {
        console.error('Error loading initial data:', error);
        if (isMounted) {
          setMessage({ 
            type: 'error', 
            text: t('errorLoadingData', 'Error loading data') 
          });
        }
      }
    };
    
    loadInitialData();
    
    return () => {
      isMounted = false;
    };
  }, []);

  const loadChallenges = async () => {
    try {
      const res = await challengeAPI.getChallenges();
      const allChallenges = res.data.challenges;
      
      // Filter and sort challenges
      const activeChallenges = allChallenges.filter(c => c.status === 'ACTIVE');
      const otherChallenges = allChallenges.filter(c => c.status !== 'ACTIVE');
      const sortedChallenges = [...activeChallenges, ...otherChallenges];
      
      setChallenges(sortedChallenges);
      
      // Auto-select first active challenge
      if (activeChallenges.length > 0) {
        setSelectedChallenge(activeChallenges[0].id);
      } else if (sortedChallenges.length > 0) {
        setSelectedChallenge(sortedChallenges[0].id);
      }
    } catch (error) {
      console.error('Error loading challenges:', error);
      setMessage({ 
        type: 'error', 
        text: t('errorLoadingChallenges', 'Error loading challenges') 
      });
    }
  };

  const loadTrades = async () => {
    try {
      const res = await tradingAPI.getTrades(selectedChallenge);
      setTrades(res.data.trades || []);
    } catch (error) {
      console.error('Error loading trades:', error);
    }
  };

  const executeTrade = async (side) => {
    // Validation
    if (!selectedChallenge) {
      setMessage({ 
        type: 'error', 
        text: t('selectChallenge', 'Please select a challenge') 
      });
      return;
    }
    
    if (!amount || parseFloat(amount) <= 0) {
      setMessage({ 
        type: 'error', 
        text: t('enterValidAmount', 'Please enter a valid amount') 
      });
      return;
    }
    
    if (!currentPrice) {
      setMessage({ 
        type: 'error', 
        text: t('priceNotAvailable', 'Price not available') 
      });
      return;
    }

    setLoading(true);
    setMessage(null);
    
    try {
      // In a real scenario, this would be an API call
      // For simulation, we'll create a simulated trade
      const tradeAmount = parseFloat(amount);
      const entryPrice = currentPrice.current_price;
      
      // Calculate profit/loss based on trade type and random market movement
      let profitLoss = 0;
      if (side === 'SELL') {
        // For sell, profit if price goes down
        const futurePrice = entryPrice * (1 + (Math.random() * 0.03 - 0.015)); // Random movement
        profitLoss = parseFloat((tradeAmount * (entryPrice - futurePrice)).toFixed(2));
      } else {
        // For buy, profit if price goes up
        const futurePrice = entryPrice * (1 + (Math.random() * 0.03 - 0.015)); // Random movement
        profitLoss = parseFloat((tradeAmount * (futurePrice - entryPrice)).toFixed(2));
      }
      
      // Simulate trade execution
      const simulatedTrade = {
        id: Date.now(),
        symbol: selectedSymbol.symbol,
        trade_type: side.toLowerCase(),
        quantity: tradeAmount,
        entry_price: entryPrice,
        exit_price: null,
        profit_loss: profitLoss,
        status: 'CLOSED',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      // Add to trades list
      setTrades(prev => [simulatedTrade, ...prev.slice(0, 14)]);
      
      // Update challenge balance
      setChallenges(prev => prev.map(c => 
        c.id === selectedChallenge 
          ? { ...c, current_balance: parseFloat((c.current_balance + profitLoss).toFixed(2)) }
          : c
      ));
      
      setMessage({ 
        type: 'success', 
        text: `${t('tradeExecuted', 'Trade executed')} ${side}! ${t('symbol', 'Symbol')}: ${selectedSymbol.symbol} | ${t('amount', 'Amount')}: ${tradeAmount} | ${t('pnl', 'P&L')}: ${profitLoss >= 0 ? '+' : ''}${profitLoss.toFixed(2)} ${currentPrice.currency}`
      });
      
      // Reset form
      setAmount('');
      
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: t('tradeExecutionFailed', 'Trade execution failed')
      });
    } finally {
      setLoading(false);
    }
  };

  const handlePriceUpdate = (priceData) => {
    setCurrentPrice(priceData);
  };

  // Simulate realistic market data
  const simulateMarketData = (symbol) => {
    const basePrices = {
      'AAPL': 175.43,
      'TSLA': 248.50,
      'GOOGL': 142.35,
      'MSFT': 378.85,
      'AMZN': 178.22,
      'META': 485.75,
      'NVDA': 127.50,
      'BTC-USD': 43250.75,
      'ETH-USD': 2650.30,
      'IAM': 124.60,
      'ATW': 89.45,
      'MAN': 215.30,
      'CGM': 187.90,
      'MSE': 45.60
    };
    
    const basePrice = basePrices[symbol] || 100;
    const volatility = {
      'CRYPTO': 0.03, // Higher volatility for crypto
      'US': 0.015,   // Moderate for US stocks
      'MOROCCO': 0.02 // Slightly higher for Morocco
    };
    
    const marketVolatility = volatility[selectedSymbol.market] || 0.015;
    const randomFactor = (Math.random() - 0.5) * 2 * marketVolatility;
    const currentPrice = basePrice * (1 + randomFactor);
    
    return {
      current_price: parseFloat(currentPrice.toFixed(2)),
      change: parseFloat((currentPrice - basePrice).toFixed(2)),
      change_percent: parseFloat(((currentPrice - basePrice) / basePrice * 100).toFixed(2)),
      high: parseFloat((currentPrice * 1.02).toFixed(2)),
      low: parseFloat((currentPrice * 0.98).toFixed(2)),
      volume: Math.floor(Math.random() * 10000000) + 5000000,
      currency: selectedSymbol.market === 'CRYPTO' ? 'USD' : 'DH',
      timestamp: new Date().toISOString()
    };
  };

  // Simulate market data periodically
  useEffect(() => {
    if (selectedSymbol) {
      const interval = setInterval(() => {
        setCurrentPrice(simulateMarketData(selectedSymbol.symbol));
      }, 3000); // Update every 3 seconds
      
      return () => clearInterval(interval);
    }
  }, [selectedSymbol]);

  return (
    <div className="trading-page">
      {/* Header */}
      <div className="trading-header">
        <h1>💱 {t('realTimeTrading', 'Real Time Trading')}</h1>
        <div className="live-badge">🔴 {t('live', 'LIVE')}</div>
      </div>

      {/* Message Display */}
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      {/* Main Trading Grid */}
      <div className="trading-grid">
        {/* Left Panel - Trading Interface */}
        <div className="trading-main">
          {/* Symbol Selector */}
          <div className="card symbol-selector-card">
            <h3>{t('selectSymbol', 'Select Symbol')}</h3>
            <div className="symbol-grid">
              {symbols.map(sym => (
                <button
                  key={sym.symbol}
                  className={`symbol-btn ${selectedSymbol.symbol === sym.symbol ? 'active' : ''}`}
                  onClick={() => setSelectedSymbol(sym)}
                >
                  <div className="symbol-name">{sym.symbol}</div>
                  <div className="symbol-market">{sym.market}</div>
                  <div className="symbol-currency">{sym.currency}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Price Display */}
          <div className="card price-card">
            <RealTimePriceComponent 
              symbol={selectedSymbol.symbol} 
              market={selectedSymbol.market} 
              onPriceUpdate={handlePriceUpdate}
            />
          </div>

          {/* Trading Panel */}
          <div className="card trading-panel">
            <h3>{t('executeTrade', 'Execute Trade')}</h3>
            
            {/* Challenge Selection */}
            <div className="form-group">
              <label className="form-label">{t('challenge', 'Challenge')}</label>
              <select 
                className="form-input"
                value={selectedChallenge || ''}
                onChange={(e) => setSelectedChallenge(parseInt(e.target.value))}
              >
                <option value="">{t('selectChallengeOption', 'Select a challenge')}</option>
                {challenges.map(c => (
                  <option key={c.id} value={c.id} disabled={c.status !== 'ACTIVE'}>
                    {c.plan_type.toUpperCase()} - {c.current_balance.toFixed(2)} DH [{c.status}]
                  </option>
                ))}
              </select>
              {challenges.length > 0 && challenges.filter(c => c.status === 'ACTIVE').length === 0 && (
                <small className="text-warning">
                  ⚠️ {t('noActiveChallenge', 'No active challenge. Please purchase one.')}
                </small>
              )}
            </div>

            {/* Amount Input */}
            <div className="form-group">
              <label className="form-label">
                {t('amount', 'Amount')} ({t('quantity', 'Quantity')})
              </label>
              <input
                type="number"
                className="form-input"
                placeholder="10"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                step="0.01"
                min="0"
              />
            </div>

            {/* Estimated Cost */}
            {currentPrice && amount && (
              <div className="cost-estimate">
                <span>{t('estimatedCost', 'Estimated cost')}:</span>
                <span className="cost-value">
                  {(parseFloat(amount) * currentPrice.current_price).toFixed(2)} {currentPrice.currency}
                </span>
              </div>
            )}

            {/* Trade Buttons */}
            <div className="trade-buttons">
              <button 
                className="btn btn-success btn-block"
                onClick={() => executeTrade('SELL')}
                disabled={loading || !selectedChallenge}
              >
                {loading ? '...' : `📈 ${t('sell', 'SELL')} (${t('profit', 'Profit')})`}
              </button>
              <button 
                className="btn btn-danger btn-block"
                onClick={() => executeTrade('BUY')}
                disabled={loading || !selectedChallenge}
              >
                {loading ? '...' : `📉 ${t('buy', 'BUY')} (${t('expense', 'Expense')})`}
              </button>
            </div>
            
            <div className="trade-info">
              <small>{t('tradeExplanation', 'SELL = Profit | BUY = Expense')}</small>
            </div>
          </div>
        </div>

        {/* Right Panel - Trades History */}
        <div className="trading-sidebar">
          <div className="card trades-history">
            <h3>{t('tradesHistory', 'Trades History')}</h3>
            <div className="trades-list">
              {trades.length === 0 ? (
                <div className="no-trades">
                  {t('noTradesYet', 'No trades yet')}
                </div>
              ) : (
                trades.slice(0, 15).map(trade => (
                  <div key={trade.id} className={`trade-item ${trade.trade_type}`}>
                    <div className="trade-header">
                      <span className="trade-symbol">{trade.symbol}</span>
                      <span className={`trade-type ${trade.trade_type}`}>
                        {trade.trade_type.toUpperCase()}
                      </span>
                    </div>
                    <div className="trade-details">
                      <div className="trade-price">
                        {t('price', 'Price')}: {trade.entry_price.toFixed(2)}
                      </div>
                      <div className={`trade-pl ${trade.profit_loss >= 0 ? 'positive' : 'negative'}`}>
                        {trade.profit_loss >= 0 ? '+' : ''}{trade.profit_loss.toFixed(2)} DH
                      </div>
                    </div>
                    <div className="trade-time">
                      {new Date(trade.created_at).toLocaleString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TradingPage;