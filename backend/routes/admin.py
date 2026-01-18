"""Admin panel routes"""

from flask import Blueprint, request, jsonify
from routes.auth import jwt_required, superadmin_required
from models import db, User, UserChallenge, PayPalSettings

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
@superadmin_required()
def get_all_users(user):
    """
    Get all users
    GET /api/admin/users
    Headers: Authorization: Bearer <admin_token>
    """
    try:
        # Get query parameters for pagination/filtering
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        
        # Build query
        query = User.query
        
        if search:
            query = query.filter(
                db.or_(
                    User.email.contains(search),
                    User.full_name.contains(search)
                )
            )
        
        # Paginate results
        users = query.paginate(
            page=page, 
            per_page=min(per_page, 100),  # Max 100 per page
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get users: {str(e)}'}), 500


@admin_bp.route('/challenges', methods=['GET'])
@superadmin_required()
def get_all_challenges(user):
    """
    Get all challenges
    GET /api/admin/challenges
    Headers: Authorization: Bearer <admin_token>
    """
    try:
        # Get query parameters for pagination/filtering
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', '', type=str)
        user_id = request.args.get('user_id', type=int)
        
        # Build query
        query = UserChallenge.query
        
        if status:
            query = query.filter(UserChallenge.status == status.upper())
        
        if user_id:
            query = query.filter(UserChallenge.user_id == user_id)
        
        # Join with users to get user info
        query = query.join(User, UserChallenge.user_id == User.id)
        
        # Paginate results
        challenges = query.paginate(
            page=page, 
            per_page=min(per_page, 100),  # Max 100 per page
            error_out=False
        )
        
        # Prepare response with user info
        challenge_list = []
        for challenge in challenges.items:
            challenge_dict = challenge.to_dict()
            challenge_dict['user'] = {
                'id': challenge.user.id,
                'email': challenge.user.email,
                'full_name': challenge.user.full_name
            }
            challenge_list.append(challenge_dict)
        
        return jsonify({
            'challenges': challenge_list,
            'total': challenges.total,
            'pages': challenges.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get challenges: {str(e)}'}), 500


@admin_bp.route('/challenges/<int:challenge_id>/status', methods=['PUT'])
@superadmin_required()
def update_challenge_status(user, challenge_id):
    """
    Manually update challenge status
    PUT /api/admin/challenges/<id>/status
    Headers: Authorization: Bearer <admin_token>
    Body: {"status": "PASSED" or "FAILED" or "ACTIVE"}
    """
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({'error': 'Status field is required'}), 400
        
        status = data['status'].upper()
        
        # Validate status
        valid_statuses = ['ACTIVE', 'PASSED', 'FAILED', 'COMPLETED']
        if status not in valid_statuses:
            return jsonify({'error': f'Invalid status. Valid options: {", ".join(valid_statuses)}'}), 400
        
        # Get challenge
        challenge = UserChallenge.query.get(challenge_id)
        if not challenge:
            return jsonify({'error': 'Challenge not found'}), 404
        
        # Update status
        old_status = challenge.status
        challenge.status = status
        challenge.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Challenge status updated from {old_status} to {status}',
            'challenge': challenge.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update challenge status: {str(e)}'}), 500


@admin_bp.route('/paypal/credentials', methods=['POST'])
@superadmin_required()
def update_paypal_credentials(user):
    """
    Update PayPal credentials
    POST /api/admin/paypal/credentials
    Headers: Authorization: Bearer <admin_token>
    Body: {
        "mode": "sandbox" or "live",
        "client_id": "...",
        "client_secret": "...",
        "is_active": true/false
    }
    """
    try:
        data = request.get_json()
        
        required_fields = ['mode', 'client_id', 'client_secret']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        # Validate mode
        mode = data['mode'].lower()
        if mode not in ['sandbox', 'live']:
            return jsonify({'error': 'Mode must be "sandbox" or "live"'}), 400
        
        # Get existing settings and deactivate them
        existing_settings = PayPalSettings.query.first()
        if existing_settings:
            existing_settings.is_active = False
        
        # Create new settings
        new_settings = PayPalSettings(
            mode=mode,
            client_id=data['client_id'],
            client_secret=data['client_secret'],
            is_active=data.get('is_active', True),
            updated_by=user.id
        )
        
        db.session.add(new_settings)
        db.session.commit()
        
        return jsonify({
            'message': 'PayPal credentials updated successfully',
            'settings': new_settings.to_dict(include_secret=False)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update PayPal credentials: {str(e)}'}), 500


@admin_bp.route('/paypal/credentials', methods=['GET'])
@superadmin_required()
def get_paypal_credentials(user):
    """
    Get current PayPal credentials
    GET /api/admin/paypal/credentials
    Headers: Authorization: Bearer <admin_token>
    """
    try:
        settings = PayPalSettings.query.first()
        
        if not settings:
            return jsonify({'settings': None}), 200
        
        return jsonify({
            'settings': settings.to_dict(include_secret=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get PayPal credentials: {str(e)}'}), 500


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@superadmin_required()
def delete_user(user, user_id):
    """
    Delete a user (soft delete by deactivation)
    DELETE /api/admin/users/<id>
    Headers: Authorization: Bearer <admin_token>
    """
    try:
        if user_id == user.id:
            return jsonify({'error': 'Cannot delete yourself'}), 400
        
        target_user = User.query.get(user_id)
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Soft delete by deactivating
        target_user.is_active = False
        target_user.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        
        return jsonify({
            'message': 'User deactivated successfully',
            'user': target_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500


@admin_bp.route('/stats', methods=['GET'])
@superadmin_required()
def get_platform_stats(user):
    """
    Get platform statistics
    GET /api/admin/stats
    Headers: Authorization: Bearer <admin_token>
    """
    try:
        from sqlalchemy import func
        
        # Get various statistics
        total_users = db.session.query(func.count(User.id)).scalar()
        active_users = db.session.query(func.count(User.id)).filter(User.is_active == True).scalar()
        total_challenges = db.session.query(func.count(UserChallenge.id)).scalar()
        active_challenges = db.session.query(func.count(UserChallenge.id)).filter(UserChallenge.status == 'ACTIVE').scalar()
        passed_challenges = db.session.query(func.count(UserChallenge.id)).filter(UserChallenge.status == 'PASSED').scalar()
        failed_challenges = db.session.query(func.count(UserChallenge.id)).filter(UserChallenge.status == 'FAILED').scalar()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'total_challenges': total_challenges,
                'active_challenges': active_challenges,
                'passed_challenges': passed_challenges,
                'failed_challenges': failed_challenges
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500