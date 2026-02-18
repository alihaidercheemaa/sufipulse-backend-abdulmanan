"""
Apply CMS Pages Schema to Database
This script creates all CMS tables and seed data for the SufiPulse platform.
"""

import psycopg2
from psycopg2 import sql
from db.config import DB_CONFIG

def apply_cms_schema():
    """Apply CMS schema to database"""
    
    print("🔧 Starting CMS Schema Application...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        
        print("✅ Connected to database")
        
        # Read schema file
        with open("sql/cms_pages_schema.sql", "r", encoding="utf-8") as f:
            schema_sql = f.read()
        
        print("📄 Schema file loaded")
        
        # Execute schema
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ CMS Schema applied successfully!")
        print("📊 Seed data inserted")
        
        # Verify tables created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'cms%'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print("\n📋 Created Tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Verify function created
        cursor.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'public' 
            AND routine_name LIKE 'get_cms%'
        """)
        
        functions = cursor.fetchall()
        print("\n⚙️  Created Functions:")
        for func in functions:
            print(f"   - {func[0]}")
        
        # Count seeded pages
        cursor.execute("SELECT COUNT(*) FROM cms_pages")
        page_count = cursor.fetchone()[0]
        print(f"\n📄 Seeded {page_count} pages")
        
        cursor.close()
        conn.close()
        
        print("\n✅ CMS Setup Complete!")
        print("\n📝 Next Steps:")
        print("   1. Access admin panel at /admin/cms")
        print("   2. Manage page content through CMS interface")
        print("   3. Pages will automatically use database content")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError:
        print("❌ Schema file not found. Make sure sql/cms_pages_schema.sql exists.")
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    apply_cms_schema()
