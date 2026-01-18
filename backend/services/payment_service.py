"""Payment service for payment processing and management"""

import secrets
from models import db, Payment


class PaymentService:
    """Service class for payment management operations"""
    
    @staticmethod
    def create_payment(user_id, amount, currency, payment_method):
        """
        Create a new payment
        
        Args:
            user_id (int): User ID
            amount (float): Payment amount
            currency (str): Currency code (e.g., USD, EUR)
            payment_method (str): Payment method (e.g., credit_card, paypal)
            
        Returns:
            tuple: (payment_dict, error_message)
        """
        try:
            # Generate unique transaction ID
            transaction_id = PaymentService._generate_transaction_id()
            
            payment = Payment(
                user_id=user_id,
                amount=amount,
                currency=currency.upper(),
                payment_method=payment_method,
                transaction_id=transaction_id,
                status='pending'
            )
            
            db.session.add(payment)
            db.session.commit()
            
            return payment.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create payment: {str(e)}"
    
    @staticmethod
    def get_payment_by_id(payment_id):
        """
        Get payment by ID
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (payment_dict, error_message)
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return None, "Payment not found"
            
            return payment.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to get payment: {str(e)}"
    
    @staticmethod
    def get_payment_by_transaction_id(transaction_id):
        """
        Get payment by transaction ID
        
        Args:
            transaction_id (str): Transaction ID
            
        Returns:
            tuple: (payment_dict, error_message)
        """
        try:
            payment = Payment.query.filter_by(transaction_id=transaction_id).first()
            if not payment:
                return None, "Payment not found"
            
            return payment.to_dict(), None
            
        except Exception as e:
            return None, f"Failed to get payment: {str(e)}"
    
    @staticmethod
    def get_user_payments(user_id, status=None):
        """
        Get all payments for a user
        
        Args:
            user_id (int): User ID
            status (str, optional): Filter by status
            
        Returns:
            tuple: (payments_list, error_message)
        """
        try:
            query = Payment.query.filter_by(user_id=user_id)
            
            if status:
                query = query.filter_by(status=status)
            
            payments = query.order_by(Payment.created_at.desc()).all()
            
            return [payment.to_dict() for payment in payments], None
            
        except Exception as e:
            return None, f"Failed to get payments: {str(e)}"
    
    @staticmethod
    def get_all_payments(page=1, per_page=10, status=None):
        """
        Get all payments with pagination
        
        Args:
            page (int): Page number
            per_page (int): Payments per page
            status (str, optional): Filter by status
            
        Returns:
            tuple: (payments_data, error_message)
        """
        try:
            query = Payment.query
            
            if status:
                query = query.filter_by(status=status)
            
            pagination = query.order_by(Payment.created_at.desc()).paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            payments = [payment.to_dict() for payment in pagination.items]
            
            return {
                'payments': payments,
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': page
            }, None
            
        except Exception as e:
            return None, f"Failed to get payments: {str(e)}"
    
    @staticmethod
    def update_payment_status(payment_id, status):
        """
        Update payment status
        
        Args:
            payment_id (int): Payment ID
            status (str): New status (pending, completed, failed, refunded)
            
        Returns:
            tuple: (payment_dict, error_message)
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return None, "Payment not found"
            
            valid_statuses = ['pending', 'completed', 'failed', 'refunded']
            if status not in valid_statuses:
                return None, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            
            payment.status = status
            db.session.commit()
            
            return payment.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update payment status: {str(e)}"
    
    @staticmethod
    def process_payment(payment_id):
        """
        Process a pending payment (simulate payment processing)
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (payment_dict, error_message)
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return None, "Payment not found"
            
            if payment.status != 'pending':
                return None, f"Payment is already {payment.status}"
            
            # In a real application, you would integrate with a payment gateway here
            # For now, we'll simulate successful payment
            payment.status = 'completed'
            db.session.commit()
            
            return payment.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to process payment: {str(e)}"
    
    @staticmethod
    def refund_payment(payment_id):
        """
        Refund a completed payment
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (payment_dict, error_message)
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return None, "Payment not found"
            
            if payment.status != 'completed':
                return None, "Only completed payments can be refunded"
            
            # In a real application, you would process the refund through payment gateway
            payment.status = 'refunded'
            db.session.commit()
            
            return payment.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to refund payment: {str(e)}"
    
    @staticmethod
    def delete_payment(payment_id):
        """
        Delete payment
        
        Args:
            payment_id (int): Payment ID
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            payment = Payment.query.get(payment_id)
            if not payment:
                return False, "Payment not found"
            
            db.session.delete(payment)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete payment: {str(e)}"
    
    @staticmethod
    def get_payment_statistics(user_id=None):
        """
        Get payment statistics
        
        Args:
            user_id (int, optional): Filter by user ID
            
        Returns:
            tuple: (statistics_dict, error_message)
        """
        try:
            query = Payment.query
            
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            payments = query.all()
            
            statistics = {
                'total_payments': len(payments),
                'completed_payments': len([p for p in payments if p.status == 'completed']),
                'pending_payments': len([p for p in payments if p.status == 'pending']),
                'failed_payments': len([p for p in payments if p.status == 'failed']),
                'refunded_payments': len([p for p in payments if p.status == 'refunded']),
                'total_amount': sum(p.amount for p in payments if p.status == 'completed'),
                'pending_amount': sum(p.amount for p in payments if p.status == 'pending'),
                'refunded_amount': sum(p.amount for p in payments if p.status == 'refunded')
            }
            
            return statistics, None
            
        except Exception as e:
            return None, f"Failed to get payment statistics: {str(e)}"
    
    @staticmethod
    def _generate_transaction_id():
        """
        Generate a unique transaction ID
        
        Returns:
            str: Unique transaction ID
        """
        return f"TXN-{secrets.token_hex(16).upper()}"
