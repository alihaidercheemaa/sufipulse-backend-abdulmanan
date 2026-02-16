#!/usr/bin/env python3
"""
Database Setup Script
This script creates the local database and then restores the dump file.
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
    load_dotenv(dotenv_path='.env')
    
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

def restore_database():
    """Restore the database from the dump file."""
    print("=" * 60)
    print("DATABASE RESTORE FROM DUMP")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv(dotenv_path='.env')
    
    # Get database configuration from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("[ERROR] DATABASE_URL is not set in your .env file")
        print("Please make sure your .env file contains the DATABASE_URL variable")
        return False
    
    print(f"Using DATABASE_URL: {database_url}")
    
    # Extract database info from URL for validation
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
    
    # Check if dump file exists
    dump_file = "sufipulse.dump"
    if not os.path.exists(dump_file):
        print(f"[ERROR] Dump file '{dump_file}' not found in the project root")
        return False
    
    print(f"[INFO] Found dump file: {dump_file}")
    print(f"[INFO] File size: {os.path.getsize(dump_file)} bytes")
    print()
    
    # Test connection to database first
    print("Testing database connection...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"[OK] Connected to database successfully!")
        print(f"Server version: {version[0]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Could not connect to database: {str(e)}")
        return False
    
    print()
    print("Starting database restore...")
    print("This may take a few moments...")
    
    try:
        # Use pg_restore to restore the dump
        cmd = [
            'pg_restore',
            '--clean',  # Drop database objects before recreating them
            '--if-exists',  # Use IF EXISTS when dropping objects
            '--no-owner',  # Don't restore ownership
            '--no-privileges',  # Don't restore privileges
            '--host', host,
            '--port', port,
            '--username', username,
            '--dbname', database,
            '--verbose',
            dump_file
        ]
        
        # Set PGPASSWORD environment variable for authentication
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n[SUCCESS] Database restored successfully from {dump_file}!")
            return True
        else:
            print(f"\n[ERROR] pg_restore failed with return code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except FileNotFoundError:
        # pg_restore not found, try alternative approach with psql
        print("[WARNING] pg_restore command not found. Trying alternative method...")
        
        try:
            cmd = [
                'psql',
                '--host', host,
                '--port', port,
                '--username', username,
                '--dbname', database,
                '--file', dump_file
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"\n[SUCCESS] Database restored successfully using psql!")
                return True
            else:
                print(f"\n[ERROR] psql restore failed with return code {result.returncode}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                print("\n[INFO] Make sure PostgreSQL client tools (pg_restore, psql) are installed and in your PATH")
                return False
                
        except FileNotFoundError:
            print("[ERROR] Neither pg_restore nor psql found in your system PATH")
            print("Please install PostgreSQL client tools to restore the database dump")
            print("On Windows, install PostgreSQL and make sure the bin directory is in your PATH")
            print("On Ubuntu/Debian: sudo apt-get install postgresql-client")
            print("On macOS: brew install libpq")
            return False

def main():
    print("Setting up local database...")
    
    # First, create the database if it doesn't exist
    if not create_database_if_not_exists():
        print("Failed to create database. Exiting.")
        return False
    
    # Then restore the dump
    return restore_database()

if __name__ == "__main__":
    success = main()
    if success:
        print("\nDatabase setup and restore completed successfully!")
    else:
        print("\nDatabase setup and restore failed!")
        sys.exit(1)