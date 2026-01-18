import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { marketAPI, tradingAPI, challengeAPI } from '../services/api';
import TradingViewChart from '../components/TradingViewChart';
import './AdvancedTradingPage.css';

function AdvancedTradingPage() {
  const { t } = useTranslation();
  const [selectedSymbol, setSelectedSymbol] = useState({ 
    symbol: 'AAPL', 
    market: 'US', 
    name: 'Apple Inc.',
    currency: 'USD'
  });
  const [currentPrice, setCurrentPrice] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [trades, setTrades] = useState([]);
  const [portfolio, setPortfolio] = useState({ totalBalance: 0, totalPnL: 0, positions: [] });
  const [activeTab, setActiveTab] = useState('trading'); // trading, portfolio, analytics

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

  // Load challenges on component mount
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

  // Load trades when challenge is selected
  useEffect(() => {
    if (selectedChallenge) {
      loadTrades();
    }
  }, [selectedChallenge]);

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
      // Calculate profit/loss based on trade type and random market movement
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

  const calculatePortfolioStats = () => {
    // Calculate portfolio statistics
    const totalBalance = challenges.reduce((sum, challenge) => sum + challenge.current_balance, 0);
    const totalPnL = trades.reduce((sum, trade) => sum + trade.profit_loss, 0);
    
    setPortfolio({
      totalBalance,
      totalPnL,
      positions: trades.filter(t => t.status === 'OPEN')
    });
  };

  useEffect(() => {
    calculatePortfolioStats();
  }, [trades, challenges]);

  return (
    <div className="advanced-trading-page">
      {/* Header */}
      <div className="trading-header">
        <div className="header-content">
          <h1>📈 {t('advancedTrading', 'Advanced Trading Platform')}</h1>
          <div className="header-stats">
            <div className="stat-card">
              <div className="stat-value">${portfolio.totalBalance.toFixed(2)}</div>
              <div className="stat-label">{t('totalBalance', 'Total Balance')}</div>
            </div>
            <div className={`stat-card ${portfolio.totalPnL >= 0 ? 'positive' : 'negative'}`}>
              <div className="stat-value">{portfolio.totalPnL >= 0 ? '+' : ''}{portfolio.totalPnL.toFixed(2)}</div>
              <div className="stat-label">{t('totalPnL', 'Total P&L')}</div>
            </div>
          </div>
        </div>
        <div className="live-indicator">🔴 {t('live', 'LIVE')}</div>
      </div>

      {/* Tabs */}
      <div className="tabs-container">
        <button 
          className={`tab-button ${activeTab === 'trading' ? 'active' : ''}`}
          onClick={() => setActiveTab('trading')}
        >
          {t('trading', 'Trading')}
        </button>
        <button 
          className={`tab-button ${activeTab === 'portfolio' ? 'active' : ''}`}
          onClick={() => setActiveTab('portfolio')}
        >
          {t('portfolio', 'Portfolio')}
        </button>
        <button 
          className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          {t('analytics', 'Analytics')}
        </button>
      </div>

      {/* Message Display */}
      {message && (
        <div className={`alert alert-${message.type}`}>
          {message.text}
        </div>
      )}

      {/* Main Content based on active tab */}
      <div className="main-content">
        {activeTab === 'trading' && (
          <div className="trading-tab">
            {/* Symbol Selector */}
            <div className="card symbol-selector-card">
              <h3>{t('selectSymbol', 'Select Symbol')}</h3>
              <div className="symbol-grid">
                {symbols.map(sym => (
                  <button
                    key={`${sym.symbol}-${sym.market}`}
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

            {/* Chart Section */}
            <div className="card chart-card">
              <TradingViewChart 
                symbol={selectedSymbol.symbol} 
                market={selectedSymbol.market} 
                priceData={currentPrice}
                onSymbolChange={(newSymbol, newMarket) => {
                  const symbolObj = symbols.find(s => s.symbol === newSymbol && s.market === newMarket);
                  if (symbolObj) {
                    setSelectedSymbol(symbolObj);
                  }
                }}
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
        )}

        {activeTab === 'portfolio' && (
          <div className="portfolio-tab">
            <div className="card portfolio-overview">
              <h3>{t('portfolioOverview', 'Portfolio Overview')}</h3>
              <div className="portfolio-stats">
                <div className="stat-item">
                  <div className="stat-label">{t('totalBalance', 'Total Balance')}</div>
                  <div className="stat-value">${portfolio.totalBalance.toFixed(2)}</div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">{t('totalPnL', 'Total P&L')}</div>
                  <div className={`stat-value ${portfolio.totalPnL >= 0 ? 'positive' : 'negative'}`}>
                    {portfolio.totalPnL >= 0 ? '+' : ''}{portfolio.totalPnL.toFixed(2)}
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">{t('totalTrades', 'Total Trades')}</div>
                  <div className="stat-value">{trades.length}</div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">{t('winRate', 'Win Rate')}</div>
                  <div className="stat-value">
                    {trades.length > 0 
                      ? `${((trades.filter(t => t.profit_loss > 0).length / trades.length) * 100).toFixed(1)}%` 
                      : '0%'}
                  </div>
                </div>
              </div>
            </div>

            <div className="card positions-section">
              <h3>{t('openPositions', 'Open Positions')}</h3>
              {portfolio.positions.length === 0 ? (
                <div className="no-positions">
                  {t('noOpenPositions', 'No open positions')}
                </div>
              ) : (
                <div className="positions-list">
                  {portfolio.positions.map(position => (
                    <div key={position.id} className="position-item">
                      <div className="position-header">
                        <span className="position-symbol">{position.symbol}</span>
                        <span className={`position-type ${position.trade_type}`}>
                          {position.trade_type.toUpperCase()}
                        </span>
                      </div>
                      <div className="position-details">
                        <div className="position-price">
                          {t('entryPrice', 'Entry Price')}: {position.entry_price}
                        </div>
                        <div className={`position-pnl ${position.profit_loss >= 0 ? 'positive' : 'negative'}`}>
                          P&L: {position.profit_loss >= 0 ? '+' : ''}{position.profit_loss.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="analytics-tab">
            <div className="card performance-chart">
              <h3>{t('performanceChart', 'Performance Chart')}</h3>
              <div className="chart-placeholder">
                <p>📊 {t('performanceChartComingSoon', 'Performance chart coming soon')}</p>
              </div>
            </div>

            <div className="card market-analysis">
              <h3>{t('marketAnalysis', 'Market Analysis')}</h3>
              <div className="analysis-placeholder">
                <p>🔍 {t('marketAnalysisComingSoon', 'Market analysis tools coming soon')}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Trades History Sidebar */}
      <div className="sidebar">
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
  );
}

export default AdvancedTradingPage;