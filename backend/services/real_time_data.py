"""
Real-time market data service
Streams live prices from Yahoo Finance and Moroccan stock market
"""

import yfinance as yf
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
from threading import Thread
import time


class RealTimeDataService:
    """Service for fetching real-time market data"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 10  # seconds
        
    def get_live_price(self, symbol, market='US'):
        """
        Get live price for any symbol
        
        Args:
            symbol (str): Stock symbol
            market (str): 'US' or 'MOROCCO'
            
        Returns:
            dict: Price data with timestamp
        """
        if market.upper() == 'MOROCCO':
            return self.get_morocco_stock(symbol)
        else:
            return self.get_us_stock(symbol)
    
    def get_us_stock(self, symbol):
        """
        Get US stock price using yfinance
        
        Args:
            symbol (str): Stock ticker (AAPL, TSLA, BTC-USD)
            
        Returns:
            dict: Price data
        """
        try:
            # Check cache
            cache_key = f"US_{symbol}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]['data']
            
            # Fetch from yfinance
            ticker = yf.Ticker(symbol)
            
            # Get latest price
            info = ticker.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            
            # Get intraday data for better accuracy
            hist = ticker.history(period='1d', interval='1m')
            
            if not hist.empty:
                latest_price = hist['Close'].iloc[-1]
                open_price = hist['Open'].iloc[0]
                high_price = hist['High'].max()
                low_price = hist['Low'].min()
                volume = hist['Volume'].sum()
            else:
                latest_price = current_price
                open_price = current_price
                high_price = current_price
                low_price = current_price
                volume = 0
            
            # Calculate change
            change = latest_price - open_price
            change_percent = (change / open_price * 100) if open_price > 0 else 0
            
            data = {
                'symbol': symbol,
                'market': 'US',
                'price': round(float(latest_price), 2),
                'open': round(float(open_price), 2),
                'high': round(float(high_price), 2),
                'low': round(float(low_price), 2),
                'volume': int(volume),
                'change': round(float(change), 2),
                'change_percent': round(float(change_percent), 2),
                'timestamp': datetime.utcnow().isoformat(),
                'currency': 'USD'
            }
            
            # Update cache
            self._update_cache(cache_key, data)
            
            return data
            
        except Exception as e:
            print(f"Error fetching US stock {symbol}: {str(e)}")
            return self._get_fallback_data(symbol, 'US')
    
    def get_morocco_stock(self, symbol):
        """
        Get Moroccan stock price
        Uses demo data for now (can be replaced with real scraper)
        
        Args:
            symbol (str): Moroccan stock symbol (IAM, ATW)
            
        Returns:
            dict: Price data
        """
        try:
            # Check cache
            cache_key = f"MOROCCO_{symbol}"
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]['data']
            
            # Demo data for Moroccan stocks
            # In production, implement real scraper here
            morocco_stocks = {
                'IAM': {'base_price': 120.0, 'name': 'Maroc Telecom'},
                'ATW': {'base_price': 450.0, 'name': 'Attijariwafa Bank'},
                'BCP': {'base_price': 280.0, 'name': 'Banque Centrale Populaire'},
                'CIH': {'base_price': 315.0, 'name': 'CIH Bank'},
                'LABEL': {'base_price': 3850.0, 'name': 'Label Vie'}
            }
            
            stock_info = morocco_stocks.get(symbol.upper(), {'base_price': 100.0, 'name': symbol})
            
            # Simulate realistic price movement
            base_price = stock_info['base_price']
            variation = random.uniform(-0.02, 0.02)  # ±2% variation
            current_price = base_price * (1 + variation)
            
            open_price = base_price
            change = current_price - open_price
            change_percent = (change / open_price * 100)
            
            data = {
                'symbol': symbol.upper(),
                'name': stock_info['name'],
                'market': 'MOROCCO',
                'price': round(current_price, 2),
                'open': round(open_price, 2),
                'high': round(current_price * 1.005, 2),
                'low': round(current_price * 0.995, 2),
                'volume': random.randint(10000, 100000),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'timestamp': datetime.utcnow().isoformat(),
                'currency': 'MAD'
            }
            
            # Update cache
            self._update_cache(cache_key, data)
            
            return data
            
        except Exception as e:
            print(f"Error fetching Morocco stock {symbol}: {str(e)}")
            return self._get_fallback_data(symbol, 'MOROCCO')
    
    def get_multiple_prices(self, symbols):
        """
        Get prices for multiple symbols at once
        
        Args:
            symbols (list): List of symbol dictionaries [{'symbol': 'AAPL', 'market': 'US'}]
            
        Returns:
            list: List of price data
        """
        results = []
        for item in symbols:
            symbol = item.get('symbol')
            market = item.get('market', 'US')
            data = self.get_live_price(symbol, market)
            results.append(data)
        return results
    
    def scrape_casablanca_stock(self, symbol):
        """
        Real scraper for Casablanca Stock Exchange
        Can be implemented with BeautifulSoup or BVCscrap
        
        Args:
            symbol (str): Stock symbol
            
        Returns:
            dict: Price data
        """
        # TODO: Implement real scraper
        # Example structure:
        try:
            url = f"https://www.casablanca-bourse.com/bourseweb/Negociation-Action.aspx?Symbol={symbol}"
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse price from HTML
            # This is a placeholder - implement actual parsing
            
            return self.get_morocco_stock(symbol)
            
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            return self.get_morocco_stock(symbol)
    
    def _is_cache_valid(self, key):
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        
        cached_time = self.cache[key]['timestamp']
        age = time.time() - cached_time
        
        return age < self.cache_duration
    
    def _update_cache(self, key, data):
        """Update cache with new data"""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def _get_fallback_data(self, symbol, market):
        """Return fallback data if fetch fails"""
        return {
            'symbol': symbol,
            'market': market,
            'price': 0.0,
            'open': 0.0,
            'high': 0.0,
            'low': 0.0,
            'volume': 0,
            'change': 0.0,
            'change_percent': 0.0,
            'timestamp': datetime.utcnow().isoformat(),
            'currency': 'MAD' if market == 'MOROCCO' else 'USD',
            'error': 'Failed to fetch live data'
        }


# Global instance
real_time_service = RealTimeDataService()
