import React, { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

// Mock chart data generator
const generateChartData = (symbol, market, days = 30) => {
  const data = [];
  let basePrice = 100;
  
  // Set base price based on symbol
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
    'SAN': 3.45,
    'EUR-USD': 1.0850,
    'CL': 75.25,
    'GC': 2035.50
  };
  
  basePrice = basePrices[symbol] || 100;
  
  const now = Date.now();
  const dayInMs = 24 * 60 * 60 * 1000;
  
  for (let i = days; i >= 0; i--) {
    const time = now - (i * dayInMs);
    // Add some random fluctuation
    const fluctuation = (Math.random() - 0.5) * 0.05; // ±2.5%
    const price = basePrice * (1 + fluctuation);
    
    // Calculate high, low, open, close
    const open = i === days ? basePrice : data[data.length - 1]?.close || basePrice;
    const close = price;
    const high = Math.max(open, close) * (1 + Math.random() * 0.02);
    const low = Math.min(open, close) * (1 - Math.random() * 0.02);
    
    data.push({
      time: Math.floor(time / 1000), // Unix timestamp in seconds
      open,
      high,
      low,
      close
    });
  }
  
  return data;
};

const TradingViewChart = ({ symbol, market, priceData, onSymbolChange }) => {
  const { t } = useTranslation();
  const chartContainerRef = useRef();
  const [chart, setChart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!window.TradingView) {
      // Load TradingView Lightweight Charts library
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js';
      script.async = true;
      script.onload = initializeChart;
      script.onerror = () => setError('Failed to load chart library');
      document.head.appendChild(script);
    } else {
      initializeChart();
    }

    return () => {
      if (chart) {
        chart.remove();
      }
    };
  }, [symbol, market]);

  const initializeChart = () => {
    try {
      if (!chartContainerRef.current) return;

      // Clear any existing chart
      if (chart) {
        chart.remove();
      }

      // Create new chart
      const newChart = window.LightweightCharts.createChart(chartContainerRef.current, {
        width: chartContainerRef.current.clientWidth,
        height: 400,
        layout: {
          backgroundColor: '#0f172a',
          textColor: 'rgba(255, 255, 255, 0.9)',
        },
        grid: {
          vertLines: {
            color: 'rgba(255, 255, 255, 0.05)',
          },
          horzLines: {
            color: 'rgba(255, 255, 255, 0.05)',
          },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        },
        crosshair: {
          mode: LightweightCharts.CrosshairMode.Normal,
        },
      });

      // Generate mock data
      const chartData = generateChartData(symbol, market);

      // Add candlestick series
      const candleSeries = newChart.addCandlestickSeries({
        upColor: '#10b981',
        downColor: '#ef4444',
        borderDownColor: '#ef4444',
        borderUpColor: '#10b981',
        wickDownColor: '#ef4444',
        wickUpColor: '#10b981',
      });

      candleSeries.setData(chartData);

      // Add current price line
      if (priceData && priceData.current_price) {
        const currentPriceLine = newChart.addLineSeries({
          color: '#3b82f6',
          lineWidth: 1,
          lineStyle: 2, // Dashed line
          lastValueVisible: false,
        });
        
        // Add a single point at the current price
        const lastTimestamp = chartData[chartData.length - 1]?.time;
        if (lastTimestamp) {
          currentPriceLine.setData([
            { time: lastTimestamp, value: priceData.current_price },
            { time: lastTimestamp + 86400, value: priceData.current_price } // Extend line to tomorrow
          ]);
        }
      }

      setChart(newChart);
      setLoading(false);

      // Handle resize
      const resizeObserver = new ResizeObserver(entries => {
        if (entries.length === 0 || !entries[0].target) return;
        const { width, height } = entries[0].contentRect;
        newChart.resize(width, height);
      });

      resizeObserver.observe(chartContainerRef.current);

      return () => resizeObserver.disconnect();
    } catch (err) {
      setError('Chart initialization failed');
      setLoading(false);
      console.error('Chart error:', err);
    }
  };

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (chart) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: 400,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [chart]);

  return (
    <div className="tradingview-chart-container">
      <div className="chart-header">
        <h4>{symbol} - {market}</h4>
        {priceData && (
          <div className="current-price-display">
            <span className="price-value">{priceData.current_price}</span>
            <span className="currency">{priceData.currency}</span>
            {priceData.change && (
              <span className={`change ${priceData.change >= 0 ? 'positive' : 'negative'}`}>
                {priceData.change >= 0 ? '+' : ''}{priceData.change} ({priceData.change_percent >= 0 ? '+' : ''}{priceData.change_percent}%)
              </span>
            )}
          </div>
        )}
      </div>
      
      {loading && (
        <div className="chart-loading">
          <div className="loading-spinner"></div>
          <p>{t('loadingChart', 'Loading chart...')}</p>
        </div>
      )}
      
      {error && (
        <div className="chart-error">
          <p>{t('chartError', 'Error loading chart')}</p>
          <p className="error-message">{error}</p>
        </div>
      )}
      
      <div 
        ref={chartContainerRef} 
        className="chart-container"
        style={{ 
          height: '400px', 
          width: '100%',
          display: loading || error ? 'none' : 'block'
        }}
      />
      
      <div className="chart-controls">
        <button 
          className="chart-btn"
          onClick={() => {
            // Refresh chart by reinitializing
            if (chart) {
              chart.remove();
              setChart(null);
              setLoading(true);
              setError(null);
              setTimeout(initializeChart, 100);
            }
          }}
        >
          🔄 {t('refresh', 'Refresh')}
        </button>
        <button 
          className="chart-btn"
          onClick={() => {
            // Zoom in
            if (chart) {
              chart.timeScale().scrollToPosition(-100);
            }
          }}
        >
          🔍 {t('zoomIn', 'Zoom In')}
        </button>
        <button 
          className="chart-btn"
          onClick={() => {
            // Zoom out
            if (chart) {
              chart.timeScale().scrollToPosition(100);
            }
          }}
        >
          🔎 {t('zoomOut', 'Zoom Out')}
        </button>
      </div>
    </div>
  );
};

export default TradingViewChart;