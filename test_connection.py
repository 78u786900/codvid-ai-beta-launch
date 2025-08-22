#!/usr/bin/env python3
"""
Test script to verify API connection
"""

import requests
import json

def test_api_connection():
    """Test the API connection"""
    base_url = "https://codvid-ai-backend-development.up.railway.app"
    
    print("Testing CodVid.AI API Connection...")
    print(f"Base URL: {base_url}")
    print("=" * 50)
    
    try:
        # Test basic connectivity
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health check status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {e}")
        print("   This is normal if the health endpoint doesn't exist")
    
    try:
        # Test with a simple request
        test_data = {
            "schema_version": "4.0",
            "data": {
                "auth_type": "email",
                "email": "test@example.com",
                "password": "test123"
            }
        }
        
        response = requests.post(
            f"{base_url}/codvid-ai/auth/login",
            json=test_data,
            timeout=15
        )
        
        print(f"API endpoint test status: {response.status_code}")
        
        if response.status_code in [200, 201, 400, 401]:
            print("API server is responding correctly")
        else:
            print(f"Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"API connection failed: {e}")
        return False
    
    print("=" * 50)
    print("API connection test completed!")
    return True

if __name__ == "__main__":
    test_api_connection() 