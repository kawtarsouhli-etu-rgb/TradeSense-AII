"""
PayPal Payment Service
Handles PayPal sandbox integration for challenge purchases
"""

import paypalrestsdk
from models import db, PayPalSettings, Payment, UserChallenge
from datetime import datetime


class PayPalService:
    """Service for PayPal payment processing"""
    
    @staticmethod
    def get_paypal_config():
        """Get PayPal configuration from database"""
        settings = PayPalSettings.get_active_settings()
        
        if not settings:
            return None, "PayPal not configured. Please contact administrator."
        
        return settings, None
    
    @staticmethod
    def configure_paypal():
        """Configure PayPal SDK with credentials from database"""
        settings, error = PayPalService.get_paypal_config()
        
        if error:
            return False, error
        
        try:
            paypalrestsdk.configure({
                "mode": settings.mode,  # sandbox or live
                "client_id": settings.client_id,
                "client_secret": settings.client_secret
            })
            return True, None
        except Exception as e:
            return False, f"PayPal configuration error: {str(e)}"
    
    @staticmethod
    def create_payment(user_id, plan_id, plan_price, plan_name, return_url, cancel_url):
        """
        Create a PayPal payment
        
        Args:
            user_id: User ID
            plan_id: Plan identifier (starter/pro/elite)
            plan_price: Amount in USD
            plan_name: Plan name
            return_url: Success redirect URL
            cancel_url: Cancel redirect URL
            
        Returns:
            tuple: (approval_url, payment_id, error)
        """
        # Configure PayPal
        success, error = PayPalService.configure_paypal()
        if not success:
            return None, None, error
        
        try:
            # Create PayPal payment object
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": f"TradeSense {plan_name.upper()} Challenge",
                            "sku": plan_id,
                            "price": str(plan_price),
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(plan_price),
                        "currency": "USD"
                    },
                    "description": f"TradeSense {plan_name.upper()} Trading Challenge"
                }]
            })
            
            # Create payment
            if payment.create():
                # Get approval URL
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        
                        # Save payment in database with pending status
                        db_payment = Payment(
                            user_id=user_id,
                            amount=plan_price,
                            currency='USD',
                            payment_method='paypal',
                            status='pending',
                            paypal_order_id=payment.id
                        )
                        db.session.add(db_payment)
                        db.session.commit()
                        
                        return approval_url, payment.id, None
                
                return None, None, "No approval URL found"
            else:
                error_msg = payment.error.get('message', 'Unknown error') if hasattr(payment, 'error') else 'Payment creation failed'
                return None, None, error_msg
                
        except Exception as e:
            return None, None, f"Payment creation error: {str(e)}"
    
    @staticmethod
    def execute_payment(payment_id, payer_id, plan_id, plan_config):
        """
        Execute/capture a PayPal payment after user approval
        
        Args:
            payment_id: PayPal payment ID
            payer_id: PayPal payer ID
            plan_id: Plan identifier
            plan_config: Plan configuration dict
            
        Returns:
            tuple: (payment_dict, challenge_dict, error)
        """
        # Configure PayPal
        success, error = PayPalService.configure_paypal()
        if not success:
            return None, None, error
        
        try:
            # Find payment in database
            db_payment = Payment.query.filter_by(paypal_order_id=payment_id).first()
            
            if not db_payment:
                return None, None, "Payment not found in database"
            
            # Get PayPal payment
            payment = paypalrestsdk.Payment.find(payment_id)
            
            # Execute payment
            if payment.execute({"payer_id": payer_id}):
                # Payment successful - Create challenge
                challenge = UserChallenge(
                    user_id=db_payment.user_id,
                    plan_type=plan_id,
                    initial_balance=plan_config['initial_balance'],
                    current_balance=plan_config['initial_balance'],
                    profit_target=plan_config['profit_target'],
                    max_daily_loss=plan_config['max_daily_loss'],
                    max_total_loss=plan_config['max_total_loss'],
                    status='ACTIVE'
                )
                db.session.add(challenge)
                db.session.flush()  # Get challenge ID
                
                # Update payment
                db_payment.status = 'completed'
                db_payment.paypal_payer_id = payer_id
                db_payment.transaction_id = payment.transactions[0].related_resources[0].sale.id
                db_payment.challenge_id = challenge.id
                
                db.session.commit()
                
                return db_payment.to_dict(), challenge.to_dict(), None
            else:
                # Payment failed
                db_payment.status = 'failed'
                db.session.commit()
                
                error_msg = payment.error.get('message', 'Unknown error') if hasattr(payment, 'error') else 'Payment execution failed'
                return None, None, error_msg
                
        except Exception as e:
            db.session.rollback()
            return None, None, f"Payment execution error: {str(e)}"
    
    @staticmethod
    def get_payment_status(payment_id):
        """Get payment status from PayPal"""
        success, error = PayPalService.configure_paypal()
        if not success:
            return None, error
        
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            return payment.state, None
        except Exception as e:
            return None, f"Error fetching payment status: {str(e)}"
