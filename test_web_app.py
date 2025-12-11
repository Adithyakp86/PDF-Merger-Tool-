import requests
import os
import json

def test_web_app_endpoints():
    """Test the web application endpoints"""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing web application endpoints...")
    
    try:
        # Test main page
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✓ Main page loads correctly")
        else:
            print(f"✗ Main page failed with status {response.status_code}")
            
        # Test toggle theme endpoint
        response = requests.post(f"{base_url}/toggle_theme")
        if response.status_code == 200:
            data = response.json()
            if "dark_mode" in data:
                print("✓ Theme toggle endpoint works correctly")
            else:
                print("✗ Theme toggle endpoint returned unexpected data")
        else:
            print(f"✗ Theme toggle endpoint failed with status {response.status_code}")
            
        # Test clear all endpoint
        response = requests.post(f"{base_url}/clear_all")
        if response.status_code == 200:
            data = response.json()
            if "success" in data:
                print("✓ Clear all endpoint works correctly")
            else:
                print("✗ Clear all endpoint returned unexpected data")
        else:
            print(f"✗ Clear all endpoint failed with status {response.status_code}")
            
        print("\nAll endpoint tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the web server. Make sure the web application is running.")
        return False
    except Exception as e:
        print(f"✗ An error occurred during testing: {e}")
        return False

if __name__ == "__main__":
    test_web_app_endpoints()