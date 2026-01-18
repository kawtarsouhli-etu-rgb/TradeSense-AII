"""
API Testing Script for TradeSense Backend
Tests all major API endpoints
"""

import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:5000"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.YELLOW}→ {message}{Colors.ENDC}")


def print_response(response):
    """Print formatted response"""
    print(f"{Colors.YELLOW}Status Code: {response.status_code}{Colors.ENDC}")
    try:
        print(f"{Colors.YELLOW}Response:{Colors.ENDC}")
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_register():
    """Test 1: User Registration"""
    print_section("TEST 1: USER REGISTRATION")
    
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "email": "test@test.com",
        "password": "Test123!",
        "full_name": "Test User"
    }
    
    print_info(f"POST {url}")
    print_info(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print_response(response)
        
        if response.status_code == 201:
            print_success("Registration successful!")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print_success("User already exists (expected if running multiple times)")
            return True
        else:
            print_error("Registration failed!")
            return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_login():
    """Test 2: User Login"""
    print_section("TEST 2: USER LOGIN")
    
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "email": "test@test.com",
        "password": "Test123!"
    }
    
    print_info(f"POST {url}")
    print_info(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data)
        print_response(response)
        
        if response.status_code == 200:
            token = response.json().get('access_token')
            print_success("Login successful!")
            print_success(f"Access Token: {token[:50]}...")
            return token
        else:
            print_error("Login failed!")
            return None
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return None


def test_get_user_info(token):
    """Test 3: Get Current User Info"""
    print_section("TEST 3: GET CURRENT USER INFO")
    
    url = f"{BASE_URL}/api/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print_info(f"GET {url}")
    print_info(f"Headers: Authorization: Bearer {token[:30]}...")
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            print_success("User info retrieved successfully!")
            return True
        else:
            print_error("Failed to get user info!")
            return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_create_challenge(token):
    """Test 4: Create Challenge"""
    print_section("TEST 4: CREATE CHALLENGE")
    
    url = f"{BASE_URL}/api/challenges/create"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "plan_type": "starter"
    }
    
    print_info(f"POST {url}")
    print_info(f"Headers: Authorization: Bearer {token[:30]}...")
    print_info(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print_response(response)
        
        if response.status_code == 201:
            challenge_id = response.json().get('challenge', {}).get('id')
            print_success(f"Challenge created successfully! ID: {challenge_id}")
            return challenge_id
        else:
            print_error("Failed to create challenge!")
            return None
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return None


def test_get_challenges(token):
    """Test 5: Get User Challenges"""
    print_section("TEST 5: GET USER CHALLENGES")
    
    url = f"{BASE_URL}/api/challenges"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print_info(f"GET {url}")
    print_info(f"Headers: Authorization: Bearer {token[:30]}...")
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            challenges = response.json().get('challenges', [])
            print_success(f"Retrieved {len(challenges)} challenge(s)!")
            return challenges[0]['id'] if challenges else None
        else:
            print_error("Failed to get challenges!")
            return None
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return None


def test_get_market_price(token):
    """Test 6: Get Market Price"""
    print_section("TEST 6: GET MARKET PRICE")
    
    symbols = ["AAPL", "BTC", "IAM"]
    
    for symbol in symbols:
        url = f"{BASE_URL}/api/market/price/{symbol}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        print_info(f"GET {url}")
        print_info(f"Headers: Authorization: Bearer {token[:30]}...")
        
        try:
            response = requests.get(url, headers=headers)
            print_response(response)
            
            if response.status_code == 200:
                price_data = response.json()
                price = price_data.get('price', 0)
                print_success(f"{symbol} price: ${price}")
            else:
                print_error(f"Failed to get {symbol} price!")
        except Exception as e:
            print_error(f"Request failed: {str(e)}")
        
        print()


def test_buy_trade(token, challenge_id):
    """Test 7: Buy Trade"""
    print_section("TEST 7: BUY TRADE")
    
    url = f"{BASE_URL}/api/trade/buy"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "symbol": "AAPL",
        "quantity": 5,
        "challenge_id": challenge_id
    }
    
    print_info(f"POST {url}")
    print_info(f"Headers: Authorization: Bearer {token[:30]}...")
    print_info(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print_response(response)
        
        if response.status_code == 201:
            trade_id = response.json().get('trade', {}).get('id')
            print_success(f"Trade created successfully! ID: {trade_id}")
            return trade_id
        else:
            print_error("Failed to create trade!")
            return None
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return None


def test_get_trades(token):
    """Test 8: Get User Trades"""
    print_section("TEST 8: GET USER TRADES")
    
    url = f"{BASE_URL}/api/trades"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print_info(f"GET {url}")
    print_info(f"Headers: Authorization: Bearer {token[:30]}...")
    
    try:
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            trades = response.json().get('trades', [])
            print_success(f"Retrieved {len(trades)} trade(s)!")
            return True
        else:
            print_error("Failed to get trades!")
            return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_sell_trade(token, trade_id):
    """Test 9: Sell Trade"""
    print_section("TEST 9: SELL TRADE")
    
    url = f"{BASE_URL}/api/trade/sell"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "trade_id": trade_id
    }
    
    print_info(f"POST {url}")
    print_info(f"Headers: Authorization: Bearer {token[:30]}...")
    print_info(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            trade = response.json().get('trade', {})
            profit_loss = trade.get('profit_loss', 0)
            print_success(f"Trade closed successfully! P/L: ${profit_loss}")
            return True
        else:
            print_error("Failed to close trade!")
            return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_get_leaderboard():
    """Test 10: Get Leaderboard"""
    print_section("TEST 10: GET LEADERBOARD")
    
    url = f"{BASE_URL}/api/leaderboard"
    
    print_info(f"GET {url}")
    
    try:
        response = requests.get(url)
        print_response(response)
        
        if response.status_code == 200:
            leaderboard = response.json().get('leaderboard', [])
            print_success(f"Retrieved leaderboard with {len(leaderboard)} trader(s)!")
            
            if leaderboard:
                print_info("\nTop 3 Traders:")
                for i, entry in enumerate(leaderboard[:3], 1):
                    user = entry.get('user', {})
                    perf = entry.get('performance', {})
                    print(f"{i}. {user.get('full_name')} - {perf.get('profit_percentage')}%")
            
            return True
        else:
            print_error("Failed to get leaderboard!")
            return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_payment_plans():
    """Test 11: Get Payment Plans"""
    print_section("TEST 11: GET PAYMENT PLANS")
    
    url = f"{BASE_URL}/api/payment/plans"
    
    print_info(f"GET {url}")
    
    try:
        response = requests.get(url)
        print_response(response)
        
        if response.status_code == 200:
            plans = response.json().get('plans', [])
            print_success(f"Retrieved {len(plans)} payment plan(s)!")
            
            for plan in plans:
                print_info(f"\n{plan['name']}: {plan['price']} {plan['currency']}")
                print_info(f"  Initial Balance: {plan['challenge_config']['initial_balance']} DH")
            
            return True
        else:
            print_error("Failed to get payment plans!")
            return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def main():
    """Main test runner"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║          TradeSense API Testing Suite                     ║")
    print("║          Testing all API endpoints                        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Track test results
    results = {
        'passed': 0,
        'failed': 0
    }
    
    # Test 1: Register
    if test_register():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 2: Login
    token = test_login()
    if token:
        results['passed'] += 1
    else:
        results['failed'] += 1
        print_error("Cannot continue without token. Exiting...")
        return
    
    # Test 3: Get User Info
    if test_get_user_info(token):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 4: Create Challenge
    challenge_id = test_create_challenge(token)
    if challenge_id:
        results['passed'] += 1
    else:
        # Try to get existing challenge
        challenge_id = test_get_challenges(token)
        if challenge_id:
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Test 5: Get Market Prices
    test_get_market_price(token)
    results['passed'] += 1
    
    # Test 6: Buy Trade
    trade_id = None
    if challenge_id:
        trade_id = test_buy_trade(token, challenge_id)
        if trade_id:
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Test 7: Get Trades
    if test_get_trades(token):
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 8: Sell Trade
    if trade_id:
        if test_sell_trade(token, trade_id):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Test 9: Get Leaderboard
    if test_get_leaderboard():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Test 10: Get Payment Plans
    if test_payment_plans():
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Summary
    print_section("TEST SUMMARY")
    total_tests = results['passed'] + results['failed']
    print(f"{Colors.GREEN}Passed: {results['passed']}/{total_tests}{Colors.ENDC}")
    print(f"{Colors.RED}Failed: {results['failed']}/{total_tests}{Colors.ENDC}")
    
    if results['failed'] == 0:
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 All tests passed! 🎉{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠ Some tests failed. Check the logs above. ⚠{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user.{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n\n{Colors.RED}Unexpected error: {str(e)}{Colors.ENDC}\n")
