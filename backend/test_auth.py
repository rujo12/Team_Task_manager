#!/usr/bin/env python
"""
Quick authentication API test script.

Usage:
    python test_auth.py

Tests all authentication endpoints and validates responses.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api"

# Colors for console output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def print_section(title):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(message):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.RESET}")

def print_json(data):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2))

def test_signup():
    """Test user signup endpoint."""
    print_section("1. Testing User Signup")
    
    # Test data
    test_user = {
        "username": f"testuser_{datetime.now().timestamp():.0f}",
        "email": f"test_{datetime.now().timestamp():.0f}@example.com",
        "password": "TestPassword123",
        "password_confirm": "TestPassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print_info(f"Creating user: {test_user['username']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print_success(f"User signup successful (Status: {response.status_code})")
            print_info(f"User ID: {data['data']['id']}")
            print_info(f"Username: {data['data']['username']}")
            print_info(f"Email: {data['data']['email']}")
            return test_user  # Return for use in next tests
        else:
            print_error(f"Signup failed (Status: {response.status_code})")
            print_json(response.json())
            return None
    
    except Exception as e:
        print_error(f"Error during signup: {str(e)}")
        return None

def test_login(user_data):
    """Test user login endpoint."""
    if not user_data:
        print_error("Skipping login test - no user data from signup")
        return None
    
    print_section("2. Testing User Login")
    
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    print_info(f"Logging in as: {user_data['username']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login successful (Status: {response.status_code})")
            
            access_token = data.get("access")
            refresh_token = data.get("refresh")
            user_info = data.get("user", {})
            
            print_info(f"Access token received (length: {len(access_token) if access_token else 0})")
            print_info(f"Refresh token received (length: {len(refresh_token) if refresh_token else 0})")
            print_info(f"User: {user_info.get('username')} ({user_info.get('email')})")
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user_info
            }
        else:
            print_error(f"Login failed (Status: {response.status_code})")
            print_json(response.json())
            return None
    
    except Exception as e:
        print_error(f"Error during login: {str(e)}")
        return None

def test_get_current_user(tokens):
    """Test get current user endpoint."""
    if not tokens or not tokens.get("access_token"):
        print_error("Skipping current user test - no access token")
        return
    
    print_section("3. Testing Get Current User")
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json"
    }
    
    print_info("Fetching current user profile...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/users/me",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            user_data = data.get("data", {})
            print_success(f"Current user retrieved (Status: {response.status_code})")
            print_info(f"Username: {user_data.get('username')}")
            print_info(f"Email: {user_data.get('email')}")
            print_info(f"Full Name: {user_data.get('full_name')}")
            print_info(f"Joined: {user_data.get('date_joined')}")
        else:
            print_error(f"Failed to get current user (Status: {response.status_code})")
            print_json(response.json())
    
    except Exception as e:
        print_error(f"Error getting current user: {str(e)}")

def test_refresh_token(tokens):
    """Test refresh token endpoint."""
    if not tokens or not tokens.get("refresh_token"):
        print_error("Skipping refresh token test - no refresh token")
        return
    
    print_section("4. Testing Refresh Token")
    
    refresh_data = {
        "refresh": tokens["refresh_token"]
    }
    
    print_info("Refreshing access token...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/refresh",
            json=refresh_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            new_access_token = data.get("access")
            print_success(f"Token refresh successful (Status: {response.status_code})")
            print_info(f"New access token received (length: {len(new_access_token) if new_access_token else 0})")
        else:
            print_error(f"Token refresh failed (Status: {response.status_code})")
            print_json(response.json())
    
    except Exception as e:
        print_error(f"Error refreshing token: {str(e)}")

def test_invalid_credentials():
    """Test login with invalid credentials."""
    print_section("5. Testing Invalid Credentials (Error Handling)")
    
    invalid_data = {
        "username": "nonexistent_user",
        "password": "WrongPassword123"
    }
    
    print_info("Attempting login with invalid credentials...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            print_success(f"Correctly rejected invalid credentials (Status: {response.status_code})")
            print_info("Error message: " + response.json().get("detail", "Unknown error"))
        else:
            print_error(f"Unexpected status code: {response.status_code}")
    
    except Exception as e:
        print_error(f"Error testing invalid credentials: {str(e)}")

def test_password_validation():
    """Test signup with invalid password."""
    print_section("6. Testing Password Validation (Error Handling)")
    
    invalid_user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "weak",  # Too short
        "password_confirm": "weak"
    }
    
    print_info("Attempting signup with weak password...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=invalid_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            data = response.json()
            print_success(f"Correctly rejected weak password (Status: {response.status_code})")
            if "details" in data and "password" in data["details"]:
                for error in data["details"]["password"]:
                    print_info(f"Validation error: {error}")
        else:
            print_error(f"Unexpected status code: {response.status_code}")
    
    except Exception as e:
        print_error(f"Error testing password validation: {str(e)}")

def main():
    """Run all tests."""
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔════════════════════════════════════════════════════════════╗
║  Team Task Manager - Authentication API Test Suite        ║
║  Testing all authentication endpoints                      ║
╚════════════════════════════════════════════════════════════╝
{Colors.RESET}
""")
    
    print_info("Make sure Django development server is running:")
    print_info("  python manage.py runserver")
    
    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/users/me", timeout=2)
    except:
        print_error("Cannot connect to API server!")
        print_info("Start the server with: python manage.py runserver")
        return
    
    print_success("Connected to API server!")
    
    # Run tests
    user_data = test_signup()
    tokens = test_login(user_data)
    test_get_current_user(tokens)
    test_refresh_token(tokens)
    test_invalid_credentials()
    test_password_validation()
    
    # Summary
    print_section("Test Summary")
    print_success("All tests completed!")
    print_info("Check above for any failures")
    print(f"\n{Colors.BOLD}Next Steps:{Colors.RESET}")
    print("1. Review AUTH_API_COMPLETE.md for full API documentation")
    print("2. Proceed to Phase 2: Project Management (Phase 3)")
    print("3. Then implement Task Management (Phase 4)")

if __name__ == "__main__":
    main()
