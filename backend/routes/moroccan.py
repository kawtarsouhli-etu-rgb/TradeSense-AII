"""
Moroccan Stock Price API Routes
Exposes IAM (Maroc Telecom) stock price via API
"""

from flask import Blueprint, jsonify
from services.moroccan_scraper import scraper

moroccan_bp = Blueprint('moroccan', __name__, url_prefix='/api/moroccan')

@moroccan_bp.route('/stock/<ticker>', methods=['GET'])
def get_moroccan_stock(ticker):
    """
    Get real-time price for Moroccan stocks
    GET /api/moroccan/stock/IAM
    
    Returns:
    {
        "symbol": "IAM",
        "current_price": 55.25,
        "source": "bourse_ma",
        "scraped_from": "https://...",
        "timestamp": "2024-01-15T10:30:00.123456",
        "processing_time_ms": 1250
    }
    """
    try:
        ticker = ticker.upper().strip()
        
        if ticker not in ['IAM', 'IAM.MC', 'MAROC-TELECOM']:
            return jsonify({
                'error': f'Stock {ticker} not supported. Currently supporting: IAM',
                'supported_stocks': ['IAM'],
                'timestamp': 'null'
            }), 400
        
        # Fetch price data
        result = scraper.get_iam_price_with_fallback()
        
        # Return appropriate status code
        if 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'timestamp': 'null'
        }), 500


@moroccan_bp.route('/stocks', methods=['GET'])
def get_all_moroccan_stocks():
    """
    Get prices for all supported Moroccan stocks
    GET /api/moroccan/stocks
    
    Returns:
    {
        "stocks": {
            "IAM": {
                "current_price": 55.25,
                "source": "bourse_ma",
                ...
            }
        },
        "supported_count": 1,
        "timestamp": "2024-01-15T10:30:00.123456"
    }
    """
    try:
        # Get IAM price
        iam_result = scraper.get_iam_price_with_fallback()
        
        response = {
            'stocks': {},
            'supported_count': 0,
            'timestamp': 'null'
        }
        
        if 'error' not in iam_result:
            response['stocks']['IAM'] = iam_result
            response['supported_count'] = 1
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'timestamp': 'null'
        }), 500


@moroccan_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'moroccan-stock-scraper',
        'supported_stocks': ['IAM'],
        'timestamp': 'null'
    }), 200


# Also add to the main price endpoint for compatibility
@moroccan_bp.route('/price/<ticker>', methods=['GET'])
def get_moroccan_price(ticker):
    """
    Compatibility endpoint for moroccan stocks
    GET /api/moroccan/price/IAM
    Same as /api/moroccan/stock/IAM
    """
    return get_moroccan_stock(ticker)
