#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
    database=os.getenv("DB_NAME", "sufipulse"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

print("Fixing recording schema for blogs...")

# Fix studio_recording_requests
try:
    cursor.execute("""
        ALTER TABLE studio_recording_requests 
        DROP CONSTRAINT IF EXISTS studio_recording_requests_kalam_id_fkey;
    """)
    print("Dropped kalam_id FK from studio_recording_requests")
except Exception as e:
    print(f"Note: {e}")

try:
    cursor.execute("""
        ALTER TABLE studio_recording_requests 
        ADD COLUMN IF NOT EXISTS blog_id INT REFERENCES blog_submissions(id) ON DELETE CASCADE;
    """)
    print("Added blog_id column to studio_recording_requests")
except Exception as e:
    print(f"Note: {e}")

try:
    cursor.execute("""
        ALTER TABLE studio_recording_requests 
        ALTER COLUMN kalam_id DROP NOT NULL;
    """)
    print("Made kalam_id nullable in studio_recording_requests")
except Exception as e:
    print(f"Note: {e}")

# Fix remote_recording_requests_new
try:
    cursor.execute("""
        ALTER TABLE remote_recording_requests_new 
        DROP CONSTRAINT IF EXISTS remote_recording_requests_new_kalam_id_fkey;
    """)
    print("Dropped kalam_id FK from remote_recording_requests_new")
except Exception as e:
    print(f"Note: {e}")

try:
    cursor.execute("""
        ALTER TABLE remote_recording_requests_new 
        ADD COLUMN IF NOT EXISTS blog_id INT REFERENCES blog_submissions(id) ON DELETE CASCADE;
    """)
    print("Added blog_id column to remote_recording_requests_new")
except Exception as e:
    print(f"Note: {e}")

try:
    cursor.execute("""
        ALTER TABLE remote_recording_requests_new 
        ALTER COLUMN kalam_id DROP NOT NULL;
    """)
    print("Made kalam_id nullable in remote_recording_requests_new")
except Exception as e:
    print(f"Note: {e}")

conn.commit()
cursor.close()
conn.close()

print("\nSchema fixed successfully!")
print("Now update the backend code to use blog_id instead of kalam_id")
