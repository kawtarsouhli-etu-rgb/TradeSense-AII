import os
from datetime import timedelta

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:111111@localhost/EXAM'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # PayPal Configuration
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', 'sb')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', 'your-fake-paypal-secret')
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')