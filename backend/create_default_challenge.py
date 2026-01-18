from app import app
from models import db, User, UserChallenge, Payment
from datetime import datetime, timedelta

def create_default_challenge():
    with app.app_context():
        # Trouver l'utilisateur admin
        admin_user = User.query.filter_by(email='admin@tradesense.ai').first()
        
        if not admin_user:
            print("Admin user not found!")
            return
        
        # Vérifier si un challenge existe déjà pour cet utilisateur
        existing_challenge = UserChallenge.query.filter_by(user_id=admin_user.id).first()
        
        if existing_challenge:
            print("User already has a challenge!")
            return
        
        # Créer un challenge de démonstration pour l'utilisateur
        
        # Créer un challenge pour l'utilisateur admin
        demo_challenge = UserChallenge(
            user_id=admin_user.id,
            plan_type='demo',
            status='ACTIVE',
            initial_balance=10000.0,  # 10,000 DH ou USD
            current_balance=10000.0,
            profit_target=1000.0,  # 10% de profit cible
            max_daily_loss=500.0,   # 5% de perte quotidienne max
            max_total_loss=1000.0,  # 10% de perte totale max
            created_at=datetime.utcnow()
        )
        
        db.session.add(demo_challenge)
        db.session.commit()
        
        print(f"Démo challenge créé pour l'utilisateur {admin_user.email}")
        print(f"Challenge ID: {demo_challenge.id}")
        print(f"Solde initial: {demo_challenge.initial_balance}")

if __name__ == '__main__':
    create_default_challenge()