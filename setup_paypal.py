"""
PayPal Setup Script
Creates initial PayPal settings in database for development
"""

from models import db, PayPalSettings
from app import app

def setup_paypal_sandbox():
    """Setup PayPal sandbox configuration for development"""
    
    # PayPal Sandbox Credentials (for development only)
    # In production, these would be set via SuperAdmin panel
    sandbox_credentials = {
        'mode': 'sandbox',
        'client_id': 'Abyru73sQ4JY58jGk8J9q4p3r2n1o0m6l5k4j3h2g1f0e9d8c7b6a5sandbox',
        'client_secret': 'ECbV98x7w6v5u4t3s2r1q0p9o8n7m6l5k4j3h2g1f0e9d8c7b6sandbox',
        'is_active': True
    }
    
    with app.app_context():
        # Check if PayPal settings already exist
        existing_settings = PayPalSettings.query.first()
        
        if existing_settings:
            print("❌ PayPal settings already exist in database")
            print("   To update, use SuperAdmin panel: /api/paypal/settings")
            return
        
        # Create PayPal settings
        paypal_settings = PayPalSettings(
            mode=sandbox_credentials['mode'],
            client_id=sandbox_credentials['client_id'],
            client_secret=sandbox_credentials['client_secret'],
            is_active=sandbox_credentials['is_active'],
            updated_by=1  # SuperAdmin user ID (assuming admin exists)
        )
        
        db.session.add(paypal_settings)
        db.session.commit()
        
        print("✅ PayPal sandbox configuration created successfully!")
        print(f"   Mode: {paypal_settings.mode}")
        print(f"   Active: {paypal_settings.is_active}")
        print(f"   Client ID: {paypal_settings.client_id[:20]}...")
        print("")
        print("📝 NOTE: These are FAKE sandbox credentials for DEVELOPMENT only.")
        print("   In production, update via SuperAdmin panel with real credentials.")

if __name__ == "__main__":
    setup_paypal_sandbox()
