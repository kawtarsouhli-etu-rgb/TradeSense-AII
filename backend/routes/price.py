"""
Real-Time Price API Routes
Optimized for frequent calls with caching
"""

from flask import Blueprint, request, jsonify
from services.price_service import price_service

price_bp = Blueprint('price', __name__, url_prefix='/api/price')

@price_bp.route('/<ticker>', methods=['GET'])
def get_price(ticker):
    """
    Get real-time price for a ticker
    GET /api/price/AAPL
    GET /api/price/BTC-USD
    GET /api/price/TSLA
    
    Returns:
    {
        "symbol": "AAPL",
        "current_price": 150.25,
        "previous_close": 149.80,
        "change": 0.45,
        "change_percent": 0.30,
        "high": 151.20,
        "low": 149.50,
        "volume": 12345678,
        "timestamp": "2024-01-15T10:30:00.123456",
        "last_updated": "2024-01-15T10:29:00"
    }
    """
    try:
        # Validate input
        if not ticker or len(ticker.strip()) == 0:
            return jsonify({
                'error': 'Ticker symbol is required',
                'timestamp': 'null'
            }), 400
        
        # Fetch price data
        result = price_service.get_price(ticker)
        
        # Return appropriate status code
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'timestamp': 'null'
        }), 500


@price_bp.route('/', methods=['GET'])
def get_multiple_prices():
    """
    Get real-time prices for multiple tickers
    GET /api/price/?tickers=AAPL,TSLA,BTC-USD
    
    Returns:
    {
        "prices": {
            "AAPL": {...},
            "TSLA": {...},
            "BTC-USD": {...}
        }
    }
    """
    try:
        tickers_str = request.args.get('tickers', '')
        
        if not tickers_str:
            return jsonify({
                'error': 'Tickers parameter is required (comma separated)',
                'timestamp': 'null'
            }), 400
        
        tickers = [ticker.strip().upper() for ticker in tickers_str.split(',')]
        
        if len(tickers) > 10:  # Limit to prevent abuse
            return jsonify({
                'error': 'Maximum 10 tickers allowed per request',
                'timestamp': 'null'
            }), 400
        
        # Fetch prices for all tickers
        results = {}
        for ticker in tickers:
            results[ticker] = price_service.get_price(ticker)
        
        return jsonify({
            'prices': results,
            'timestamp': 'null'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'timestamp': 'null'
        }), 500


@price_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'real-time-price-api',
        'timestamp': 'null'
    }), 200
