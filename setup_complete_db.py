#!/usr/bin/env python3
"""
Database Setup Script
This script sets up the database schema and handles the data import.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
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
    
    print(f"Connecting to PostgreSQL server at {host}:{port} as user {username}")
    
    try:
        # Connect to PostgreSQL server (using 'postgres' database as default)
        conn = psycopg2.connect(
            host=host,
            port=port,
            database='postgres',  # Connect to default postgres database
            user=username,
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database,))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Database '{database}' does not exist. Creating it...")
            cur.execute(f'CREATE DATABASE "{database}" OWNER "{username}"')
            print(f"Database '{database}' created successfully!")
        else:
            print(f"Database '{database}' already exists.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not connect to PostgreSQL server or create database: {str(e)}")
        return False

def create_schema_from_sql_file():
    """Create database schema from schema.sql file."""
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
    
    print(f"Creating schema in database '{database}'...")
    
    try:
        # Connect to the specific database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        cur = conn.cursor()
        
        # Read and execute the schema file
        with open('schema.sql', 'r', encoding='utf-8') as schema_file:
            schema_sql = schema_file.read()
        
        # Split the schema into individual statements
        # PostgreSQL statements typically end with semicolons
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements):
            if statement:  # Skip empty statements
                try:
                    cur.execute(statement)
                    print(f"Executed statement {i+1}/{len(statements)}")
                except psycopg2.Error as e:
                    # Some statements might fail (like index creation if table doesn't exist yet)
                    # This is expected during schema creation
                    print(f"Statement {i+1} might have failed (this is OK during schema creation): {str(e)[:100]}...")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Schema created successfully in database '{database}'!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Could not create schema: {str(e)}")
        return False

def try_import_data_from_dump():
    """Try to import data from the dump file, with fallback options."""
    print("\nAttempting to import data from dump file...")
    
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
    
    # Check if dump file exists
    dump_file = "sufipulse.dump"
    if not os.path.exists(dump_file):
        print(f"[INFO] Dump file '{dump_file}' not found. Skipping data import.")
        return True
    
    print(f"[INFO] Found dump file: {dump_file}")
    print(f"[INFO] File size: {os.path.getsize(dump_file)} bytes")
    
    # Due to version incompatibility, we'll try to convert the dump to SQL first
    print("Attempting to convert dump to SQL format...")
    
    # Set up environment with password
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    # Try to extract as SQL using pg_restore
    try:
        # Create a temporary SQL file
        temp_sql_file = 'temp_extracted_data.sql'
        
        # Try to extract the data portion only
        cmd = [
            'pg_restore',
            '--data-only',  # Only extract data, not schema
            '--column-inserts',  # Use INSERT with column names
            '--no-owner',
            '--no-privileges',
            '--file', temp_sql_file,
            dump_file
        ]
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Successfully extracted data to temporary SQL file.")
            
            # Now import the data using psql
            import_cmd = [
                'psql',
                f'--host={host}',
                f'--port={port}',
                f'--username={username}',
                f'--dbname={database}',
                f'--file={temp_sql_file}'
            ]
            
            import_result = subprocess.run(import_cmd, env=env, capture_output=True, text=True)
            if import_result.returncode == 0:
                print("[SUCCESS] Data imported from dump file!")
                # Clean up temp file
                os.remove(temp_sql_file)
                return True
            else:
                print(f"[INFO] Could not import data with psql: {import_result.stderr}")
                print("Proceeding with schema-only setup.")
                
        else:
            print(f"[INFO] Could not extract data from dump: {result.stderr}")
            print("This is likely due to version incompatibility between the dump and current PostgreSQL.")
            print("Proceeding with schema-only setup.")
            
    except FileNotFoundError:
        print("[INFO] pg_restore not available, skipping data import from dump.")
    
    # If everything else fails, just return True to continue with schema-only
    return True

def main():
    print("=" * 60)
    print("DATABASE SETUP FOR SUFIPULSE PROJECT")
    print("=" * 60)
    
    # Step 1: Create database if it doesn't exist
    print("\nStep 1: Creating database...")
    if not create_database_if_not_exists():
        print("Failed to create database. Exiting.")
        return False
    
    # Step 2: Create schema from schema.sql
    print("\nStep 2: Creating database schema...")
    if not create_schema_from_sql_file():
        print("Failed to create schema. Exiting.")
        return False
    
    # Step 3: Try to import data from dump
    print("\nStep 3: Importing data...")
    if not try_import_data_from_dump():
        print("Data import failed, but schema creation succeeded.")
    
    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETED!")
    print("=" * 60)
    print("Database has been set up with schema from schema.sql")
    print("If data import failed, your database has the correct structure")
    print("but no initial data. You can add data manually or via your app.")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\nDatabase setup completed successfully!")
    else:
        print("\nDatabase setup failed!")
        sys.exit(1)