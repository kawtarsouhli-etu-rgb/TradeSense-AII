"""Authentication service for user login, registration, and token management"""

import jwt
from datetime import datetime, timedelta
from flask import current_app
from models import db, User


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def register_user(email, password, full_name):
        """
        Register a new user
        
        Args:
            email (str): User email
            password (str): User password
            full_name (str): User full name
            
        Returns:
            tuple: (user_dict, error_message)
        """
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return None, "Email already registered"
            
            # Create new user
            user = User(
                email=email,
                full_name=full_name
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return user.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(email, password):
        """
        Authenticate user and generate tokens
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            tuple: (token_data, error_message)
        """
        try:
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            if not user or not user.check_password(password):
                return None, "Invalid email or password"
            
            # Generate tokens
            access_token = AuthService.generate_access_token(user)
            refresh_token = AuthService.generate_refresh_token(user)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }, None
            
        except Exception as e:
            return None, f"Login failed: {str(e)}"
    
    @staticmethod
    def generate_access_token(user):
        """
        Generate JWT access token
        
        Args:
            user (User): User object
            
        Returns:
            str: JWT access token
        """
        payload = {
            'user_id': user.id,
            'email': user.email,
            'is_admin': user.is_admin,
            'is_superadmin': user.is_superadmin,
            'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
        
        return token
    
    @staticmethod
    def generate_refresh_token(user):
        """
        Generate JWT refresh token
        
        Args:
            user (User): User object
            
        Returns:
            str: JWT refresh token
        """
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + current_app.config['JWT_REFRESH_TOKEN_EXPIRES'],
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        token = jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
        
        return token
    
    @staticmethod
    def verify_token(token):
        """
        Verify and decode JWT token
        
        Args:
            token (str): JWT token
            
        Returns:
            tuple: (payload, error_message)
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            return payload, None
            
        except jwt.ExpiredSignatureError:
            return None, "Token has expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"
        except Exception as e:
            return None, f"Token verification failed: {str(e)}"
    
    @staticmethod
    def refresh_access_token(refresh_token):
        """
        Generate new access token using refresh token
        
        Args:
            refresh_token (str): JWT refresh token
            
        Returns:
            tuple: (new_access_token, error_message)
        """
        payload, error = AuthService.verify_token(refresh_token)
        
        if error:
            return None, error
        
        if payload.get('type') != 'refresh':
            return None, "Invalid token type"
        
        # Get user
        user = User.query.get(payload['user_id'])
        if not user:
            return None, "User not found"
        
        # Generate new access token
        new_access_token = AuthService.generate_access_token(user)
        
        return new_access_token, None
    
    @staticmethod
    def get_current_user(token):
        """
        Get current user from token
        
        Args:
            token (str): JWT access token
            
        Returns:
            tuple: (user, error_message)
        """
        payload, error = AuthService.verify_token(token)
        
        if error:
            return None, error
        
        user = User.query.get(payload['user_id'])
        if not user:
            return None, "User not found"
        
        return user, None
