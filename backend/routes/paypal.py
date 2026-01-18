"""
PayPal API Routes
"""

from flask import Blueprint, request, jsonify, redirect, url_for
from routes.auth import jwt_required, superadmin_required
from services.paypal_service import PayPalService
from models import db, PayPalSettings, User
from datetime import datetime

paypal_bp = Blueprint('paypal', __name__, url_prefix='/api/paypal')


# Challenge plan configurations (same as payment.py)
CHALLENGE_PLANS = {
    'starter': {
        'name': 'Starter',
        'price': 200,
        'currency': 'USD',
        'initial_balance': 1000.0,
        'profit_target': 100.0,    # 10%
        'max_daily_loss': 50.0,    # 5%
        'max_total_loss': 100.0    # 10%
    },
    'pro': {
        'name': 'Pro',
        'price': 500,
        'currency': 'USD',
        'initial_balance': 5000.0,
        'profit_target': 500.0,    # 10%
        'max_daily_loss': 250.0,   # 5%
        'max_total_loss': 500.0    # 10%
    },
    'elite': {
        'name': 'Elite',
        'price': 1000,
        'currency': 'USD',
        'initial_balance': 10000.0,
        'profit_target': 1000.0,   # 10%
        'max_daily_loss': 500.0,   # 5%
        'max_total_loss': 1000.0   # 10%
    }
}


@paypal_bp.route('/create-payment', methods=['POST'])
@jwt_required()
def create_paypal_payment(user):
    """
    Create a PayPal payment for challenge purchase
    POST /api/paypal/create-payment
    Body: {"plan_id": "pro"}
    """
    try:
        data = request.get_json()
        
        if not data or 'plan_id' not in data:
            return jsonify({'error': 'Missing plan_id'}), 400
        
        plan_id = data['plan_id'].lower()
        
        if plan_id not in CHALLENGE_PLANS:
            return jsonify({'error': 'Invalid plan'}), 400
        
        plan_config = CHALLENGE_PLANS[plan_id]
        
        # Frontend URLs (will be configured in frontend)
        return_url = request.headers.get('Referer', '') + '?payment=success'
        cancel_url = request.headers.get('Referer', '') + '?payment=cancelled'
        
        # Create PayPal payment
        approval_url, payment_id, error = PayPalService.create_payment(
            user_id=user.id,
            plan_id=plan_id,
            plan_price=plan_config['price'],
            plan_name=plan_config['name'],
            return_url=return_url,
            cancel_url=cancel_url
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'approval_url': approval_url,
            'payment_id': payment_id,
            'plan': plan_config
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Payment creation failed: {str(e)}'}), 500


@paypal_bp.route('/execute-payment', methods=['POST'])
@jwt_required()
def execute_paypal_payment(user):
    """
    Execute PayPal payment after user approval
    POST /api/paypal/execute-payment
    Body: {"payment_id": "...", "payer_id": "...", "plan_id": "pro"}
    """
    try:
        data = request.get_json()
        
        required_fields = ['payment_id', 'payer_id', 'plan_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400
        
        payment_id = data['payment_id']
        payer_id = data['payer_id']
        plan_id = data['plan_id'].lower()
        
        if plan_id not in CHALLENGE_PLANS:
            return jsonify({'error': 'Invalid plan'}), 400
        
        plan_config = CHALLENGE_PLANS[plan_id]
        
        # Execute payment
        payment_result, challenge_result, error = PayPalService.execute_payment(
            payment_id=payment_id,
            payer_id=payer_id,
            plan_id=plan_id,
            plan_config=plan_config
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Payment successful and challenge activated!',
            'payment': payment_result,
            'challenge': challenge_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Payment execution failed: {str(e)}'}), 500


# ==================== ADMIN ROUTES ====================

@paypal_bp.route('/settings', methods=['GET'])
@superadmin_required()
def get_paypal_settings(user):
    """
    Get PayPal configuration settings (SuperAdmin only)
    GET /api/paypal/settings
    """
    try:
        settings = PayPalSettings.query.first()
        
        if not settings:
            return jsonify({'settings': None}), 200
        
        return jsonify({'settings': settings.to_dict(include_secret=False)}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get settings: {str(e)}'}), 500


@paypal_bp.route('/settings', methods=['POST'])
@superadmin_required()
def update_paypal_settings(user):
    """
    Update PayPal configuration settings (SuperAdmin only)
    POST /api/paypal/settings
    Body: {
        "mode": "sandbox",
        "client_id": "...",
        "client_secret": "...",
        "is_active": true
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['mode', 'client_id', 'client_secret']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {", ".join(required_fields)}'}), 400
        
        # Deactivate existing settings
        existing = PayPalSettings.query.first()
        if existing:
            existing.is_active = False
            db.session.commit()
        
        # Create new settings
        settings = PayPalSettings(
            mode=data['mode'].lower(),
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            is_active=data.get('is_active', True),
            updated_by=user.id
        )
        
        db.session.add(settings)
        db.session.commit()
        
        return jsonify({
            'message': 'PayPal settings updated successfully',
            'settings': settings.to_dict(include_secret=False)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update settings: {str(e)}'}), 500


@paypal_bp.route('/settings/test', methods=['POST'])
@superadmin_required()
def test_paypal_connection(user):
    """
    Test PayPal API connection with current settings
    POST /api/paypal/settings/test
    """
    try:
        success, error = PayPalService.configure_paypal()
        
        if success:
            return jsonify({'message': 'PayPal connection successful'}), 200
        else:
            return jsonify({'error': error}), 400
            
    except Exception as e:
        return jsonify({'error': f'Connection test failed: {str(e)}'}), 500
