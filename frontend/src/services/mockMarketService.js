// Mock Market Service for realistic market data simulation
const mockMarketData = {
  // US Stocks (USD)
  'AAPL-US': { current_price: 175.43, change: 1.25, change_percent: 0.72, high: 176.20, low: 174.10, volume: 55678900, currency: 'USD' },
  'TSLA-US': { current_price: 248.50, change: -2.30, change_percent: -0.92, high: 252.40, low: 247.80, volume: 34567890, currency: 'USD' },
  'GOOGL-US': { current_price: 142.35, change: 0.85, change_percent: 0.60, high: 143.10, low: 141.50, volume: 23456780, currency: 'USD' },
  'MSFT-US': { current_price: 378.85, change: 2.10, change_percent: 0.56, high: 379.50, low: 376.20, volume: 19876540, currency: 'USD' },
  'AMZN-US': { current_price: 178.22, change: -0.45, change_percent: -0.25, high: 179.80, low: 177.10, volume: 28765430, currency: 'USD' },
  'META-US': { current_price: 485.75, change: 3.20, change_percent: 0.66, high: 487.30, low: 482.10, volume: 15678900, currency: 'USD' },
  'NVDA-US': { current_price: 127.50, change: 4.75, change_percent: 3.86, high: 128.90, low: 123.40, volume: 45678900, currency: 'USD' },
  
  // Crypto (USD)
  'BTC-USD-CRYPTO': { current_price: 43250.75, change: 1250.50, change_percent: 2.98, high: 43500.20, low: 41800.50, volume: 12345678900, currency: 'USD' },
  'ETH-USD-CRYPTO': { current_price: 2650.30, change: -45.20, change_percent: -1.68, high: 2720.80, low: 2630.10, volume: 8765432100, currency: 'USD' },
  'ADA-USD-CRYPTO': { current_price: 0.45, change: 0.02, change_percent: 4.65, high: 0.46, low: 0.43, volume: 1234567890, currency: 'USD' },
  'BNB-USD-CRYPTO': { current_price: 310.25, change: -5.75, change_percent: -1.82, high: 318.50, low: 305.20, volume: 987654321, currency: 'USD' },
  
  // Morocco Stocks (MAD/DH)
  'IAM-MOROCCO': { current_price: 124.60, change: 0.30, change_percent: 0.24, high: 125.10, low: 123.80, volume: 1234567, currency: 'MAD' },
  'ATW-MOROCCO': { current_price: 89.45, change: -0.15, change_percent: -0.17, high: 90.20, low: 88.90, volume: 987654, currency: 'MAD' },
  'MAN-MOROCCO': { current_price: 215.30, change: 1.20, change_percent: 0.56, high: 216.50, low: 214.20, volume: 765432, currency: 'MAD' },
  'CGM-MOROCCO': { current_price: 187.90, change: 0.80, change_percent: 0.43, high: 188.50, low: 186.70, volume: 543210, currency: 'MAD' },
  'MSE-MOROCCO': { current_price: 45.60, change: -0.20, change_percent: -0.44, high: 46.20, low: 45.10, volume: 234567, currency: 'MAD' },
  
  // European Stocks (EUR)
  'SAN-EUR': { current_price: 3.45, change: 0.05, change_percent: 1.47, high: 3.48, low: 3.40, volume: 5432100, currency: 'EUR' },
  'AIR-EUR': { current_price: 12.30, change: -0.20, change_percent: -1.59, high: 12.50, low: 12.15, volume: 2345678, currency: 'EUR' },
  'MC-EUR': { current_price: 1520.00, change: 15.50, change_percent: 1.03, high: 1525.00, low: 1505.00, volume: 456789, currency: 'EUR' },
  
  // Forex pairs
  'EUR-USD-FX': { current_price: 1.0850, change: 0.0015, change_percent: 0.14, high: 1.0865, low: 1.0835, volume: 9876543210, currency: 'USD' },
  'GBP-USD-FX': { current_price: 1.2700, change: -0.0025, change_percent: -0.20, high: 1.2725, low: 1.2675, volume: 8765432100, currency: 'USD' },
  'USD-JPY-FX': { current_price: 149.50, change: 0.75, change_percent: 0.50, high: 149.75, low: 148.80, volume: 7654321000, currency: 'JPY' },
  'EUR-MAD-FX': { current_price: 11.8500, change: 0.0150, change_percent: 0.13, high: 11.8650, low: 11.8350, volume: 6543210000, currency: 'MAD' },
  
  // Commodities
  'CL-USD-COMMODITY': { current_price: 75.25, change: 1.25, change_percent: 1.69, high: 75.50, low: 74.10, volume: 34567890, currency: 'USD' },
  'GC-USD-COMMODITY': { current_price: 2035.50, change: -8.75, change_percent: -0.43, high: 2042.00, low: 2030.25, volume: 12345678, currency: 'USD' },
  'XAU-EUR-COMMODITY': { current_price: 1850.25, change: 5.50, change_percent: 0.30, high: 1852.50, low: 1845.75, volume: 5678901, currency: 'EUR' },
  
  // Asian Markets
  '7203-TOKYO': { current_price: 5800.00, change: 50.00, change_percent: 0.87, high: 5820.00, low: 5750.00, volume: 2345678, currency: 'JPY' },
  '2888-HK': { current_price: 3.45, change: -0.05, change_percent: -1.43, high: 3.52, low: 3.40, volume: 45678901, currency: 'HKD' },
  
  // Emerging markets
  'PETR4-SAO_PAULO': { current_price: 28.50, change: 0.75, change_percent: 2.70, high: 28.75, low: 27.80, volume: 56789012, currency: 'BRL' },
  'TCS-BOMBAY': { current_price: 3250.75, change: -15.25, change_percent: -0.47, high: 3275.50, low: 3240.00, volume: 2345678, currency: 'INR' }
};

// Simulate realistic market data with random fluctuations
export const getMockPrice = (symbol, market = 'US') => {
  const key = `${symbol}-${market}`;
  const baseData = mockMarketData[key] || mockMarketData['AAPL-US'];
  
  // Apply random fluctuation to simulate real-time movement
  const fluctuation = (Math.random() - 0.5) * 0.02; // ±1% fluctuation
  const newPrice = baseData.current_price * (1 + fluctuation);
  
  // Calculate change based on previous value
  const change = newPrice - baseData.current_price;
  const changePercent = (change / baseData.current_price) * 100;
  
  // Update high/low based on new price
  const high = Math.max(baseData.high, newPrice);
  const low = Math.min(baseData.low, newPrice);
  
  return {
    current_price: parseFloat(newPrice.toFixed(2)),
    change: parseFloat(change.toFixed(2)),
    change_percent: parseFloat(changePercent.toFixed(2)),
    high: parseFloat(high.toFixed(2)),
    low: parseFloat(low.toFixed(2)),
    volume: Math.floor(baseData.volume * (0.95 + Math.random() * 0.1)), // Volume fluctuation
    currency: baseData.currency,
    timestamp: new Date().toISOString()
  };
};

// Simulate delay for API-like behavior
export const simulateAPICall = (delay = 300) => {
  return new Promise(resolve => setTimeout(resolve, delay));
};