"""
Recreate only the get_cms_page_data function
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
    
    # Read just the function part from schema
    with open("sql/cms_pages_schema.sql", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find and extract the function definition
    start_marker = "-- Function to get complete page data"
    end_marker = "COMMENT ON FUNCTION get_cms_page_data"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        function_sql = content[start_idx:end_idx + len("COMMENT ON FUNCTION get_cms_page_data IS 'Retrieve complete page data including all sections, stats, team, timeline, values, testimonials, sections, and hubs';")]
        
        cursor.execute(function_sql)
        conn.commit()
        print("[OK] Recreated function with fixes")
        
        # Test it
        cursor.execute("SELECT * FROM get_cms_page_data('about')")
        result = cursor.fetchone()
        print("[OK] Function works! Returned page:", result[1] if result else "None")
        print("[OK] Columns:", [desc[0] for desc in cursor.description])
    else:
        print("[ERROR] Could not find function definition in schema file")
    
except Exception as e:
    print("[ERROR]", str(e))
    conn.rollback()
finally:
    cursor.close()
    conn.close()
