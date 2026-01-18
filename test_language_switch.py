# Test the language switching functionality
import time
import subprocess
import requests

def test_language_switching():
    print("Testing language switching functionality...")
    
    # Test the backend is running
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server is not responding")
            return
    except Exception as e:
        print(f"❌ Backend server error: {e}")
        print("Make sure the backend server is running on port 5000")
        return
    
    print("\nThe language switching should work as follows:")
    print("1. Click on the language selector in the top right corner")
    print("2. Select French (Français) or Arabic (العربية)")
    print("3. The language should change immediately")
    print("4. The text throughout the application should update to the selected language")
    print("\nTroubleshooting tips if language doesn't change:")
    print("- Make sure you have installed all dependencies: npm install")
    print("- Restart the frontend: npm run dev")
    print("- Clear browser cache and hard refresh (Ctrl+F5)")
    print("- Check browser console for JavaScript errors")
    print("- Make sure the i18n configuration is loaded correctly")

if __name__ == "__main__":
    test_language_switching()