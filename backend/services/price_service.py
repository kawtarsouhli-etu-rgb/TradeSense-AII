"""
Real-Time Price Service with Caching
Optimized for frequent API calls
"""

import yfinance as yf
from datetime import datetime, timedelta
import threading
import time
from typing import Dict, Optional


class PriceCache:
    """Thread-safe price cache with TTL"""
    
    def __init__(self, ttl_seconds: int = 10):
        self.cache: Dict[str, Dict] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
        self.lock = threading.Lock()
    
    def get(self, symbol: str) -> Optional[Dict]:
        """Get cached price data if not expired"""
        with self.lock:
            if symbol in self.cache:
                cached_data = self.cache[symbol]
                if datetime.now() < cached_data['expires_at']:
                    return cached_data['data']
                else:
                    # Remove expired entry
                    del self.cache[symbol]
        return None
    
    def set(self, symbol: str, data: Dict):
        """Set cached price data with expiration"""
        with self.lock:
            self.cache[symbol] = {
                'data': data,
                'expires_at': datetime.now() + self.ttl
            }
    
    def cleanup_expired(self):
        """Remove all expired entries"""
        with self.lock:
            expired_symbols = []
            now = datetime.now()
            for symbol, cached_data in self.cache.items():
                if now >= cached_data['expires_at']:
                    expired_symbols.append(symbol)
            
            for symbol in expired_symbols:
                del self.cache[symbol]


class RealTimePriceService:
    """Service for fetching real-time prices with caching"""
    
    def __init__(self, cache_ttl: int = 10):
        self.cache = PriceCache(ttl_seconds=cache_ttl)
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
    
    def _cleanup_loop(self):
        """Background thread to periodically clean up expired cache entries"""
        while True:
            time.sleep(30)  # Clean up every 30 seconds
            self.cache.cleanup_expired()
    
    def get_price(self, ticker: str) -> Dict:
        """
        Get real-time price for a ticker with caching
        
        Args:
            ticker (str): Stock/crypto ticker (e.g., 'AAPL', 'BTC-USD')
            
        Returns:
            Dict: Price data with timestamp
        """
        # Check cache first
        cached_data = self.cache.get(ticker.upper())
        if cached_data:
            return cached_data
        
        try:
            # Fetch fresh data
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period='1d', interval='1m')
            
            if hist.empty:
                return {
                    'error': f'No data found for ticker: {ticker}',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get the latest price
            latest = hist.iloc[-1]
            
            price_data = {
                'symbol': ticker.upper(),
                'current_price': round(float(latest['Close']), 2),
                'previous_close': round(float(hist.iloc[-2]['Close']) if len(hist) > 1 else 0, 2),
                'change': round(float(latest['Close'] - latest['Open']), 2),
                'change_percent': round(((latest['Close'] - latest['Open']) / latest['Open']) * 100, 2),
                'high': round(float(latest['High']), 2),
                'low': round(float(latest['Low']), 2),
                'volume': int(latest['Volume']),
                'timestamp': datetime.now().isoformat(),
                'last_updated': latest.name.isoformat()  # Timestamp from yfinance
            }
            
            # Cache the result
            self.cache.set(ticker.upper(), price_data)
            
            return price_data
            
        except Exception as e:
            return {
                'error': f'Error fetching data for {ticker}: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_multiple_prices(self, tickers: list) -> Dict:
        """Get prices for multiple tickers"""
        results = {}
        for ticker in tickers:
            results[ticker] = self.get_price(ticker)
        return results


# Global instance
price_service = RealTimePriceService(cache_ttl=10)
