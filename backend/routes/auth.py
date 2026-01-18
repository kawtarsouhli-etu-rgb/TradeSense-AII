"""Authentication routes"""

from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.user_service import UserService
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def jwt_required():
    """Decorator to protect routes with JWT authentication"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Get token from Authorization header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(' ')[1]  # Bearer <token>
                except IndexError:
                    return jsonify({'error': 'Invalid token format'}), 401
            
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            
            # Verify token
            user, error = AuthService.get_current_user(token)
            if error:
                return jsonify({'error': error}), 401
            
            # Pass user to the route
            return f(user, *args, **kwargs)
        
        return decorated_function
    return decorator


def superadmin_required():
    """Decorator to protect routes with SuperAdmin access"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(user, *args, **kwargs):
            # Check if user is superadmin
            if not getattr(user, 'is_superadmin', False):
                return jsonify({'error': 'SuperAdmin access required'}), 403
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: {"email": "user@example.com", "password": "pass123", "full_name": "John Doe"}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['email', 'password', 'full_name']):
            return jsonify({'error': 'Missing required fields: email, password, full_name'}), 400
        
        email = data['email']
        password = data['password']
        full_name = data['full_name']
        
        # Register user
        user, error = AuthService.register_user(email, password, full_name)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user
        }), 201
    
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token
    POST /api/auth/login
    Body: {"email": "user@example.com", "password": "pass123"}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing required fields: email, password'}), 400
        
        email = data['email']
        password = data['password']
        
        # Login user
        token_data, error = AuthService.login_user(email, password)
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'message': 'Login successful',
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'user': token_data['user']
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user(user):
    """
    Get current user information (JWT protected)
    GET /api/auth/me
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get user statistics
        stats, error = UserService.get_user_stats(user.id)
        
        user_data = user.to_dict()
        if not error:
            user_data['stats'] = stats
        
        return jsonify({
            'user': user_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get user info: {str(e)}'}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """
    Refresh access token using refresh token
    POST /api/auth/refresh
    Body: {"refresh_token": "..."}
    """
    try:
        data = request.get_json()
        
        if not data or 'refresh_token' not in data:
            return jsonify({'error': 'Missing refresh token'}), 400
        
        refresh_token = data['refresh_token']
        
        # Generate new access token
        new_access_token, error = AuthService.refresh_access_token(refresh_token)
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify({
            'access_token': new_access_token
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500
