"""Challenge service for trading challenge management"""

from models import db, UserChallenge


class ChallengeService:
    """Service class for challenge management operations"""
    
    @staticmethod
    def create_challenge(user_id, plan_type, initial_balance, profit_target, max_daily_loss, max_total_loss):
        """
        Create a new trading challenge
        
        Args:
            user_id (int): User ID
            plan_type (str): Type of plan (basic, pro, elite)
            initial_balance (float): Starting balance
            profit_target (float): Profit target amount
            max_daily_loss (float): Maximum daily loss allowed
            max_total_loss (float): Maximum total loss allowed
            
        Returns:
            tuple: (challenge_dict, error_message)
        """
        try:
            challenge = UserChallenge(
                user_id=user_id,
                plan_type=plan_type,
                initial_balance=initial_balance,
                current_balance=initial_balance,
                profit_target=profit_target,
                max_daily_loss=max_daily_loss,
                max_total_loss=max_total_loss,
                status='active'
            )
            
            db.session.add(challenge)
            db.session.commit()
            
            return challenge.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create challenge: {str(e)}"
    
    @staticmethod
    def get_challenge_by_id(challenge_id):
        """
        Get challenge by ID
        
        Args:
            challenge_id (int): Challenge ID
            
        Returns:
            tuple: (challenge_dict, error_message)
        """
        try:
            challenge = UserChallenge.query.get(challenge_id)
            if not challenge:
                return None, "Challenge not found"
            
            return challenge.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to get challenge: {str(e)}"
    
    @staticmethod
    def get_user_challenges(user_id, status=None):
        """
        Get all challenges for a user
        
        Args:
            user_id (int): User ID
            status (str, optional): Filter by status
            
        Returns:
            tuple: (challenges_list, error_message)
        """
        try:
            query = UserChallenge.query.filter_by(user_id=user_id)
            
            if status:
                query = query.filter_by(status=status)
            
            challenges = query.order_by(UserChallenge.created_at.desc()).all()
            
            return [challenge.to_dict() for challenge in challenges], None
            
        except Exception as e:
            return None, f"Failed to get challenges: {str(e)}"
    
    @staticmethod
    def get_all_challenges(page=1, per_page=10, status=None):
        """
        Get all challenges with pagination
        
        Args:
            page (int): Page number
            per_page (int): Challenges per page
            status (str, optional): Filter by status
            
        Returns:
            tuple: (challenges_data, error_message)
        """
        try:
            query = UserChallenge.query
            
            if status:
                query = query.filter_by(status=status)
            
            pagination = query.order_by(UserChallenge.created_at.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            challenges = [challenge.to_dict() for challenge in pagination.items]
            
            return {
                'challenges': challenges,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }, None
            
        except Exception as e:
            return None, f"Failed to get challenges: {str(e)}"
    
    @staticmethod
    def update_challenge_balance(challenge_id, new_balance):
        """
        Update challenge balance
        
        Args:
            challenge_id (int): Challenge ID
            new_balance (float): New balance amount
            
        Returns:
            tuple: (challenge_dict, error_message)
        """
        try:
            challenge = UserChallenge.query.get(challenge_id)
            if not challenge:
                return None, "Challenge not found"
            
            challenge.current_balance = new_balance
            
            # Check if challenge objectives are met or violated
            ChallengeService._check_challenge_status(challenge)
            
            db.session.commit()
            
            return challenge.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update challenge balance: {str(e)}"
    
    @staticmethod
    def update_challenge_status(challenge_id, status):
        """
        Update challenge status
        
        Args:
            challenge_id (int): Challenge ID
            status (str): New status (active, passed, failed, completed)
            
        Returns:
            tuple: (challenge_dict, error_message)
        """
        try:
            challenge = UserChallenge.query.get(challenge_id)
            if not challenge:
                return None, "Challenge not found"
            
            valid_statuses = ['active', 'passed', 'failed', 'completed']
            if status not in valid_statuses:
                return None, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            
            challenge.status = status
            db.session.commit()
            
            return challenge.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update challenge status: {str(e)}"
    
    @staticmethod
    def delete_challenge(challenge_id):
        """
        Delete challenge
        
        Args:
            challenge_id (int): Challenge ID
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            challenge = UserChallenge.query.get(challenge_id)
            if not challenge:
                return False, "Challenge not found"
            
            db.session.delete(challenge)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete challenge: {str(e)}"
    
    @staticmethod
    def get_challenge_performance(challenge_id):
        """
        Get challenge performance metrics
        
        Args:
            challenge_id (int): Challenge ID
            
        Returns:
            tuple: (performance_dict, error_message)
        """
        try:
            challenge = UserChallenge.query.get(challenge_id)
            if not challenge:
                return None, "Challenge not found"
            
            profit_loss = challenge.current_balance - challenge.initial_balance
            profit_loss_percentage = (profit_loss / challenge.initial_balance) * 100
            progress_to_target = (profit_loss / challenge.profit_target) * 100 if challenge.profit_target > 0 else 0
            
            performance = {
                'challenge_id': challenge_id,
                'initial_balance': challenge.initial_balance,
                'current_balance': challenge.current_balance,
                'profit_loss': profit_loss,
                'profit_loss_percentage': round(profit_loss_percentage, 2),
                'profit_target': challenge.profit_target,
                'progress_to_target': round(progress_to_target, 2),
                'total_trades': len(challenge.trades),
                'winning_trades': len([t for t in challenge.trades if t.profit_loss > 0]),
                'losing_trades': len([t for t in challenge.trades if t.profit_loss < 0]),
                'status': challenge.status
            }
            
            return performance, None
            
        except Exception as e:
            return None, f"Failed to get challenge performance: {str(e)}"
    
    @staticmethod
    def _check_challenge_status(challenge):
        """
        Internal method to check and update challenge status based on performance
        
        Args:
            challenge (UserChallenge): Challenge object
        """
        profit_loss = challenge.current_balance - challenge.initial_balance
        
        # Check if profit target is reached
        if profit_loss >= challenge.profit_target:
            challenge.status = 'passed'
        
        # Check if max total loss is exceeded
        elif abs(profit_loss) >= challenge.max_total_loss:
            challenge.status = 'failed'
