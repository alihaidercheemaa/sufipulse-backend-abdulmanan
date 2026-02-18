import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(database_url)
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM get_cms_page_data('about')")
    result = cursor.fetchone()
    print("SUCCESS!")
    print("Columns:", [desc[0] for desc in cursor.description])
    print("Result:", result)
except Exception as e:
    print("ERROR:", str(e))
finally:
    cursor.close()
    conn.close()
