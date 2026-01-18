"""
Test script for Challenge Engine
Demonstrates the trade execution and challenge evaluation
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_trade_execution():
    """Test the /api/trade/execute endpoint"""
    
    print("=" * 60)
    print("CHALLENGE ENGINE TEST")
    print("=" * 60)
    
    # Test 1: Execute a winning trade
    print("\n[TEST 1] Execute SELL trade (profit)")
    trade_data = {
        "challenge_id": 1,
        "symbol": "AAPL",
        "side": "SELL",
        "amount": 10,
        "price": 150.0
    }
    
    response = requests.post(f"{BASE_URL}/api/trade/execute", json=trade_data)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test 2: Execute a losing trade
    print("\n[TEST 2] Execute BUY trade (loss)")
    trade_data = {
        "challenge_id": 1,
        "symbol": "TSLA",
        "side": "BUY",
        "amount": 5,
        "price": 200.0
    }
    
    response = requests.post(f"{BASE_URL}/api/trade/execute", json=trade_data)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test 3: Get challenge metrics
    print("\n[TEST 3] Get challenge metrics")
    response = requests.get(f"{BASE_URL}/api/challenge/1/metrics")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test 4: Try to trigger daily loss (5% of 5000 = 250)
    print("\n[TEST 4] Execute large losing trade (should trigger daily loss limit)")
    trade_data = {
        "challenge_id": 1,
        "symbol": "GOOGL",
        "side": "BUY",
        "amount": 2,
        "price": 300.0  # 600 loss
    }
    
    response = requests.post(f"{BASE_URL}/api/trade/execute", json=trade_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if result.get('success') and result['challenge']['status'] == 'FAILED':
        print("\n✓ Challenge correctly FAILED due to daily loss limit!")
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_trade_execution()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Flask server.")
        print("Please ensure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"ERROR: {str(e)}")
