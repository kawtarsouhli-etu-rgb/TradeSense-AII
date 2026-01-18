import requests
import json

# Base URL for the backend
BASE_URL = "http://localhost:5000"

def test_api():
    print("Testing TradeSense API...")
    
    # Test registration
    print("\n1. Testing Registration:")
    register_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    try:
        register_response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Registration Status: {register_response.status_code}")
        print(f"Registration Response: {register_response.text}")
    except Exception as e:
        print(f"Registration Error: {e}")
    
    # Test login
    print("\n2. Testing Login:")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        print(f"Login Response: {login_response.text}")
        
        if login_response.status_code == 200:
            response_data = login_response.json()
            access_token = response_data.get('access_token')
            print(f"Access Token: {access_token[:50]}..." if access_token else "No token received")
            
            # Test protected route
            print("\n3. Testing Protected Route (/me):")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            me_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
            print(f"Me Endpoint Status: {me_response.status_code}")
            print(f"Me Endpoint Response: {me_response.text}")
    
    except Exception as e:
        print(f"Login Error: {e}")

if __name__ == "__main__":
    test_api()