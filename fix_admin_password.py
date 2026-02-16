#!/usr/bin/env python3
"""
Fix Admin User Password Hash
This script updates the admin user's password hash to use the correct algorithm.
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
from utils.hashing import hash_password

def fix_admin_password():
    """Update the admin user's password hash to use the correct algorithm."""
    # Load environment variables
    load_dotenv(override=True)
    
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] DATABASE_URL is not set in your .env file")
        return False
    
    # Parse the database URL
    import re
    pg_pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$'
    match = re.match(pg_pattern, database_url)
    
    if not match:
        print("[ERROR] Invalid DATABASE_URL format")
        return False
    
    username, password, host, port, database = match.groups()
    
    # Email and password to update
    admin_email = "admin@sufipulse.com"
    plain_password = "Fayazkhan7861$"
    
    # Hash the password using the correct method
    correct_hashed_password = hash_password(plain_password)
    print(f"Updating password for: {admin_email}")
    print(f"New hash: {correct_hashed_password[:50]}...")  # Show first 50 chars
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        cur = conn.cursor()
        
        # Update the admin user's password
        cur.execute("""
            UPDATE users 
            SET password_hash = %s
            WHERE email = %s
        """, (correct_hashed_password, admin_email))
        
        conn.commit()
        
        # Verify the update
        cur.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (admin_email,))
        user = cur.fetchone()
        
        if user:
            print(f"[SUCCESS] Admin user password updated!")
            print(f"User ID: {user[0]}")
            print(f"Email: {user[1]}")
            print(f"Hash starts with: {user[2][:30]}...")
            
            # Test that the new hash can be verified
            from utils.hashing import verify_password
            is_valid = verify_password(plain_password, user[2])
            print(f"Password verification test: {'PASS' if is_valid else 'FAIL'}")
        else:
            print("[ERROR] Could not verify updated user")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not update admin user: {str(e)}")
        return False

if __name__ == "__main__":
    print("Fixing admin user password hash...")
    success = fix_admin_password()
    if success:
        print("\nAdmin user password hash fixed!")
    else:
        print("\nAdmin user password hash fix failed!")