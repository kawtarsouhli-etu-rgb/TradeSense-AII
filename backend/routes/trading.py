"""Trading routes"""

from flask import Blueprint, request, jsonify
from routes.auth import jwt_required
from services.trade_service import TradeService
from services.market_data import get_stock_price, get_crypto_price, get_morocco_stock
from services.challenge_monitor import check_challenge_rules
from models import db, UserChallenge, Trade
from challenge_engine import evaluate_challenge, get_challenge_metrics

trading_bp = Blueprint('trading', __name__, url_prefix='/api')


@trading_bp.route('/trade/execute', methods=['POST'])
def execute_trade():
    """
    Execute a trade (BUY or SELL) and update challenge balance
    POST /api/trade/execute
    Body: {
        "challenge_id": 1,
        "symbol": "AAPL",
        "side": "BUY" or "SELL",
        "amount": 100.0,
        "price": 150.25
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['challenge_id', 'symbol', 'side', 'amount', 'price']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        challenge_id = int(data['challenge_id'])
        symbol = data['symbol'].upper()
        side = data['side'].upper()
        amount = float(data['amount'])
        price = float(data['price'])
        
        # Validate side
        if side not in ['BUY', 'SELL']:
            return jsonify({
                'success': False,
                'error': 'Side must be BUY or SELL'
            }), 400
        
        # Get challenge
        challenge = UserChallenge.query.get(challenge_id)
        if not challenge:
            return jsonify({
                'success': False,
                'error': 'Challenge not found'
            }), 404
        
        # Check if challenge is active
        if challenge.status != 'ACTIVE':
            return jsonify({
                'success': False,
                'error': f'Challenge is {challenge.status}. Cannot execute trades.'
            }), 400
        
        # Calculate trade value
        trade_value = amount * price
        
        # Calculate P&L (simplified: BUY = negative, SELL = positive)
        if side == 'BUY':
            profit_loss = -trade_value
        else:  # SELL
            profit_loss = trade_value
        
        # Create trade record
        trade = Trade(
            challenge_id=challenge_id,
            user_id=challenge.user_id,
            symbol=symbol,
            trade_type=side.lower(),
            quantity=amount,
            entry_price=price,
            exit_price=price if side == 'SELL' else None,
            profit_loss=profit_loss,
            status='closed' if side == 'SELL' else 'open'
        )
        
        # Update challenge balance
        challenge.current_balance += profit_loss
        
        # Save trade and updated balance
        db.session.add(trade)
        db.session.commit()
        
        # Evaluate challenge after trade
        evaluation = evaluate_challenge(challenge_id)
        
        # Get detailed metrics
        metrics = get_challenge_metrics(challenge_id)
        
        return jsonify({
            'success': True,
            'trade': {
                'id': trade.id,
                'symbol': symbol,
                'side': side,
                'amount': amount,
                'price': price,
                'profit_loss': round(profit_loss, 2),
                'timestamp': trade.created_at.isoformat()
            },
            'challenge': {
                'id': challenge_id,
                'status': evaluation['status'],
                'balance': evaluation['balance'],
                'message': evaluation['message']
            },
            'account_state': {
                'balance': challenge.current_balance,
                'equity': challenge.current_balance,  # Simplified: equity = balance for now
                'challenge_id': challenge.id,
                'challenge_status': evaluation['status']
            },
            'metrics': metrics
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid numeric value: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Trade execution failed: {str(e)}'
        }), 500


@trading_bp.route('/trade/buy', methods=['POST'])
@jwt_required()
def buy_trade_endpoint(user):
    """
    Execute a BUY trade at current market price
    POST /api/trade/buy
    Headers: Authorization: Bearer <token>
    Body: {
        "challenge_id": 1,
        "symbol": "AAPL",
        "amount": 100.0
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['challenge_id', 'symbol', 'amount']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        challenge_id = int(data['challenge_id'])
        symbol = data['symbol'].upper()
        amount = float(data['amount'])
        
        # Get current market price
        if symbol in ['BTC', 'ETH', 'BTC-USD', 'ETH-USD']:
            price_data = get_crypto_price(symbol)
        elif symbol in ['IAM', 'ATW']:
            price_data = get_morocco_stock(symbol)
        else:
            price_data = get_stock_price(symbol)
        
        if 'error' in price_data:
            return jsonify({
                'success': False,
                'error': f'Failed to get market price: {price_data["error"]}'
            }), 400
        
        market_price = price_data['price']
        
        # Validate challenge ownership
        challenge = UserChallenge.query.get(challenge_id)
        if not challenge or challenge.user_id != user.id:
            return jsonify({
                'success': False,
                'error': 'Challenge not found or unauthorized'
            }), 404
        
        # Calculate trade value and P&L
        trade_value = amount * market_price
        profit_loss = -trade_value  # Negative for BUY
        
        # Create trade record
        trade = Trade(
            challenge_id=challenge_id,
            user_id=challenge.user_id,
            symbol=symbol,
            trade_type='buy',
            quantity=amount,
            entry_price=market_price,
            exit_price=None,
            profit_loss=profit_loss,
            status='open'
        )
        
        # Update challenge balance
        challenge.current_balance += profit_loss
        
        # Save trade and updated balance
        db.session.add(trade)
        db.session.commit()
        
        # Evaluate challenge after trade
        evaluation = evaluate_challenge(challenge_id)
        
        # Get detailed metrics
        metrics = get_challenge_metrics(challenge_id)
        
        return jsonify({
            'success': True,
            'trade': {
                'id': trade.id,
                'symbol': symbol,
                'side': 'BUY',
                'amount': amount,
                'price': market_price,
                'profit_loss': round(profit_loss, 2),
                'timestamp': trade.created_at.isoformat()
            },
            'account_state': {
                'balance': challenge.current_balance,
                'equity': challenge.current_balance,
                'challenge_id': challenge.id,
                'challenge_status': evaluation['status']
            },
            'metrics': metrics
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid numeric value: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Buy trade execution failed: {str(e)}'
        }), 500


@trading_bp.route('/trade/sell', methods=['POST'])
@jwt_required()
def sell_trade_endpoint(user):
    """
    Execute a SELL trade at current market price
    POST /api/trade/sell
    Headers: Authorization: Bearer <token>
    Body: {
        "challenge_id": 1,
        "symbol": "AAPL",
        "amount": 100.0
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['challenge_id', 'symbol', 'amount']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        challenge_id = int(data['challenge_id'])
        symbol = data['symbol'].upper()
        amount = float(data['amount'])
        
        # Get current market price
        if symbol in ['BTC', 'ETH', 'BTC-USD', 'ETH-USD']:
            price_data = get_crypto_price(symbol)
        elif symbol in ['IAM', 'ATW']:
            price_data = get_morocco_stock(symbol)
        else:
            price_data = get_stock_price(symbol)
        
        if 'error' in price_data:
            return jsonify({
                'success': False,
                'error': f'Failed to get market price: {price_data["error"]}'
            }), 400
        
        market_price = price_data['price']
        
        # Validate challenge ownership
        challenge = UserChallenge.query.get(challenge_id)
        if not challenge or challenge.user_id != user.id:
            return jsonify({
                'success': False,
                'error': 'Challenge not found or unauthorized'
            }), 404
        
        # Calculate trade value and P&L
        trade_value = amount * market_price
        profit_loss = trade_value  # Positive for SELL
        
        # Create trade record
        trade = Trade(
            challenge_id=challenge_id,
            user_id=challenge.user_id,
            symbol=symbol,
            trade_type='sell',
            quantity=amount,
            entry_price=market_price,
            exit_price=market_price,
            profit_loss=profit_loss,
            status='closed'
        )
        
        # Update challenge balance
        challenge.current_balance += profit_loss
        
        # Save trade and updated balance
        db.session.add(trade)
        db.session.commit()
        
        # Evaluate challenge after trade
        evaluation = evaluate_challenge(challenge_id)
        
        # Get detailed metrics
        metrics = get_challenge_metrics(challenge_id)
        
        return jsonify({
            'success': True,
            'trade': {
                'id': trade.id,
                'symbol': symbol,
                'side': 'SELL',
                'amount': amount,
                'price': market_price,
                'profit_loss': round(profit_loss, 2),
                'timestamp': trade.created_at.isoformat()
            },
            'account_state': {
                'balance': challenge.current_balance,
                'equity': challenge.current_balance,
                'challenge_id': challenge.id,
                'challenge_status': evaluation['status']
            },
            'metrics': metrics
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid numeric value: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Sell trade execution failed: {str(e)}'
        }), 500


@trading_bp.route('/trades', methods=['GET'])
@jwt_required()
def get_trades(user):
    """
    Get user's trade history
    GET /api/trades?status=open&challenge_id=1
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get query parameters
        status = request.args.get('status')  # open or closed
        challenge_id = request.args.get('challenge_id')
        
        # Get trades
        if challenge_id:
            trades, error = TradeService.get_challenge_trades(int(challenge_id), status)
        else:
            trades, error = TradeService.get_user_trades(user.id, status)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get trade statistics
        stats, stats_error = TradeService.get_trade_statistics(user_id=user.id)
        
        return jsonify({
            'trades': trades,
            'statistics': stats if not stats_error else {}
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get trades: {str(e)}'}), 500


@trading_bp.route('/trade/<int:trade_id>', methods=['GET'])
@jwt_required()
def get_trade(user, trade_id):
    """
    Get specific trade details
    GET /api/trade/<trade_id>
    Headers: Authorization: Bearer <token>
    """
    try:
        trade, error = TradeService.get_trade_by_id(trade_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        # Verify trade belongs to user
        if trade['user_id'] != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'trade': trade}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get trade: {str(e)}'}), 500


@trading_bp.route('/challenge/<int:challenge_id>/metrics', methods=['GET'])
def get_metrics(challenge_id):
    """
    Get detailed challenge metrics
    GET /api/challenge/<challenge_id>/metrics
    """
    try:
        metrics = get_challenge_metrics(challenge_id)
        
        if not metrics:
            return jsonify({
                'success': False,
                'error': 'Challenge not found'
            }), 404
        
        return jsonify({
            'success': True,
            'metrics': metrics
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get metrics: {str(e)}'
        }), 500