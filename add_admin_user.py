#!/usr/bin/env python3
"""
Add Admin User Script

This script adds an admin user to the database with a securely hashed password.
It uses the same hashing mechanism as the application (Argon2 via passlib).

Usage:
    python add_admin_user.py
    
    Or with custom credentials:
    python add_admin_user.py --email admin@example.com --password YourPassword123! --name "Admin Name"
"""

import os
import sys
import argparse
import re
from dotenv import load_dotenv

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import psycopg2
from psycopg2.extras import DictCursor
from utils.hashing import hash_password, verify_password


def parse_database_url(database_url: str) -> dict:
    """Parse PostgreSQL database URL into connection parameters."""
    pg_pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$'
    match = re.match(pg_pattern, database_url)

    if not match:
        raise ValueError("Invalid DATABASE_URL format. Expected: postgresql://user:pass@host:port/dbname")

    username, password, host, port, database = match.groups()
    return {
        "host": host,
        "port": int(port),
        "database": database,
        "user": username,
        "password": password
    }


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def add_admin_user(email: str, password: str, name: str, 
                   country: str = "Pakistan", city: str = "Karachi") -> bool:
    """
    Add an admin user to the database with a hashed password.
    
    Args:
        email: Admin user's email address
        password: Plain text password (will be hashed)
        name: Admin user's name
        country: Country (default: Pakistan)
        city: City (default: Karachi)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Load environment variables
    load_dotenv(override=True)

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL is not set in your .env file")
        print("Please copy .env.example to .env and configure your database connection.")
        return False

    # Validate email
    if not validate_email(email):
        print(f"[ERROR] Invalid email format: {email}")
        return False

    # Validate password
    is_valid, error_msg = validate_password(password)
    if not is_valid:
        print(f"[ERROR] {error_msg}")
        return False

    # Parse the database URL
    try:
        db_params = parse_database_url(database_url)
    except ValueError as e:
        print(f"[ERROR] {str(e)}")
        return False

    # Hash the password using Argon2
    print(f"Hashing password using Argon2...")
    hashed_password = hash_password(password)
    print(f"Password hashed successfully: {hashed_password[:50]}...")

    try:
        # Connect to the database
        print(f"\nConnecting to database: {db_params['database']}@{db_params['host']}")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Check if user already exists
        cur.execute("SELECT id, email, role FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            print(f"\n[WARNING] User with email '{email}' already exists!")
            print(f"User ID: {existing_user[0]}, Role: {existing_user[2]}")
            
            # Ask for confirmation to update
            choice = input("\nDo you want to update this user to admin role? (y/n): ").strip().lower()
            if choice != 'y':
                print("Operation cancelled.")
                cur.close()
                conn.close()
                return False
            
            # Update existing user to admin
            cur.execute("""
                UPDATE users
                SET password_hash = %s, 
                    name = %s,
                    role = 'admin',
                    country = %s,
                    city = %s,
                    is_registered = TRUE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE email = %s
                RETURNING id, email, name, role, country, city, is_registered, created_at
            """, (hashed_password, name, country, city, email))
            
            conn.commit()
            user = cur.fetchone()
            print(f"\n[SUCCESS] Admin user updated!")
            
        else:
            # Create new admin user
            print(f"\nCreating new admin user: {email}")
            cur.execute("""
                INSERT INTO users (email, name, password_hash, role, country, city, is_registered)
                VALUES (%s, %s, %s, 'admin', %s, %s, TRUE)
                RETURNING id, email, name, role, country, city, is_registered, created_at
            """, (email, name, hashed_password, country, city))
            
            conn.commit()
            user = cur.fetchone()
            print(f"\n[SUCCESS] Admin user created!")

        # Display user information
        print("\n" + "=" * 60)
        print("ADMIN USER INFORMATION")
        print("=" * 60)
        print(f"User ID:        {user[0]}")
        print(f"Email:          {user[1]}")
        print(f"Name:           {user[2]}")
        print(f"Role:           {user[3]}")
        print(f"Country:        {user[4]}")
        print(f"City:           {user[5]}")
        print(f"Is Registered:  {user[6]}")
        print(f"Created At:     {user[7]}")
        print("=" * 60)
        print(f"\nCredentials for login:")
        print(f"  Email:    {email}")
        print(f"  Password: {password}")
        print("=" * 60)

        # Verify the password hash works
        print("\nVerifying password hash...")
        cur.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        stored_hash = cur.fetchone()[0]
        is_valid = verify_password(password, stored_hash)
        print(f"Password verification test: {'✓ PASS' if is_valid else '✗ FAIL'}")

        cur.close()
        conn.close()

        return True

    except psycopg2.IntegrityError as e:
        print(f"[ERROR] Database integrity error: {str(e)}")
        return False
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Database connection error: {str(e)}")
        print("Please check your DATABASE_URL and ensure the database is running.")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Add an admin user to the database with a hashed password.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python add_admin_user.py
  python add_admin_user.py --email admin@example.com --password SecurePass123! --name "Admin User"
  python add_admin_user.py -e admin@example.com -p SecurePass123! -n "Admin User" -c "Pakistan" -C "Lahore"
        """
    )
    
    parser.add_argument(
        "-e", "--email",
        type=str,
        default="admin@sufipulse.com",
        help="Admin user email (default: admin@sufipulse.com)"
    )
    
    parser.add_argument(
        "-p", "--password",
        type=str,
        default="Fayazkhan7861$",
        help="Admin user password (default: Fayazkhan7861$)"
    )
    
    parser.add_argument(
        "-n", "--name",
        type=str,
        default="Admin User",
        help="Admin user name (default: Admin User)"
    )
    
    parser.add_argument(
        "-c", "--country",
        type=str,
        default="Pakistan",
        help="Country (default: Pakistan)"
    )
    
    parser.add_argument(
        "-C", "--city",
        type=str,
        default="Karachi",
        help="City (default: Karachi)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("ADD ADMIN USER SCRIPT")
    print("=" * 60)
    print(f"\nConfiguration:")
    print(f"  Email:     {args.email}")
    print(f"  Name:      {args.name}")
    print(f"  Country:   {args.country}")
    print(f"  City:      {args.city}")
    print()

    success = add_admin_user(
        email=args.email,
        password=args.password,
        name=args.name,
        country=args.country,
        city=args.city
    )

    if success:
        print("\n✓ Admin user setup completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Admin user setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
