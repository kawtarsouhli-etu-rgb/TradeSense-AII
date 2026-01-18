# 🅿️ PayPal Integration Guide

## 📋 Overview
Integrated PayPal Checkout in sandbox mode for TradeSense AI challenge purchases.

## 🏗️ Architecture

### PayPal Flow (Sandbox Mode)
```
1. User selects plan → Click "Pay with PayPal"
2. Frontend calls /api/paypal/create-payment
3. Backend creates PayPal order + saves in DB (status: pending)
4. Returns approval_url to frontend
5. User redirected to PayPal sandbox
6. User approves payment
7. PayPal redirects back with payment_id + payer_id
8. Frontend calls /api/paypal/execute-payment
9. Backend executes payment + creates challenge
10. Challenge status = ACTIVE
11. Payment saved in database
```

## 🔧 Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install paypalrestsdk==1.13.1
```

### 2. Database Migration
Run this to create PayPal tables:
```python
# In Python shell
from app import app, db
with app.app_context():
    db.create_all()
```

### 3. Configure PayPal Credentials (SuperAdmin Panel)

**Via API:**
```bash
# SuperAdmin token required
curl -X POST http://localhost:5000/api/paypal/settings \
  -H "Authorization: Bearer SUPERADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "sandbox",
    "client_id": "YOUR_SANDBOX_CLIENT_ID",
    "client_secret": "YOUR_SANDBOX_CLIENT_SECRET",
    "is_active": true
  }'
```

**Or via Database Directly:**
```sql
INSERT INTO paypal_settings (mode, client_id, client_secret, is_active, updated_at) 
VALUES (
  'sandbox',
  'YOUR_SANDBOX_CLIENT_ID',
  'YOUR_SANDBOX_CLIENT_SECRET',
  1,
  datetime('now')
);
```

### 4. Get PayPal Sandbox Credentials

1. Go to https://developer.paypal.com/
2. Create account or login
3. Go to "My Apps & Credentials"
4. Create App (Sandbox)
5. Copy Client ID and Secret

## 🎨 Frontend Integration

### Add PayPal Button to ChallengesPage.jsx

In your payment modal, add:
```jsx
import { paypalAPI } from '../services/api';

// Add to payment methods
<button 
  className="payment-btn payment-paypal"
  onClick={() => handlePayPalPayment()}
>
  <span className="payment-icon">🅿️</span>
  <div className="payment-info">
    <strong>Pay with PayPal</strong>
    <small>Secure checkout with PayPal</small>
  </div>
</button>

// Handler function
const handlePayPalPayment = async () => {
  try {
    setPaymentLoading(true);
    
    // 1. Create PayPal payment
    const res = await paypalAPI.createPayment(paymentModal.plan.id);
    
    // 2. Redirect to PayPal
    window.location.href = res.data.approval_url;
    
  } catch (error) {
    setMessage({ 
      type: 'error', 
      text: error.response?.data?.error || 'PayPal payment failed' 
    });
    setPaymentLoading(false);
  }
};

// Handle PayPal return (in App.jsx or component mount)
useEffect(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const paymentId = urlParams.get('paymentId');
  const payerId = urlParams.get('PayerID');
  const planId = urlParams.get('plan_id'); // You'll need to pass this
  
  if (paymentId && payerId && planId) {
    // Execute payment
    paypalAPI.executePayment(paymentId, payerId, planId)
      .then(res => {
        // Success - challenge activated
        setMessage({ 
          type: 'success', 
          text: '✅ PayPal payment successful! Challenge activated.' 
        });
        // Reload challenges
        loadData();
      })
      .catch(err => {
        setMessage({ 
          type: 'error', 
          text: err.response?.data?.error || 'Payment execution failed' 
        });
      });
  }
}, []);
```

## 🧪 Testing PayPal Sandbox

### Test Accounts
1. **Merchant Account** (your business):
   - Use your sandbox client credentials

2. **Buyer Account** (for testing):
   - Go to PayPal Developer Dashboard
   - Navigate to "Sandbox" → "Accounts"
   - Use existing test accounts or create new ones
   - Example buyer: sb-buyer@example.com

### Test Process
1. Select a challenge plan
2. Click "Pay with PayPal"
3. You'll be redirected to PayPal sandbox
4. Login with sandbox buyer account
5. Approve payment
6. You should be redirected back to your app
7. Challenge should be ACTIVE

## 🔐 Security Notes

### Backend
- ✅ PayPal credentials stored in database (not hardcoded)
- ✅ SuperAdmin only can update credentials
- ✅ Payment validation before challenge creation
- ✅ Database transactions with rollback on failure

### Frontend
- ✅ JWT authentication required
- ✅ Payment status verified server-side
- ✅ No sensitive data exposed to client

## 📊 Database Schema

### New Columns in `payments` table:
- `challenge_id` (FK to user_challenges)
- `paypal_order_id` (PayPal order ID)
- `paypal_payer_id` (PayPal payer ID)

### New Table `paypal_settings`:
- `mode` (sandbox/live)
- `client_id` (encrypted)
- `client_secret` (encrypted)
- `is_active` (boolean)
- `updated_by` (FK to users - SuperAdmin)

## 🚨 Troubleshooting

### Common Errors:
1. **"PayPal not configured"**
   - Solution: Add credentials via SuperAdmin panel

2. **"Invalid client ID/secret"**
   - Solution: Verify sandbox credentials in PayPal Developer Dashboard

3. **"Payment not found"**
   - Solution: Check database for pending payment record

4. **Redirect loop**
   - Solution: Ensure return URLs match exactly

## 🎯 Production Deployment

### Steps:
1. Change `mode` from "sandbox" to "live"
2. Use live PayPal credentials
3. Update return URLs to production domain
4. Test thoroughly with small amounts
5. Monitor transactions in PayPal dashboard

### Environment Variables (Recommended):
Instead of database, you can use environment variables:
```bash
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=your_live_client_id
PAYPAL_CLIENT_SECRET=your_live_client_secret
```

Then modify `paypal_service.py` to read from env vars.

---
**Need help?** Contact the TradeSense team for PayPal integration support.
