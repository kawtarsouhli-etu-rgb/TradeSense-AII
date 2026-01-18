"""Market data service for fetching stock and crypto prices"""

import yfinance as yf
import random
from datetime import datetime


def get_stock_price(symbol):
    """
    Get current stock price using yfinance
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
        
    Returns:
        dict: {"symbol": str, "price": float, "timestamp": datetime}
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if data.empty:
            return {
                "symbol": symbol,
                "price": 0.0,
                "timestamp": datetime.utcnow(),
                "error": "No data available"
            }
        
        current_price = data['Close'].iloc[-1]
        
        return {
            "symbol": symbol,
            "price": float(current_price),
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        return {
            "symbol": symbol,
            "price": 0.0,
            "timestamp": datetime.utcnow(),
            "error": str(e)
        }


def get_crypto_price(symbol):
    """
    Get current cryptocurrency price using yfinance
    
    Args:
        symbol (str): Crypto symbol (e.g., 'BTC-USD', 'ETH-USD')
        
    Returns:
        dict: {"symbol": str, "price": float, "timestamp": datetime}
    """
    try:
        # Ensure symbol has -USD suffix for crypto
        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"
        
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if data.empty:
            return {
                "symbol": symbol,
                "price": 0.0,
                "timestamp": datetime.utcnow(),
                "error": "No data available"
            }
        
        current_price = data['Close'].iloc[-1]
        
        return {
            "symbol": symbol,
            "price": float(current_price),
            "timestamp": datetime.utcnow()
        }
    
    except Exception as e:
        return {
            "symbol": symbol,
            "price": 0.0,
            "timestamp": datetime.utcnow(),
            "error": str(e)
        }


def get_morocco_stock(symbol):
    """
    Get demonstration price for Moroccan stocks
    
    Args:
        symbol (str): Moroccan stock symbol (e.g., 'IAM', 'ATW')
        
    Returns:
        dict: {"symbol": str, "price": float, "timestamp": datetime}
    """
    # Generate random price between 100-150 DH
    demo_price = round(random.uniform(100, 150), 2)
    
    return {
        "symbol": symbol,
        "price": demo_price,
        "timestamp": datetime.utcnow()
    }
