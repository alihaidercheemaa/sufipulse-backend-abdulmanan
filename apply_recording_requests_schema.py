#!/usr/bin/env python3
"""
Script to apply the recording requests schema updates to the database.
This creates the new tables for studio and remote recording requests.
"""

import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create and return a database connection"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "sufipulse"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

def apply_schema_updates():
    """Apply the recording requests schema updates"""
    print("🔄 Applying recording requests schema updates...")
    
    # Read the SQL file
    sql_file_path = os.path.join(os.path.dirname(__file__), "sql", "recording_requests_schema.sql")
    
    if not os.path.exists(sql_file_path):
        print(f"❌ SQL file not found: {sql_file_path}")
        return False
    
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the SQL script
        print("📝 Executing SQL script...")
        cursor.execute(sql_content)
        
        # Commit the changes
        conn.commit()
        
        print("✅ Schema updates applied successfully!")
        print("\n📊 Created tables:")
        print("   - studio_recording_requests")
        print("   - remote_recording_requests_new")
        print("\n📊 Created indexes:")
        print("   - idx_studio_recording_vocalist_id")
        print("   - idx_studio_recording_kalam_id")
        print("   - idx_studio_recording_status")
        print("   - idx_studio_recording_created_at")
        print("   - idx_remote_recording_new_vocalist_id")
        print("   - idx_remote_recording_new_kalam_id")
        print("   - idx_remote_recording_new_status")
        print("   - idx_remote_recording_new_created_at")
        print("\n📊 Created functions:")
        print("   - get_approved_unassigned_kalams()")
        print("   - update_lyric_status_on_request_approval()")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success = apply_schema_updates()
    if success:
        print("\n🎉 Recording requests schema setup complete!")
    else:
        print("\n💥 Schema setup failed. Please check the errors above.")
        exit(1)
