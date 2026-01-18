"""
Test Script for Moroccan Stock Scraper
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_moroccan_scraper():
    print("🧪 Testing Moroccan Stock Scraper API\n")
    
    # Test 1: IAM stock price
    print("1️⃣ Testing IAM stock price...")
    try:
        response = requests.get(f"{BASE_URL}/api/moroccan/stock/IAM")
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print(f"   ✅ Success: {data['symbol']} = {data['current_price']} MAD")
                print(f"      Source: {data['source']}")
                print(f"      Time: {data['processing_time_ms']:.2f}ms")
                if 'is_demo' in data and data['is_demo']:
                    print("      📝 Note: Using demo data (live data not available)")
            else:
                print(f"   ⚠️  Info: {data['error']}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: All moroccan stocks
    print("\n2️⃣ Testing all moroccan stocks...")
    try:
        response = requests.get(f"{BASE_URL}/api/moroccan/stocks")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: Found {data['supported_count']} supported stocks")
            if 'IAM' in data['stocks']:
                iam_data = data['stocks']['IAM']
                print(f"      IAM: {iam_data['current_price']} MAD")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 3: Health check
    print("\n3️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/moroccan/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check: {data['status']}")
            print(f"      Supported stocks: {data['supported_stocks']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check exception: {e}")
    
    # Test 4: Compatibility endpoint
    print("\n4️⃣ Testing compatibility endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/moroccan/price/IAM")
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print(f"   ✅ Compatibility endpoint works: {data['current_price']} MAD")
            else:
                print(f"   ⚠️  Compatibility: {data['error']}")
        else:
            print(f"   ❌ Compatibility endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Compatibility exception: {e}")
    
    print("\n" + "="*50)
    print("✅ Moroccan Stock API tests completed!")
    print("💡 Note: May show demo data if live data not available")
    print("="*50)

if __name__ == "__main__":
    test_moroccan_scraper()
