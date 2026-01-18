"""Quick backend API test script"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing TradeSense Backend API\n")
    
    # Test 1: Check API is running
    print("1️⃣ Testing API status...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", timeout=5)
        print(f"   ✅ API is running (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ API is NOT running! Error: {e}")
        print("\n⚠️  Please start Flask backend first:")
        print("   cd backend")
        print("   python app.py")
        return
    
    # Test 2: Register a test user
    print("\n2️⃣ Testing user registration...")
    register_data = {
        "full_name": "Test User",
        "email": "test@tradesense.ai",
        "password": "test123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        if response.status_code == 201:
            print("   ✅ User registered successfully")
        elif response.status_code == 400 and "already exists" in response.text:
            print("   ℹ️  User already exists (OK)")
        else:
            print(f"   ⚠️  Unexpected response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Registration failed: {e}")
    
    # Test 3: Login
    print("\n3️⃣ Testing user login...")
    login_data = {
        "email": "test@tradesense.ai",
        "password": "test123"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print("   ✅ Login successful")
            print(f"   Token: {token[:30]}...")
            
            # Test 4: Get challenges
            print("\n4️⃣ Testing challenges endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/api/challenges", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Challenges loaded: {data.get('total', 0)} challenges")
            else:
                print(f"   ❌ Challenges failed: {response.status_code}")
            
            # Test 5: Get watchlist
            print("\n5️⃣ Testing market watchlist...")
            response = requests.get(f"{BASE_URL}/api/market/watchlist", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Watchlist loaded: {len(data.get('data', []))} symbols")
            else:
                print(f"   ❌ Watchlist failed: {response.status_code}")
            
            # Test 6: Get payment plans
            print("\n6️⃣ Testing payment plans...")
            response = requests.get(f"{BASE_URL}/api/payment/plans", headers=headers)
            if response.status_code == 200:
                data = response.json()
                plans = data.get('plans', [])
                print(f"   ✅ Plans loaded: {len(plans)} plans")
                for plan in plans:
                    print(f"      - {plan['name'].upper()}: {plan['price']} DH")
            else:
                print(f"   ❌ Plans failed: {response.status_code}")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Login error: {e}")
    
    print("\n" + "="*50)
    print("✅ Backend tests completed!")
    print("="*50)

if __name__ == "__main__":
    test_api()
