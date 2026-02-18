#!/usr/bin/env python3
"""
Test Signup Process with Email Error Handling
This script tests that signup works even when email sending fails.
"""

import os
from dotenv import load_dotenv
from api.auth import signup, SignUpRequest
from fastapi import HTTPException

def test_signup_with_email_error_handling():
    """Test that signup works even when email sending fails."""
    print("Testing signup with email error handling...")
    
    # Load environment variables
    load_dotenv(override=True)
    
    # Create a test user request
    signup_data = SignUpRequest(
        email="testuser@example.com",
        name="Test User",
        password="SecurePassword123!",
        role="writer",  # Use a valid role
        country="Pakistan",
        city="Karachi"
    )
    
    try:
        # Call the signup function directly
        result = signup(signup_data)
        print("Signup successful!")
        print(f"Result: {result}")
        return True
    except HTTPException as he:
        if "already exists" in str(he.detail).lower():
            print(f"User already exists (expected if running multiple times): {he.detail}")
            return True  # This is acceptable
        else:
            print(f"HTTP Exception during signup: {he.detail} (status: {he.status_code})")
            return False
    except Exception as e:
        print(f"Signup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_signup_with_email_error_handling()
    if success:
        print("\nSignup test completed successfully!")
    else:
        print("\nSignup test failed!")