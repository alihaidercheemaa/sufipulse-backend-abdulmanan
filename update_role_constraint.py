#!/usr/bin/env python3
"""
Fix Database Constraint Script
This script updates the users table role constraint to include 'blogger'.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2

def update_role_constraint():
    """Update the role constraint in the users table to include 'blogger'."""
    print("=" * 60)
    print("UPDATING USER ROLE CONSTRAINT TO INCLUDE 'blogger'")
    print("=" * 60)

    # Load environment variables
    load_dotenv(dotenv_path='.env')

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL is not set in your .env file")
        print("Please make sure your .env file contains the DATABASE_URL variable")
        return False

    print(f"Using DATABASE_URL: {database_url}")

    # Parse the database URL
    import re
    pg_pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$'
    match = re.match(pg_pattern, database_url)

    if not match:
        print("[ERROR] Invalid DATABASE_URL format")
        print("Expected format: postgresql://username:password@host:port/database")
        return False

    username, password, host, port, database = match.groups()

    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    print()

    # Connect to the database
    print("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        cur = conn.cursor()
        print("[OK] Connected to database successfully!")
    except Exception as e:
        print(f"[ERROR] Could not connect to database: {str(e)}")
        return False

    try:
        # First, let's check the current constraint
        print("Checking current role constraint...")
        cur.execute("""
            SELECT conname, pg_get_constraintdef(oid) 
            FROM pg_constraint 
            WHERE conrelid = 'users'::regclass AND contype = 'c'
        """)
        constraints = cur.fetchall()
        
        print("Current constraints on users table:")
        for constraint in constraints:
            print(f"  {constraint[0]}: {constraint[1]}")
        
        # Update the constraint to include 'blogger'
        print("\nUpdating role constraint to include 'blogger'...")
        try:
            # Drop the old constraint
            cur.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS users_role_check;")
            print("[OK] Dropped old constraint")
            
            # Create the new constraint with 'blogger' included
            cur.execute("""
                ALTER TABLE users 
                ADD CONSTRAINT users_role_check 
                CHECK (role IN ('writer', 'vocalist', 'blogger', 'admin'));
            """)
            print("[OK] Added new constraint with 'blogger' role")
            
            conn.commit()
            print(f"\n[SUCCESS] Role constraint updated successfully!")
            return True
            
        except psycopg2.Error as e:
            print(f"[ERROR] Failed to update constraint: {str(e)}")
            conn.rollback()
            return False

    except Exception as e:
        print(f"[ERROR] Failed to update role constraint: {str(e)}")
        return False
    finally:
        cur.close()
        conn.close()

def main():
    print("Updating user role constraint to include 'blogger'...")
    return update_role_constraint()

if __name__ == "__main__":
    success = main()
    if success:
        print("\nRole constraint updated successfully!")
    else:
        print("\nRole constraint update failed!")
        sys.exit(1)