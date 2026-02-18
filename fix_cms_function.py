"""
Fix the get_cms_page_data function
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(database_url)
cursor = conn.cursor()

try:
    # Drop old function
    cursor.execute("DROP FUNCTION IF EXISTS get_cms_page_data(VARCHAR)")
    conn.commit()
    print("[OK] Dropped old function")
    
    # Read and execute the fixed schema
    with open("sql/cms_pages_schema.sql", "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    cursor.execute(schema_sql)
    conn.commit()
    print("[OK] Recreated function with fixes")
    
    # Test it
    cursor.execute("SELECT * FROM get_cms_page_data('about')")
    result = cursor.fetchone()
    print("[OK] Function works! Returned page:", result[1] if result else "None")
    
except Exception as e:
    print("[ERROR]", str(e))
    conn.rollback()
finally:
    cursor.close()
    conn.close()
