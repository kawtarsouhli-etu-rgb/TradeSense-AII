import React, { useEffect, useState } from 'react';
import { usePrice } from '../context/PriceContext';
import TradingViewChart from '../components/TradingViewChart';

const RealTimePriceComponent = ({ symbol, market = 'US', onPriceUpdate }) => {
  const { prices, startAutoRefresh, stopAutoRefresh, isLoading } = usePrice();
  const [currentSymbol, setCurrentSymbol] = useState(symbol);
  const [currentMarket, setCurrentMarket] = useState(market);

  // Get current price data
  const priceKey = `${currentSymbol}-${currentMarket}`;
  const currentPrice = prices[priceKey];

  // Notify parent of price updates
  useEffect(() => {
    if (currentPrice && onPriceUpdate) {
      onPriceUpdate(currentPrice);
    }
  }, [currentPrice, onPriceUpdate]);

  // Start auto-refresh when component mounts - optimized
  useEffect(() => {
    let isActive = true;
    
    // Start with immediate fetch
    const initialFetch = async () => {
      if (isActive) {
        try {
          await startAutoRefresh(currentSymbol, currentMarket, 15000);
        } catch (error) {
          console.warn('Initial price fetch failed:', error);
        }
      }
    };
    
    initialFetch();

    return () => {
      isActive = false;
      stopAutoRefresh(currentSymbol, currentMarket);
    };
  }, [currentSymbol, currentMarket, startAutoRefresh, stopAutoRefresh]);

  // Handle symbol change
  const handleSymbolChange = (newSymbol, newMarket) => {
    // Stop current interval
    stopAutoRefresh(currentSymbol, currentMarket);
    
    // Update state
    setCurrentSymbol(newSymbol);
    setCurrentMarket(newMarket);
    
    // Start new interval
    startAutoRefresh(newSymbol, newMarket, 15000);
  };

  // Format price change
  const formatChange = (change, changePercent) => {
    if (!change || !changePercent) return null;
    
    const sign = change >= 0 ? '+' : '';
    const changeStr = `${sign}${change}`;
    const percentStr = `${sign}${changePercent}%`;
    
    return (
      <span className={`change ${change >= 0 ? 'positive' : 'negative'}`}>
        {changeStr} ({percentStr})
      </span>
    );
  };

  return (
    <div className="real-time-price-component">
      <div className="price-header">
        <h3>{currentSymbol} ({currentMarket})</h3>
        {isLoading[priceKey] && <span className="loading-indicator">🔄</span>}
      </div>

      <div className="price-display">
        {currentPrice ? (
          <>
            <div className="current-price">
              <span className="price-value">{currentPrice.current_price}</span>
              <span className="currency">{currentPrice.currency}</span>
            </div>
            <div className="price-change">
              {formatChange(currentPrice.change, currentPrice.change_percent)}
            </div>
            <div className="price-details">
              <div className="detail-item">
                <span>High</span>
                <span>{currentPrice.high}</span>
              </div>
              <div className="detail-item">
                <span>Low</span>
                <span>{currentPrice.low}</span>
              </div>
              <div className="detail-item">
                <span>Volume</span>
                <span>{currentPrice.volume?.toLocaleString()}</span>
              </div>
            </div>
          </>
        ) : (
          <div className="no-data">Loading price data...</div>
        )}
      </div>

      <div className="chart-section">
        <TradingViewChart 
          symbol={currentSymbol}
          market={currentMarket}
          priceData={currentPrice}
          onSymbolChange={handleSymbolChange}
        />
      </div>

      <div className="refresh-status">
        <small>Last updated: {currentPrice?.timestamp ? new Date(currentPrice.timestamp).toLocaleTimeString() : 'N/A'}</small>
      </div>
    </div>
  );
};

export default RealTimePriceComponent;