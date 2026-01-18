from app import app, db
from models import User, PayPalSettings
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Créer toutes les tables
        db.create_all()
        
        # Créer l'utilisateur administrateur par défaut
        admin_exists = User.query.filter_by(email='admin@tradesense.ai').first()
        if not admin_exists:
            admin_user = User(
                full_name='Admin User',
                email='admin@tradesense.ai',
                is_admin=True,
                is_superadmin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("Admin user created: admin@tradesense.ai / admin123")
        
        # Créer l'utilisateur standard par défaut
        user_exists = User.query.filter_by(email='user@tradesense.ai').first()
        if not user_exists:
            user = User(
                full_name='Regular User',
                email='user@tradesense.ai',
                is_admin=False,
                is_superadmin=False
            )
            user.set_password('user123')
            db.session.add(user)
            print("Regular user created: user@tradesense.ai / user123")
        
        # Créer les paramètres PayPal par défaut
        paypal_settings_exists = PayPalSettings.query.first()
        if not paypal_settings_exists:
            paypal_settings = PayPalSettings(
                mode='sandbox',
                client_id='sb',
                client_secret='your-fake-paypal-secret',
                is_active=True,
                updated_by=None
            )
            db.session.add(paypal_settings)
            print("PayPal settings created")
        
        db.session.commit()
        print("\nBase de données MySQL initialisée avec succès!")
        print("Schéma: EXAM")
        print("Utilisateurs créés:")
        print("- admin@tradesense.ai (admin)")
        print("- user@tradesense.ai (user)")

if __name__ == "__main__":
    init_database()