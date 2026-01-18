"""Leaderboard routes"""

from flask import Blueprint, jsonify
from models import UserChallenge, User
from sqlalchemy import desc

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/api/leaderboard')


@leaderboard_bp.route('', methods=['GET'])
def get_leaderboard():
    """
    Get top 10 traders by profit percentage
    GET /api/leaderboard
    """
    try:
        # Get all active or funded challenges
        challenges = UserChallenge.query.filter(
            UserChallenge.status.in_(['active', 'funded'])
        ).all()
        
        # Calculate profit percentage for each challenge
        leaderboard_data = []
        
        for challenge in challenges:
            # Get user info
            user = User.query.get(challenge.user_id)
            if not user:
                continue
            
            # Calculate profit/loss percentage
            profit_loss = challenge.current_balance - challenge.initial_balance
            profit_percentage = (profit_loss / challenge.initial_balance) * 100
            
            # Calculate win rate
            total_trades = len(challenge.trades)
            closed_trades = [t for t in challenge.trades if t.status == 'closed']
            winning_trades = [t for t in closed_trades if t.profit_loss > 0]
            win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
            
            leaderboard_data.append({
                'rank': 0,  # Will be set after sorting
                'user': {
                    'id': user.id,
                    'full_name': user.full_name,
                    'email': user.email
                },
                'challenge': {
                    'id': challenge.id,
                    'plan_type': challenge.plan_type,
                    'status': challenge.status,
                    'initial_balance': challenge.initial_balance,
                    'current_balance': challenge.current_balance,
                    'created_at': challenge.created_at.isoformat()
                },
                'performance': {
                    'profit_loss': round(profit_loss, 2),
                    'profit_percentage': round(profit_percentage, 2),
                    'total_trades': total_trades,
                    'winning_trades': len(winning_trades),
                    'win_rate': round(win_rate, 2)
                }
            })
        
        # Sort by profit percentage (descending) and get top 10
        leaderboard_data.sort(key=lambda x: x['performance']['profit_percentage'], reverse=True)
        top_10 = leaderboard_data[:10]
        
        # Assign ranks
        for i, entry in enumerate(top_10, start=1):
            entry['rank'] = i
        
        return jsonify({
            'leaderboard': top_10,
            'total_traders': len(leaderboard_data)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get leaderboard: {str(e)}'}), 500


@leaderboard_bp.route('/top-performer', methods=['GET'])
def get_top_performer():
    """
    Get the top performing trader
    GET /api/leaderboard/top-performer
    """
    try:
        # Get all active or funded challenges
        challenges = UserChallenge.query.filter(
            UserChallenge.status.in_(['active', 'funded'])
        ).all()
        
        if not challenges:
            return jsonify({
                'message': 'No active challenges found',
                'top_performer': None
            }), 200
        
        # Find challenge with highest profit percentage
        best_challenge = None
        best_profit_pct = float('-inf')
        
        for challenge in challenges:
            profit_loss = challenge.current_balance - challenge.initial_balance
            profit_percentage = (profit_loss / challenge.initial_balance) * 100
            
            if profit_percentage > best_profit_pct:
                best_profit_pct = profit_percentage
                best_challenge = challenge
        
        if not best_challenge:
            return jsonify({
                'message': 'No top performer found',
                'top_performer': None
            }), 200
        
        # Get user info
        user = User.query.get(best_challenge.user_id)
        
        # Calculate stats
        profit_loss = best_challenge.current_balance - best_challenge.initial_balance
        total_trades = len(best_challenge.trades)
        closed_trades = [t for t in best_challenge.trades if t.status == 'closed']
        winning_trades = [t for t in closed_trades if t.profit_loss > 0]
        win_rate = (len(winning_trades) / len(closed_trades) * 100) if closed_trades else 0
        
        top_performer = {
            'user': {
                'id': user.id,
                'full_name': user.full_name
            },
            'challenge': {
                'id': best_challenge.id,
                'plan_type': best_challenge.plan_type,
                'status': best_challenge.status,
                'initial_balance': best_challenge.initial_balance,
                'current_balance': best_challenge.current_balance
            },
            'performance': {
                'profit_loss': round(profit_loss, 2),
                'profit_percentage': round(best_profit_pct, 2),
                'total_trades': total_trades,
                'winning_trades': len(winning_trades),
                'win_rate': round(win_rate, 2)
            }
        }
        
        return jsonify({
            'top_performer': top_performer
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get top performer: {str(e)}'}), 500
