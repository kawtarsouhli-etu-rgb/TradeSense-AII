"""Payment routes"""

from flask import Blueprint, request, jsonify
from routes.auth import jwt_required
from services.payment_service import PaymentService
from services.challenge_service import ChallengeService

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payment')


# Payment plans configuration
PAYMENT_PLANS = [
    {
        'id': 'starter',
        'name': 'Starter',
        'price': 200,
        'currency': 'DH',
        'description': 'Perfect for beginners',
        'features': [
            'Initial balance: 1,000 DH',
            'Profit target: 10%',
            'Max daily loss: 5%',
            'Max total loss: 10%',
            'Basic trading tools'
        ],
        'challenge_config': {
            'plan_type': 'starter',
            'initial_balance': 1000.0,
            'profit_target': 100.0,
            'max_daily_loss': 50.0,
            'max_total_loss': 100.0
        }
    },
    {
        'id': 'pro',
        'name': 'Pro',
        'price': 500,
        'currency': 'DH',
        'description': 'For experienced traders',
        'features': [
            'Initial balance: 5,000 DH',
            'Profit target: 10%',
            'Max daily loss: 5%',
            'Max total loss: 10%',
            'Advanced trading tools',
            'Priority support'
        ],
        'challenge_config': {
            'plan_type': 'pro',
            'initial_balance': 5000.0,
            'profit_target': 500.0,
            'max_daily_loss': 250.0,
            'max_total_loss': 500.0
        }
    },
    {
        'id': 'elite',
        'name': 'Elite',
        'price': 1000,
        'currency': 'DH',
        'description': 'For professional traders',
        'features': [
            'Initial balance: 10,000 DH',
            'Profit target: 10%',
            'Max daily loss: 5%',
            'Max total loss: 10%',
            'Premium trading tools',
            '24/7 VIP support',
            'Personal account manager'
        ],
        'challenge_config': {
            'plan_type': 'elite',
            'initial_balance': 10000.0,
            'profit_target': 1000.0,
            'max_daily_loss': 500.0,
            'max_total_loss': 1000.0
        }
    }
]


@payment_bp.route('/plans', methods=['GET'])
def get_payment_plans():
    """
    Get available payment plans
    GET /api/payment/plans
    """
    try:
        return jsonify({
            'plans': PAYMENT_PLANS
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get payment plans: {str(e)}'}), 500


@payment_bp.route('/mock', methods=['POST'])
@jwt_required()
def mock_payment(user):
    """
    Mock payment processing - creates payment and challenge
    POST /api/payment/mock
    Headers: Authorization: Bearer <token>
    Body: {"plan_id": "starter|pro|elite"}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'plan_id' not in data:
            return jsonify({'error': 'Missing required field: plan_id'}), 400
        
        plan_id = data['plan_id'].lower()
        
        # Find plan
        plan = next((p for p in PAYMENT_PLANS if p['id'] == plan_id), None)
        
        if not plan:
            return jsonify({'error': f'Invalid plan_id. Must be one of: starter, pro, elite'}), 400
        
        # Create payment record
        payment, payment_error = PaymentService.create_payment(
            user_id=user.id,
            amount=plan['price'],
            currency=plan['currency'],
            payment_method='mock'
        )
        
        if payment_error:
            return jsonify({'error': payment_error}), 400
        
        # Process payment (mark as completed)
        processed_payment, process_error = PaymentService.process_payment(payment['id'])
        
        if process_error:
            return jsonify({'error': process_error}), 400
        
        # Create challenge
        challenge_config = plan['challenge_config']
        challenge, challenge_error = ChallengeService.create_challenge(
            user_id=user.id,
            plan_type=challenge_config['plan_type'],
            initial_balance=challenge_config['initial_balance'],
            profit_target=challenge_config['profit_target'],
            max_daily_loss=challenge_config['max_daily_loss'],
            max_total_loss=challenge_config['max_total_loss']
        )
        
        if challenge_error:
            return jsonify({'error': challenge_error}), 400
        
        return jsonify({
            'message': 'Payment processed and challenge created successfully',
            'payment': processed_payment,
            'challenge': challenge,
            'plan': {
                'id': plan['id'],
                'name': plan['name'],
                'price': plan['price'],
                'currency': plan['currency']
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': f'Failed to process payment: {str(e)}'}), 500


@payment_bp.route('/history', methods=['GET'])
@jwt_required()
def get_payment_history(user):
    """
    Get user's payment history
    GET /api/payment/history?status=completed
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get query parameters
        status = request.args.get('status')  # pending, completed, failed, refunded
        
        # Get payments
        payments, error = PaymentService.get_user_payments(user.id, status)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get payment statistics
        stats, stats_error = PaymentService.get_payment_statistics(user_id=user.id)
        
        return jsonify({
            'payments': payments,
            'statistics': stats if not stats_error else {}
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get payment history: {str(e)}'}), 500


@payment_bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(user, payment_id):
    """
    Get specific payment details
    GET /api/payment/<payment_id>
    Headers: Authorization: Bearer <token>
    """
    try:
        payment, error = PaymentService.get_payment_by_id(payment_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        # Verify payment belongs to user
        if payment['user_id'] != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({'payment': payment}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get payment: {str(e)}'}), 500
