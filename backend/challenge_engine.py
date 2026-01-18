"""
Challenge Engine - Core Business Logic
Handles challenge evaluation based on trading rules
"""

from datetime import datetime, timedelta
from models import db, UserChallenge, Trade


def evaluate_challenge(challenge_id):
    """
    Evaluate challenge status based on business rules:
    - MAX DAILY LOSS = 5% of starting balance
    - MAX TOTAL LOSS = 10% of starting balance  
    - PROFIT TARGET = +10% of starting balance
    
    Args:
        challenge_id (int): Challenge ID to evaluate
        
    Returns:
        dict: Challenge evaluation result with status and metrics
    """
    challenge = UserChallenge.query.get(challenge_id)
    
    if not challenge:
        return {
            'success': False,
            'error': 'Challenge not found'
        }
    
    # Skip if already finalized
    if challenge.status in ['PASSED', 'FAILED']:
        return {
            'success': True,
            'status': challenge.status,
            'balance': challenge.current_balance,
            'message': f'Challenge already {challenge.status}'
        }
    
    starting_balance = challenge.initial_balance
    current_balance = challenge.current_balance
    
    # Calculate total profit/loss
    total_pnl = current_balance - starting_balance
    total_pnl_pct = (total_pnl / starting_balance) * 100
    
    # Check Rule 1: PROFIT TARGET (+10%)
    if total_pnl_pct >= 10.0:
        challenge.status = 'PASSED'
        db.session.commit()
        return {
            'success': True,
            'status': 'PASSED',
            'balance': current_balance,
            'total_pnl': round(total_pnl, 2),
            'total_pnl_pct': round(total_pnl_pct, 2),
            'message': 'Profit target reached! Challenge PASSED'
        }
    
    # Check Rule 2: MAX TOTAL LOSS (10%)
    if total_pnl <= -(starting_balance * 0.10):
        challenge.status = 'FAILED'
        db.session.commit()
        return {
            'success': True,
            'status': 'FAILED',
            'balance': current_balance,
            'total_pnl': round(total_pnl, 2),
            'total_pnl_pct': round(total_pnl_pct, 2),
            'message': 'Max total loss (10%) exceeded. Challenge FAILED'
        }
    
    # Check Rule 3: MAX DAILY LOSS (5%)
    daily_pnl = calculate_daily_pnl(challenge_id)
    max_daily_loss = starting_balance * 0.05
    
    if daily_pnl <= -max_daily_loss:
        challenge.status = 'FAILED'
        db.session.commit()
        daily_pnl_pct = (daily_pnl / starting_balance) * 100
        return {
            'success': True,
            'status': 'FAILED',
            'balance': current_balance,
            'daily_pnl': round(daily_pnl, 2),
            'daily_pnl_pct': round(daily_pnl_pct, 2),
            'message': 'Max daily loss (5%) exceeded. Challenge FAILED'
        }
    
    # Challenge still ACTIVE
    daily_pnl_pct = (daily_pnl / starting_balance) * 100
    
    return {
        'success': True,
        'status': 'ACTIVE',
        'balance': current_balance,
        'total_pnl': round(total_pnl, 2),
        'total_pnl_pct': round(total_pnl_pct, 2),
        'daily_pnl': round(daily_pnl, 2),
        'daily_pnl_pct': round(daily_pnl_pct, 2),
        'message': 'Challenge is active'
    }


def calculate_daily_pnl(challenge_id):
    """
    Calculate profit/loss for today's trades only
    Daily loss resets every new day (uses UTC timestamps)
    
    Args:
        challenge_id (int): Challenge ID
        
    Returns:
        float: Total P&L for today
    """
    # Get start of today (UTC)
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get all trades from today
    today_trades = Trade.query.filter(
        Trade.challenge_id == challenge_id,
        Trade.created_at >= today_start
    ).all()
    
    if not today_trades:
        return 0.0
    
    # Sum up profit/loss from today's trades
    daily_pnl = sum(trade.profit_loss for trade in today_trades)
    
    return daily_pnl


def get_challenge_metrics(challenge_id):
    """
    Get detailed challenge metrics
    
    Args:
        challenge_id (int): Challenge ID
        
    Returns:
        dict: Detailed metrics
    """
    challenge = UserChallenge.query.get(challenge_id)
    
    if not challenge:
        return None
    
    starting_balance = challenge.initial_balance
    current_balance = challenge.current_balance
    total_pnl = current_balance - starting_balance
    total_pnl_pct = (total_pnl / starting_balance) * 100
    
    daily_pnl = calculate_daily_pnl(challenge_id)
    daily_pnl_pct = (daily_pnl / starting_balance) * 100
    
    # Calculate remaining allowances
    max_total_loss_amount = starting_balance * 0.10
    remaining_total_loss = max_total_loss_amount + total_pnl
    
    max_daily_loss_amount = starting_balance * 0.05
    remaining_daily_loss = max_daily_loss_amount + daily_pnl
    
    profit_target_amount = starting_balance * 0.10
    remaining_to_target = profit_target_amount - total_pnl
    
    return {
        'challenge_id': challenge_id,
        'status': challenge.status,
        'balance': {
            'starting': starting_balance,
            'current': current_balance,
        },
        'total': {
            'pnl': round(total_pnl, 2),
            'pnl_pct': round(total_pnl_pct, 2),
            'max_loss_allowed': max_total_loss_amount,
            'remaining_loss_buffer': round(remaining_total_loss, 2)
        },
        'daily': {
            'pnl': round(daily_pnl, 2),
            'pnl_pct': round(daily_pnl_pct, 2),
            'max_loss_allowed': max_daily_loss_amount,
            'remaining_loss_buffer': round(remaining_daily_loss, 2)
        },
        'target': {
            'profit_needed': round(remaining_to_target, 2),
            'profit_target': profit_target_amount,
            'progress_pct': round((total_pnl / profit_target_amount) * 100, 2) if profit_target_amount > 0 else 0
        }
    }
