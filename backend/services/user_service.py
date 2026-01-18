"""User service for user management operations"""

from models import db, User


class UserService:
    """Service class for user management operations"""
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            tuple: (user_dict, error_message)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "User not found"
            
            return user.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to get user: {str(e)}"
    
    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        
        Args:
            email (str): User email
            
        Returns:
            tuple: (user_dict, error_message)
        """
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                return None, "User not found"
            
            return user.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to get user: {str(e)}"
    
    @staticmethod
    def get_all_users(page=1, per_page=10):
        """
        Get all users with pagination
        
        Args:
            page (int): Page number
            per_page (int): Users per page
            
        Returns:
            tuple: (users_data, error_message)
        """
        try:
            pagination = User.query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            users = [user.to_dict() for user in pagination.items]
            
            return {
                'users': users,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }, None
            
        except Exception as e:
            return None, f"Failed to get users: {str(e)}"
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update user information
        
        Args:
            user_id (int): User ID
            **kwargs: Fields to update (email, full_name, is_admin, is_superadmin)
            
        Returns:
            tuple: (user_dict, error_message)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "User not found"
            
            # Update allowed fields
            allowed_fields = ['email', 'full_name', 'is_admin', 'is_superadmin']
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    setattr(user, field, value)
            
            db.session.commit()
            
            return user.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update user: {str(e)}"
    
    @staticmethod
    def update_password(user_id, current_password, new_password):
        """
        Update user password
        
        Args:
            user_id (int): User ID
            current_password (str): Current password
            new_password (str): New password
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            # Verify current password
            if not user.check_password(current_password):
                return False, "Current password is incorrect"
            
            # Set new password
            user.set_password(new_password)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update password: {str(e)}"
    
    @staticmethod
    def delete_user(user_id):
        """
        Delete user
        
        Args:
            user_id (int): User ID
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            db.session.delete(user)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete user: {str(e)}"
    
    @staticmethod
    def get_user_stats(user_id):
        """
        Get user statistics
        
        Args:
            user_id (int): User ID
            
        Returns:
            tuple: (stats_dict, error_message)
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None, "User not found"
            
            stats = {
                'total_challenges': len(user.challenges),
                'active_challenges': len([c for c in user.challenges if c.status == 'active']),
                'total_trades': len(user.trades),
                'open_trades': len([t for t in user.trades if t.status == 'open']),
                'total_payments': len(user.payments),
                'total_paid': sum(p.amount for p in user.payments if p.status == 'completed')
            }
            
            return stats, None
            
        except Exception as e:
            return None, f"Failed to get user stats: {str(e)}"
