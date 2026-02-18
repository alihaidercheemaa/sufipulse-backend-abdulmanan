"""
Script to create the youtube_videos table in the database.
Run this script to fix the 'relation youtube_videos does not exist' error.
"""

import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("Database URL:", DATABASE_URL)
print("\n--- Creating youtube_videos Table ---\n")

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    print("[OK] Connected to database")
    
    # Read the SQL file
    with open("create_youtube_videos_table.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    
    # Execute the SQL
    with conn.cursor() as cur:
        cur.execute(sql)
        print("[OK] Executed SQL commands")
    
    # Commit the changes
    conn.commit()
    print("[OK] Changes committed")
    
    # Verify the table was created
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = 'youtube_videos'
        """)
        result = cur.fetchone()
        
        if result:
            print("\n[SUCCESS] youtube_videos table created successfully!")
            
            # Show table structure
            cur.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'youtube_videos'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            print("\nTable structure:")
            print("-" * 60)
            for col in columns:
                print(f"  {col[0]:20} {col[1]:25} {col[2]}")
            print("-" * 60)
        else:
            print("\n[ERROR] Table was not created")
    
    conn.close()
    print("\n[OK] Connection closed")
    
except psycopg2.Error as e:
    print(f"\n[ERROR] Database error: {e}")
except FileNotFoundError:
    print("\n[ERROR] SQL file not found. Make sure create_youtube_videos_table.sql exists.")
except Exception as e:
    print(f"\n[ERROR] Unexpected error: {e}")

print("\n--- Script Complete ---")
