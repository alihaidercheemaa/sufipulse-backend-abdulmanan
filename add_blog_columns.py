#!/usr/bin/env python3
"""
Add New Columns to Blog Submissions Table
This script adds the new category, tags, and language columns to the blog_submissions table.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2

def add_columns_to_blog_submissions():
    """Add new columns to the blog_submissions table."""
    print("=" * 60)
    print("ADDING NEW COLUMNS TO BLOG_SUBMISSIONS TABLE")
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
        # Check if columns already exist
        print("Checking if columns already exist...")
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'blog_submissions'
            AND column_name IN ('category', 'tags', 'language');
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        print(f"Existing columns: {existing_columns}")

        # Add category column if it doesn't exist
        if 'category' not in existing_columns:
            print("Adding category column...")
            cur.execute("ALTER TABLE blog_submissions ADD COLUMN category VARCHAR(100);")
            print("[OK] Added category column")
        else:
            print("Category column already exists, skipping...")

        # Add tags column if it doesn't exist
        if 'tags' not in existing_columns:
            print("Adding tags column...")
            cur.execute("ALTER TABLE blog_submissions ADD COLUMN tags TEXT[] DEFAULT '{}';")
            print("[OK] Added tags column")
        else:
            print("Tags column already exists, skipping...")

        # Add language column if it doesn't exist
        if 'language' not in existing_columns:
            print("Adding language column...")
            cur.execute("ALTER TABLE blog_submissions ADD COLUMN language VARCHAR(50);")
            print("[OK] Added language column")
        else:
            print("Language column already exists, skipping...")

        # Add indexes for the new columns if they don't exist
        print("Checking if indexes exist...")
        
        # Check for category index
        cur.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'blog_submissions' AND indexname = 'idx_blog_submissions_category';
        """)
        if not cur.fetchone():
            print("Adding index for category column...")
            cur.execute("CREATE INDEX idx_blog_submissions_category ON blog_submissions(category);")
            print("[OK] Added index for category column")
        else:
            print("Category index already exists, skipping...")

        # Check for language index
        cur.execute("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'blog_submissions' AND indexname = 'idx_blog_submissions_language';
        """)
        if not cur.fetchone():
            print("Adding index for language column...")
            cur.execute("CREATE INDEX idx_blog_submissions_language ON blog_submissions(language);")
            print("[OK] Added index for language column")
        else:
            print("Language index already exists, skipping...")

        conn.commit()
        print(f"\n[SUCCESS] All columns and indexes added successfully!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to add columns: {str(e)}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def main():
    print("Adding new columns to blog_submissions table...")
    return add_columns_to_blog_submissions()

if __name__ == "__main__":
    success = main()
    if success:
        print("\nColumns added successfully!")
    else:
        print("\nColumn addition failed!")
        sys.exit(1)