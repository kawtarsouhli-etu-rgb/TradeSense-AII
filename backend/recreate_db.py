from app import app
from models import db

def recreate_database():
    with app.app_context():
        print("Dropping and recreating database...")
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database recreated successfully!")

if __name__ == "__main__":
    recreate_database()