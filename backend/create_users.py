from app import app
from models import db, User

def create_default_users():
    with app.app_context():
        # Check if users already exist
        existing_users = User.query.all()
        if len(existing_users) == 0:
            # Create a default admin user
            admin_user = User(
                email='admin@tradesense.ai',
                full_name='Admin User',
                is_admin=True,
                is_superadmin=True
            )
            admin_user.set_password('admin123')
            
            # Create a regular user
            regular_user = User(
                email='user@tradesense.ai',
                full_name='Regular User'
            )
            regular_user.set_password('user123')
            
            db.session.add(admin_user)
            db.session.add(regular_user)
            db.session.commit()
            
            print("Default users created successfully!")
            print(f"Admin: admin@tradesense.ai / admin123")
            print(f"User: user@tradesense.ai / user123")
        else:
            print(f"{len(existing_users)} users already exist in the database.")
            print("Deleting existing users and creating default ones...")
            
            # Delete all existing users
            for user in existing_users:
                db.session.delete(user)
            
            # Create a default admin user
            admin_user = User(
                email='admin@tradesense.ai',
                full_name='Admin User',
                is_admin=True,
                is_superadmin=True
            )
            admin_user.set_password('admin123')
            
            # Create a regular user
            regular_user = User(
                email='user@tradesense.ai',
                full_name='Regular User'
            )
            regular_user.set_password('user123')
            
            db.session.add(admin_user)
            db.session.add(regular_user)
            db.session.commit()
            
            print("Default users recreated successfully!")
            print(f"Admin: admin@tradesense.ai / admin123")
            print(f"User: user@tradesense.ai / user123")

if __name__ == "__main__":
    create_default_users()