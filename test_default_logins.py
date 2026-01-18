import requests
import json

# Base URL for the backend
BASE_URL = "http://localhost:5000"

def test_login_with_default_users():
    print("Testing login with default users...")
    
    # Test with admin credentials
    print("\n1. Testing Admin Login:")
    admin_login_data = {
        "email": "admin@tradesense.ai",
        "password": "admin123"
    }
    
    try:
        admin_response = requests.post(f"{BASE_URL}/api/auth/login", json=admin_login_data)
        print(f"Admin Login Status: {admin_response.status_code}")
        if admin_response.status_code == 200:
            print("Admin login successful!")
            response_data = admin_response.json()
            print(f"User: {response_data['user']['full_name']}")
            print(f"Is Admin: {response_data['user']['is_admin']}")
            print(f"Is SuperAdmin: {response_data['user']['is_superadmin']}")
        else:
            print(f"Admin login failed: {admin_response.text}")
    except Exception as e:
        print(f"Admin login Error: {e}")
    
    # Test with regular user credentials
    print("\n2. Testing Regular User Login:")
    user_login_data = {
        "email": "user@tradesense.ai",
        "password": "user123"
    }
    
    try:
        user_response = requests.post(f"{BASE_URL}/api/auth/login", json=user_login_data)
        print(f"User Login Status: {user_response.status_code}")
        if user_response.status_code == 200:
            print("User login successful!")
            response_data = user_response.json()
            print(f"User: {response_data['user']['full_name']}")
            print(f"Is Admin: {response_data['user']['is_admin']}")
            print(f"Is SuperAdmin: {response_data['user']['is_superadmin']}")
        else:
            print(f"User login failed: {user_response.text}")
    except Exception as e:
        print(f"User login Error: {e}")
    
    # Test with test user credentials from previous test
    print("\n3. Testing Test User Login:")
    test_login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        test_response = requests.post(f"{BASE_URL}/api/auth/login", json=test_login_data)
        print(f"Test User Login Status: {test_response.status_code}")
        if test_response.status_code == 200:
            print("Test user login successful!")
            response_data = test_response.json()
            print(f"User: {response_data['user']['full_name']}")
            print(f"Is Admin: {response_data['user']['is_admin']}")
            print(f"Is SuperAdmin: {response_data['user']['is_superadmin']}")
        else:
            print(f"Test user login failed: {test_response.text}")
    except Exception as e:
        print(f"Test user login Error: {e}")

if __name__ == "__main__":
    test_login_with_default_users()