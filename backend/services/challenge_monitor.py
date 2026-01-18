"""Challenge monitoring service for rule validation"""

from datetime import datetime, timedelta
from models import UserChallenge, Trade


def check_challenge_rules(challenge_id, db):
    """
    Check and enforce challenge rules
    
    Verifies:
    - Daily loss > 5% → status='failed'
    - Total loss > 10% → status='failed'
    - Profit > 10% → status='funded'
    
    Args:
        challenge_id (int): Challenge ID
        db: SQLAlchemy database instance
        
    Returns:
        dict: {"status": str, "reason": str}
    """
    try:
        # Get challenge
        challenge = UserChallenge.query.get(challenge_id)
        
        if not challenge:
            return {
                "status": "error",
                "reason": "Challenge not found"
            }
        
        # Skip if challenge is already completed or failed
        if challenge.status in ['failed', 'funded', 'completed']:
            return {
                "status": challenge.status,
                "reason": "Challenge already finalized"
            }
        
        initial_balance = challenge.initial_balance
        current_balance = challenge.current_balance
        
        # Calculate total profit/loss
        total_profit_loss = current_balance - initial_balance
        total_profit_loss_pct = (total_profit_loss / initial_balance) * 100
        
        # Check Rule 1: Total loss > 10% → failed
        if total_profit_loss_pct <= -10:
            challenge.status = 'failed'
            db.session.commit()
            return {
                "status": "failed",
                "reason": f"Total loss exceeds 10% ({total_profit_loss_pct:.2f}%)"
            }
        
        # Check Rule 2: Profit > 10% → funded
        if total_profit_loss_pct >= 10:
            challenge.status = 'funded'
            db.session.commit()
            return {
                "status": "funded",
                "reason": f"Profit target reached ({total_profit_loss_pct:.2f}%)"
            }
        
        # Check Rule 3: Daily loss > 5% → failed
        daily_loss_pct = _check_daily_loss(challenge)
        if daily_loss_pct <= -5:
            challenge.status = 'failed'
            db.session.commit()
            return {
                "status": "failed",
                "reason": f"Daily loss exceeds 5% ({daily_loss_pct:.2f}%)"
            }
        
        # All rules passed, challenge remains active
        return {
            "status": "active",
            "reason": "All rules satisfied",
            "metrics": {
                "total_profit_loss_pct": round(total_profit_loss_pct, 2),
                "daily_loss_pct": round(daily_loss_pct, 2)
            }
        }
    
    except Exception as e:
        return {
            "status": "error",
            "reason": f"Error checking challenge rules: {str(e)}"
        }


def _check_daily_loss(challenge):
    """
    Calculate daily loss percentage for a challenge
    
    Args:
        challenge (UserChallenge): Challenge object
        
    Returns:
        float: Daily loss percentage
    """
    try:
        # Get trades from today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        today_trades = Trade.query.filter(
            Trade.challenge_id == challenge.id,
            Trade.created_at >= today_start,
            Trade.status == 'closed'
        ).all()
        
        if not today_trades:
            return 0.0
        
        # Calculate total profit/loss for today
        daily_profit_loss = sum(trade.profit_loss for trade in today_trades)
        
        # Calculate percentage based on initial balance
        daily_loss_pct = (daily_profit_loss / challenge.initial_balance) * 100
        
        return daily_loss_pct
    
    except Exception as e:
        return 0.0
