"""Challenge routes"""

from flask import Blueprint, request, jsonify
from routes.auth import jwt_required
from services.challenge_service import ChallengeService
from services.challenge_monitor import check_challenge_rules
from models import db

challenges_bp = Blueprint('challenges', __name__, url_prefix='/api/challenges')


# Challenge plan configurations
CHALLENGE_PLANS = {
    'starter': {
        'initial_balance': 1000.0,
        'profit_target': 100.0,  # 10%
        'max_daily_loss': 50.0,  # 5%
        'max_total_loss': 100.0  # 10%
    },
    'pro': {
        'initial_balance': 5000.0,
        'profit_target': 500.0,  # 10%
        'max_daily_loss': 250.0,  # 5%
        'max_total_loss': 500.0  # 10%
    },
    'elite': {
        'initial_balance': 10000.0,
        'profit_target': 1000.0,  # 10%
        'max_daily_loss': 500.0,  # 5%
        'max_total_loss': 1000.0  # 10%
    }
}


@challenges_bp.route('', methods=['GET'])
@jwt_required()
def get_challenges(user):
    """
    Get user's challenges
    GET /api/challenges?status=active
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get query parameters
        status = request.args.get('status')  # active, passed, failed, completed
        
        # Get challenges
        challenges, error = ChallengeService.get_user_challenges(user.id, status)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'challenges': challenges,
            'total': len(challenges)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get challenges: {str(e)}'}), 500


@challenges_bp.route('/create', methods=['POST'])
@jwt_required()
def create_challenge(user):
    """
    Create a new challenge
    POST /api/challenges/create
    Headers: Authorization: Bearer <token>
    Body: {"plan_type": "starter|pro|elite"}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'plan_type' not in data:
            return jsonify({'error': 'Missing required field: plan_type'}), 400
        
        plan_type = data['plan_type'].lower()
        
        # Validate plan type
        if plan_type not in CHALLENGE_PLANS:
            return jsonify({'error': f'Invalid plan type. Must be one of: starter, pro, elite'}), 400
        
        # Get plan configuration
        plan_config = CHALLENGE_PLANS[plan_type]
        
        # Create challenge
        challenge, error = ChallengeService.create_challenge(
            user_id=user.id,
            plan_type=plan_type,
            initial_balance=plan_config['initial_balance'],
            profit_target=plan_config['profit_target'],
            max_daily_loss=plan_config['max_daily_loss'],
            max_total_loss=plan_config['max_total_loss']
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Challenge created successfully',
            'challenge': challenge
        }), 201
    
    except Exception as e:
        return jsonify({'error': f'Failed to create challenge: {str(e)}'}), 500


@challenges_bp.route('/<int:challenge_id>', methods=['GET'])
@jwt_required()
def get_challenge(user, challenge_id):
    """
    Get challenge details
    GET /api/challenges/<id>
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get challenge
        challenge, error = ChallengeService.get_challenge_by_id(challenge_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        # Verify challenge belongs to user
        if challenge['user_id'] != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get challenge performance
        performance, perf_error = ChallengeService.get_challenge_performance(challenge_id)
        
        # Check challenge rules
        rule_status = check_challenge_rules(challenge_id, db)
        
        return jsonify({
            'challenge': challenge,
            'performance': performance if not perf_error else {},
            'rule_status': rule_status
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get challenge: {str(e)}'}), 500


@challenges_bp.route('/<int:challenge_id>/status', methods=['PUT'])
@jwt_required()
def update_challenge_status(user, challenge_id):
    """
    Update challenge status
    PUT /api/challenges/<id>/status
    Headers: Authorization: Bearer <token>
    Body: {"status": "active|passed|failed|completed"}
    """
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Missing required field: status'}), 400
        
        # Get challenge to verify ownership
        challenge, error = ChallengeService.get_challenge_by_id(challenge_id)
        
        if error:
            return jsonify({'error': error}), 404
        
        if challenge['user_id'] != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update status
        updated_challenge, update_error = ChallengeService.update_challenge_status(
            challenge_id, 
            data['status']
        )
        
        if update_error:
            return jsonify({'error': update_error}), 400
        
        return jsonify({
            'message': 'Challenge status updated',
            'challenge': updated_challenge
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to update challenge: {str(e)}'}), 500


@challenges_bp.route('/plans', methods=['GET'])
def get_challenge_plans():
    """
    Get available challenge plans (no auth required)
    GET /api/challenges/plans
    """
    try:
        plans = []
        for plan_name, config in CHALLENGE_PLANS.items():
            plans.append({
                'name': plan_name,
                'initial_balance': config['initial_balance'],
                'profit_target': config['profit_target'],
                'profit_target_percentage': 10,
                'max_daily_loss': config['max_daily_loss'],
                'max_daily_loss_percentage': 5,
                'max_total_loss': config['max_total_loss'],
                'max_total_loss_percentage': 10
            })
        
        return jsonify({'plans': plans}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get plans: {str(e)}'}), 500
