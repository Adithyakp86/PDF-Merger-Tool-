import requests
import os
import json

def test_pdf_editing_endpoints():
    """Test the PDF editing endpoints"""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing PDF editing endpoints...")
    
    try:
        # Test remove page endpoint (without actual file)
        response = requests.post(f"{base_url}/edit/remove_page", 
                               json={"pdf_path": "nonexistent.pdf", "page_num": 0})
        if response.status_code == 404:
            print("✓ Remove page endpoint correctly handles missing files")
        else:
            print(f"✗ Remove page endpoint returned unexpected status {response.status_code}")
            
        # Test rotate page endpoint (without actual file)
        response = requests.post(f"{base_url}/edit/rotate_page", 
                               json={"pdf_path": "nonexistent.pdf", "page_num": 0, "rotation": 90})
        if response.status_code == 404:
            print("✓ Rotate page endpoint correctly handles missing files")
        else:
            print(f"✗ Rotate page endpoint returned unexpected status {response.status_code}")
            
        # Test add text endpoint (without actual file)
        response = requests.post(f"{base_url}/edit/add_text", 
                               json={"pdf_path": "nonexistent.pdf", "text": "Test", "page_num": 0, "x": 100, "y": 750})
        if response.status_code == 404:
            print("✓ Add text endpoint correctly handles missing files")
        else:
            print(f"✗ Add text endpoint returned unexpected status {response.status_code}")
            
        print("\nAll PDF editing endpoint tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to the web server. Make sure the web application is running.")
        return False
    except Exception as e:
        print(f"✗ An error occurred during testing: {e}")
        return False

if __name__ == "__main__":
    test_pdf_editing_endpoints()