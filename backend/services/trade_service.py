"""Trade service for trade management and execution"""

from datetime import datetime
from models import db, Trade, UserChallenge


class TradeService:
    """Service class for trade management operations"""
    
    @staticmethod
    def create_trade(challenge_id, user_id, symbol, trade_type, quantity, entry_price):
        """
        Create a new trade
        
        Args:
            challenge_id (int): Challenge ID
            user_id (int): User ID
            symbol (str): Trading symbol (e.g., AAPL, GOOGL)
            trade_type (str): Trade type (buy or sell)
            quantity (float): Trade quantity
            entry_price (float): Entry price
            
        Returns:
            tuple: (trade_dict, error_message)
        """
        try:
            # Verify challenge exists and is active
            challenge = UserChallenge.query.get(challenge_id)
            if not challenge:
                return None, "Challenge not found"
            
            if challenge.status != 'active':
                return None, "Challenge is not active"
            
            if challenge.user_id != user_id:
                return None, "Challenge does not belong to this user"
            
            # Validate trade type
            if trade_type.lower() not in ['buy', 'sell']:
                return None, "Invalid trade type. Must be 'buy' or 'sell'"
            
            # Create trade
            trade = Trade(
                challenge_id=challenge_id,
                user_id=user_id,
                symbol=symbol.upper(),
                trade_type=trade_type.lower(),
                quantity=quantity,
                entry_price=entry_price,
                status='open'
            )
            
            db.session.add(trade)
            db.session.commit()
            
            return trade.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create trade: {str(e)}"
    
    @staticmethod
    def get_trade_by_id(trade_id):
        """
        Get trade by ID
        
        Args:
            trade_id (int): Trade ID
            
        Returns:
            tuple: (trade_dict, error_message)
        """
        try:
            trade = Trade.query.get(trade_id)
            if not trade:
                return None, "Trade not found"
            
            return trade.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to get trade: {str(e)}"
    
    @staticmethod
    def get_user_trades(user_id, status=None):
        """
        Get all trades for a user
        
        Args:
            user_id (int): User ID
            status (str, optional): Filter by status (open or closed)
            
        Returns:
            tuple: (trades_list, error_message)
        """
        try:
            query = Trade.query.filter_by(user_id=user_id)
            
            if status:
                query = query.filter_by(status=status)
            
            trades = query.order_by(Trade.created_at.desc()).all()
            
            return [trade.to_dict() for trade in trades], None
            
        except Exception as e:
            return None, f"Failed to get trades: {str(e)}"
    
    @staticmethod
    def get_challenge_trades(challenge_id, status=None):
        """
        Get all trades for a challenge
        
        Args:
            challenge_id (int): Challenge ID
            status (str, optional): Filter by status
            
        Returns:
            tuple: (trades_list, error_message)
        """
        try:
            query = Trade.query.filter_by(challenge_id=challenge_id)
            
            if status:
                query = query.filter_by(status=status)
            
            trades = query.order_by(Trade.created_at.desc()).all()
            
            return [trade.to_dict() for trade in trades], None
            
        except Exception as e:
            return None, f"Failed to get challenge trades: {str(e)}"
    
    @staticmethod
    def close_trade(trade_id, exit_price):
        """
        Close an open trade
        
        Args:
            trade_id (int): Trade ID
            exit_price (float): Exit price
            
        Returns:
            tuple: (trade_dict, error_message)
        """
        try:
            trade = Trade.query.get(trade_id)
            if not trade:
                return None, "Trade not found"
            
            if trade.status != 'open':
                return None, "Trade is already closed"
            
            # Calculate profit/loss
            if trade.trade_type == 'buy':
                profit_loss = (exit_price - trade.entry_price) * trade.quantity
            else:  # sell
                profit_loss = (trade.entry_price - exit_price) * trade.quantity
            
            # Update trade
            trade.exit_price = exit_price
            trade.profit_loss = profit_loss
            trade.status = 'closed'
            
            # Update challenge balance
            challenge = UserChallenge.query.get(trade.challenge_id)
            if challenge:
                challenge.current_balance += profit_loss
                TradeService._check_challenge_limits(challenge)
            
            db.session.commit()
            
            return trade.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to close trade: {str(e)}"
    
    @staticmethod
    def update_trade(trade_id, **kwargs):
        """
        Update trade information
        
        Args:
            trade_id (int): Trade ID
            **kwargs: Fields to update
            
        Returns:
            tuple: (trade_dict, error_message)
        """
        try:
            trade = Trade.query.get(trade_id)
            if not trade:
                return None, "Trade not found"
            
            # Update allowed fields
            allowed_fields = ['symbol', 'quantity', 'entry_price', 'exit_price', 'profit_loss', 'status']
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    setattr(trade, field, value)
            
            db.session.commit()
            
            return trade.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update trade: {str(e)}"
    
    @staticmethod
    def delete_trade(trade_id):
        """
        Delete trade
        
        Args:
            trade_id (int): Trade ID
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            trade = Trade.query.get(trade_id)
            if not trade:
                return False, "Trade not found"
            
            db.session.delete(trade)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete trade: {str(e)}"
    
    @staticmethod
    def get_trade_statistics(user_id=None, challenge_id=None):
        """
        Get trade statistics
        
        Args:
            user_id (int, optional): Filter by user ID
            challenge_id (int, optional): Filter by challenge ID
            
        Returns:
            tuple: (statistics_dict, error_message)
        """
        try:
            query = Trade.query
            
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            if challenge_id:
                query = query.filter_by(challenge_id=challenge_id)
            
            trades = query.all()
            
            if not trades:
                return {
                    'total_trades': 0,
                    'open_trades': 0,
                    'closed_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'total_profit_loss': 0,
                    'average_profit_loss': 0,
                    'win_rate': 0
                }, None
            
            closed_trades = [t for t in trades if t.status == 'closed']
            winning_trades = [t for t in closed_trades if t.profit_loss > 0]
            losing_trades = [t for t in closed_trades if t.profit_loss < 0]
            
            total_profit_loss = sum(t.profit_loss for t in closed_trades)
            average_profit_loss = total_profit_loss / len(closed_trades) if closed_trades else 0
            win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
            
            statistics = {
                'total_trades': len(trades),
                'open_trades': len([t for t in trades if t.status == 'open']),
                'closed_trades': len(closed_trades),
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'total_profit_loss': round(total_profit_loss, 2),
                'average_profit_loss': round(average_profit_loss, 2),
                'win_rate': round(win_rate, 2)
            }
            
            return statistics, None
            
        except Exception as e:
            return None, f"Failed to get trade statistics: {str(e)}"
    
    @staticmethod
    def _check_challenge_limits(challenge):
        """
        Internal method to check if challenge has exceeded loss limits
        
        Args:
            challenge (UserChallenge): Challenge object
        """
        profit_loss = challenge.current_balance - challenge.initial_balance
        
        # Check if max total loss is exceeded
        if abs(profit_loss) >= challenge.max_total_loss:
            challenge.status = 'failed'
