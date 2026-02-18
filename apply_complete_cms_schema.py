"""
Apply Complete CMS Schema for All 20 Pages
This script creates all CMS tables and inserts seed data for ALL 20 pages.
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def apply_complete_cms_schema():
    """Apply complete CMS schema for all 20 pages"""
    
    print("[CMS] Starting Complete CMS Schema Application...")
    print("[CMS] This will create tables and add ALL 20 pages\n")
    
    try:
        # Get database URL from environment
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("[ERROR] DATABASE_URL not found in .env file")
            return
        
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("[OK] Connected to database")
        
        # Step 1: Apply main schema (creates tables + first 7 pages)
        print("\n[CMS] Applying main CMS schema...")
        with open("sql/cms_pages_schema.sql", "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.execute(schema_sql)
        conn.commit()
        print("[OK] Main schema applied (7 pages)")
        
        # Step 2: Add remaining 13 pages
        print("\n[CMS] Adding remaining 13 pages...")
        with open("sql/cms_add_all_20_pages.sql", "r", encoding="utf-8") as f:
            add_pages_sql = f.read()
        cursor.execute(add_pages_sql)
        conn.commit()
        print("[OK] Additional pages added (13 pages)")
        
        # Verify total pages
        cursor.execute("SELECT COUNT(*) FROM cms_pages")
        total_pages = cursor.fetchone()[0]
        print(f"\n[OK] Total pages in database: {total_pages}")
        
        # List all pages
        cursor.execute("""
            SELECT id, page_name, page_slug, is_active 
            FROM cms_pages 
            ORDER BY id
        """)
        pages = cursor.fetchall()
        
        print("\n[CMS] All CMS Pages:")
        print("=" * 80)
        print(f"{'ID':<4} {'Page Name':<30} {'Slug':<30} {'Status':<8}")
        print("=" * 80)
        for page in pages:
            status = "Active" if page[3] else "Inactive"
            print(f"{page[0]:<4} {page[1]:<30} {page[2]:<30} {status:<8}")
        print("=" * 80)
        
        cursor.close()
        conn.close()
        
        print("\n[SUCCESS] Complete CMS Setup Finished!")
        print("\n*** ALL 20 pages are now in the database! ***")
        print("\nNext Steps:")
        print("   1. Restart backend server: python main.py")
        print("   2. Go to: http://localhost:3000/admin/cms")
        print("   3. You should now see ALL 20 pages!")
        print("   4. Edit any page to manage its content")
        
    except psycopg2.Error as e:
        print(f"\n[ERROR] Database error: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError as e:
        print(f"\n[ERROR] Schema file not found: {e}")
        print("   Make sure you're running from sufipulse-backend-talhaadil directory")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    apply_complete_cms_schema()
