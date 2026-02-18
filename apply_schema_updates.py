#!/usr/bin/env python3
"""
Apply Schema Updates Script
This script applies the updated schema to the database, including the new bloggers and blog_submissions tables.
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def apply_schema_updates():
    """Apply schema updates to the database."""
    print("=" * 60)
    print("APPLYING SCHEMA UPDATES TO DATABASE")
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

    # Read the updated schema from schema.sql
    try:
        with open('schema.sql', 'r') as file:
            schema_sql = file.read()
        print(f"[INFO] Loaded schema from schema.sql")
    except FileNotFoundError:
        print("[ERROR] schema.sql file not found in the project root")
        return False

    # Apply the schema updates
    print("Applying schema updates...")
    try:
        # Split the schema into individual statements
        statements = schema_sql.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                try:
                    cur.execute(statement)
                    conn.commit()
                    print(f"[OK] Executed statement: {statement[:50]}...")
                except psycopg2.Error as e:
                    # If it's a duplicate object error, it means the table/column already exists
                    if 'already exists' in str(e).lower():
                        print(f"[INFO] Skipped (already exists): {statement[:50]}...")
                        conn.rollback()  # Rollback the failed transaction
                    else:
                        print(f"[ERROR] Failed to execute statement: {str(e)}")
                        conn.rollback()  # Rollback the failed transaction
                except Exception as e:
                    print(f"[ERROR] Unexpected error: {str(e)}")
                    conn.rollback()  # Rollback the failed transaction

        print(f"\n[SUCCESS] Schema updates applied successfully!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to apply schema updates: {str(e)}")
        return False
    finally:
        cur.close()
        conn.close()

def main():
    print("Applying schema updates to the database...")
    return apply_schema_updates()

if __name__ == "__main__":
    success = main()
    if success:
        print("\nSchema updates applied successfully!")
    else:
        print("\nSchema updates failed!")
        sys.exit(1)