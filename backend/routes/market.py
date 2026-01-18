"""
Market data routes - Real-time prices and market information
"""

from flask import Blueprint, request, jsonify
from services.real_time_data import real_time_service

market_bp = Blueprint('market', __name__, url_prefix='/api/market')


@market_bp.route('/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """
    Get real-time price for a symbol
    GET /api/market/price/AAPL?market=US
    """
    try:
        market = request.args.get('market', 'US')
        data = real_time_service.get_live_price(symbol, market)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@market_bp.route('/prices', methods=['POST'])
def get_multiple_prices():
    """
    Get prices for multiple symbols
    POST /api/market/prices
    Body: {
        "symbols": [
            {"symbol": "AAPL", "market": "US"},
            {"symbol": "IAM", "market": "MOROCCO"}
        ]
    }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'No symbols provided'
            }), 400
        
        results = real_time_service.get_multiple_prices(symbols)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@market_bp.route('/watchlist', methods=['GET'])
def get_watchlist():
    """
    Get predefined watchlist with live prices
    GET /api/market/watchlist
    """
    try:
        watchlist = [
            {'symbol': 'AAPL', 'market': 'US', 'name': 'Apple Inc.'},
            {'symbol': 'TSLA', 'market': 'US', 'name': 'Tesla Inc.'},
            {'symbol': 'GOOGL', 'market': 'US', 'name': 'Alphabet Inc.'},
            {'symbol': 'MSFT', 'market': 'US', 'name': 'Microsoft Corp.'},
            {'symbol': 'BTC-USD', 'market': 'US', 'name': 'Bitcoin'},
            {'symbol': 'ETH-USD', 'market': 'US', 'name': 'Ethereum'},
            {'symbol': 'IAM', 'market': 'MOROCCO', 'name': 'Maroc Telecom'},
            {'symbol': 'ATW', 'market': 'MOROCCO', 'name': 'Attijariwafa Bank'},
        ]
        
        results = []
        for item in watchlist:
            price_data = real_time_service.get_live_price(item['symbol'], item['market'])
            price_data['display_name'] = item['name']
            results.append(price_data)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@market_bp.route('/morocco/stocks', methods=['GET'])
def get_morocco_stocks():
    """
    Get all available Moroccan stocks
    GET /api/market/morocco/stocks
    """
    try:
        morocco_stocks = [
            {'symbol': 'IAM', 'name': 'Maroc Telecom'},
            {'symbol': 'ATW', 'name': 'Attijariwafa Bank'},
            {'symbol': 'BCP', 'name': 'Banque Centrale Populaire'},
            {'symbol': 'CIH', 'name': 'CIH Bank'},
            {'symbol': 'LABEL', 'name': 'Label Vie'}
        ]
        
        results = []
        for stock in morocco_stocks:
            price_data = real_time_service.get_morocco_stock(stock['symbol'])
            results.append(price_data)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@market_bp.route('/search', methods=['GET'])
def search_symbols():
    """
    Search for symbols
    GET /api/market/search?q=apple
    """
    try:
        query = request.args.get('q', '').upper()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query required'
            }), 400
        
        # Predefined symbols database
        all_symbols = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'market': 'US'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'market': 'US'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'market': 'US'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'market': 'US'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'market': 'US'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'market': 'US'},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'market': 'US'},
            {'symbol': 'BTC-USD', 'name': 'Bitcoin', 'market': 'US'},
            {'symbol': 'ETH-USD', 'name': 'Ethereum', 'market': 'US'},
            {'symbol': 'IAM', 'name': 'Maroc Telecom', 'market': 'MOROCCO'},
            {'symbol': 'ATW', 'name': 'Attijariwafa Bank', 'market': 'MOROCCO'},
            {'symbol': 'BCP', 'name': 'Banque Centrale Populaire', 'market': 'MOROCCO'},
        ]
        
        # Filter results
        results = [
            s for s in all_symbols
            if query in s['symbol'] or query in s['name'].upper()
        ]
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
