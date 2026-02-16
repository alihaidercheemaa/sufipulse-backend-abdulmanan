#!/usr/bin/env python3
"""
Update Blog Submissions Status Values
This script updates the status column constraint and existing values in blog_submissions table.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2

def update_blog_status_values():
    """Update status values in blog_submissions table."""
    print("=" * 60)
    print("UPDATING BLOG SUBMISSIONS STATUS VALUES")
    print("=" * 60)

    # Load environment variables
    load_dotenv(dotenv_path='.env')

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL is not set in your .env file")
        return False

    print(f"Using DATABASE_URL: {database_url}")

    # Parse the database URL
    import re
    pg_pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$'
    match = re.match(pg_pattern, database_url)

    if not match:
        print("[ERROR] Invalid DATABASE_URL format")
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
        # First, drop the old constraint
        print("Dropping old status constraint...")
        try:
            cur.execute("ALTER TABLE blog_submissions DROP CONSTRAINT IF EXISTS blog_submissions_status_check;")
            conn.commit()
            print("[OK] Dropped old constraint")
        except Exception as e:
            print(f"Note: {str(e)}")

        # Map old status values to new ones
        print("Updating existing status values...")
        status_mapping = {
            'draft': 'pending',
            'submitted': 'pending',
            'changes_requested': 'revision',
            'admin_approved': 'approved',
            'admin_rejected': 'rejected',
            'final_approved': 'approved',
            'complete_approved': 'approved',
            'posted': 'posted'
        }

        for old_status, new_status in status_mapping.items():
            cur.execute("""
                UPDATE blog_submissions 
                SET status = %s 
                WHERE status = %s
            """, (new_status, old_status))
            conn.commit()
            print(f"  Updated {old_status} -> {new_status}")

        # Add the new constraint
        print("Adding new status constraint...")
        cur.execute("""
            ALTER TABLE blog_submissions 
            ADD CONSTRAINT blog_submissions_status_check 
            CHECK (status IN ('pending', 'review', 'approved', 'revision', 'rejected', 'posted'))
        """)
        conn.commit()
        print("[OK] Added new status constraint")

        print(f"\n[SUCCESS] Status values updated successfully!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to update status values: {str(e)}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def main():
    print("Updating blog submissions status values...")
    return update_blog_status_values()

if __name__ == "__main__":
    success = main()
    if success:
        print("\nStatus values updated successfully!")
    else:
        print("\nStatus update failed!")
        sys.exit(1)