from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superadmin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    challenges = db.relationship('UserChallenge', backref='user', lazy=True, cascade='all, delete-orphan')
    trades = db.relationship('Trade', backref='user', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'is_admin': self.is_admin,
            'is_superadmin': self.is_superadmin,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class UserChallenge(db.Model):
    """User challenge model for trading challenges"""
    __tablename__ = 'user_challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    plan_type = db.Column(db.String(50), nullable=False)
    initial_balance = db.Column(db.Float, nullable=False, default=5000.0)
    current_balance = db.Column(db.Float, nullable=False, default=5000.0)
    status = db.Column(db.String(20), default='ACTIVE', index=True)  # ACTIVE, PASSED, FAILED
    profit_target = db.Column(db.Float, nullable=False)
    max_daily_loss = db.Column(db.Float, nullable=False)
    max_total_loss = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    trades = db.relationship('Trade', backref='challenge', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert challenge object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_type': self.plan_type,
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'status': self.status,
            'profit_target': self.profit_target,
            'max_daily_loss': self.max_daily_loss,
            'max_total_loss': self.max_total_loss,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<UserChallenge {self.id} - {self.plan_type}>'


class Trade(db.Model):
    """Trade model for recording user trades"""
    __tablename__ = 'trades'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('user_challenges.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)  # e.g., 'AAPL', 'GOOGL'
    trade_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    quantity = db.Column(db.Float, nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=True)
    profit_loss = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='open')  # open, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert trade object to dictionary"""
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'trade_type': self.trade_type,
            'quantity': self.quantity,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'profit_loss': self.profit_loss,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Trade {self.id} - {self.symbol}>'


class Payment(db.Model):
    """Payment model for tracking user payments"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('user_challenges.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    payment_method = db.Column(db.String(50), nullable=False)  # 'paypal', 'cmi', 'crypto', 'mock'
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    paypal_order_id = db.Column(db.String(100), nullable=True)  # PayPal order ID
    paypal_payer_id = db.Column(db.String(100), nullable=True)  # PayPal payer ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert payment object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'paypal_order_id': self.paypal_order_id,
            'paypal_payer_id': self.paypal_payer_id,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount} {self.currency}>'


class PayPalSettings(db.Model):
    """PayPal configuration settings (managed by SuperAdmin)"""
    __tablename__ = 'paypal_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(20), default='sandbox')  # sandbox or live
    client_id = db.Column(db.String(200), nullable=False)
    client_secret = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_secret=False):
        """Convert settings to dictionary (hide secret by default)"""
        data = {
            'id': self.id,
            'mode': self.mode,
            'client_id': self.client_id,
            'is_active': self.is_active,
            'updated_at': self.updated_at.isoformat()
        }
        if include_secret:
            data['client_secret'] = self.client_secret
        else:
            data['client_secret'] = '***HIDDEN***'
        return data
    
    @classmethod
    def get_active_settings(cls):
        """Get active PayPal settings"""
        return cls.query.filter_by(is_active=True).first()
    
    @classmethod
    def update_settings(cls, mode, client_id, client_secret, updated_by_user_id):
        """Update PayPal settings with new values"""
        # Deactivate existing settings
        existing = cls.query.first()
        if existing:
            existing.is_active = False
        
        # Create new settings
        new_settings = cls(
            mode=mode,
            client_id=client_id,
            client_secret=client_secret,
            is_active=True,
            updated_by=updated_by_user_id
        )
        
        db.session.add(new_settings)
        db.session.commit()
        
        return new_settings
    
    def __repr__(self):
        return f'<PayPalSettings {self.mode} - Active: {self.is_active}>'
