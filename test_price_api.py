"""
Test Script for Real-Time Price API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_price_endpoint():
    print("🧪 Testing Real-Time Price API\n")
    
    # Test 1: Single ticker
    print("1️⃣ Testing single ticker (AAPL)...")
    try:
        response = requests.get(f"{BASE_URL}/api/price/AAPL")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data['symbol']} = ${data['current_price']}")
            print(f"      Change: {data['change']} ({data['change_percent']}%)")
            print(f"      Volume: {data['volume']:,}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Cryptocurrency
    print("\n2️⃣ Testing cryptocurrency (BTC-USD)...")
    try:
        response = requests.get(f"{BASE_URL}/api/price/BTC-USD")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data['symbol']} = ${data['current_price']}")
            print(f"      Change: {data['change']} ({data['change_percent']}%)")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 3: Multiple tickers
    print("\n3️⃣ Testing multiple tickers...")
    try:
        response = requests.get(f"{BASE_URL}/api/price/?tickers=AAPL,TSLA,BTC-USD")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Success: Multiple prices fetched")
            for ticker, price_data in data['prices'].items():
                if 'error' not in price_data:
                    print(f"      {ticker}: ${price_data['current_price']}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 4: Health check
    print("\n4️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/price/health")
        if response.status_code == 200:
            print("   ✅ Health check: Healthy")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check exception: {e}")
    
    print("\n" + "="*50)
    print("✅ Price API tests completed!")
    print("💡 Note: Prices may vary depending on market hours")
    print("="*50)

if __name__ == "__main__":
    test_price_endpoint()
