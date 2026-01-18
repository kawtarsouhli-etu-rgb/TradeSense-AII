from app import app
from models import db, User, UserChallenge

def check_challenges():
    with app.app_context():
        # Trouver tous les utilisateurs
        users = User.query.all()
        
        for user in users:
            print(f"\nUtilisateur: {user.email}")
            print(f"ID: {user.id}")
            
            # Trouver tous les challenges pour cet utilisateur
            challenges = UserChallenge.query.filter_by(user_id=user.id).all()
            
            if not challenges:
                print("  ❌ Aucun challenge trouvé")
            else:
                for challenge in challenges:
                    print(f"  Challenge ID: {challenge.id}")
                    print(f"  Type: {challenge.plan_type}")
                    print(f"  Statut: {challenge.status}")
                    print(f"  Solde initial: {challenge.initial_balance}")
                    print(f"  Solde courant: {challenge.current_balance}")
                    print(f"  Date de création: {challenge.created_at}")
                    print("---")

if __name__ == '__main__':
    check_challenges()