from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)  # Initialize JWT manager

# Register blueprints
from routes.trading import trading_bp
from routes.market import market_bp
from routes.auth import auth_bp
from routes.challenges import challenges_bp
from routes.payment import payment_bp
from routes.leaderboard import leaderboard_bp
from routes.admin import admin_bp
from routes.paypal import paypal_bp
from routes.price import price_bp
from routes.moroccan import moroccan_bp

app.register_blueprint(trading_bp)
app.register_blueprint(market_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(challenges_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(paypal_bp)
app.register_blueprint(price_bp)
app.register_blueprint(moroccan_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({
        "message": "TradeSense API",
        "status": "running"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "status": "success",
        "message": "API fonctionne!"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
