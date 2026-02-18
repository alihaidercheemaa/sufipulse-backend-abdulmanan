import subprocess
import sys

# Run the setup script in a fresh Python process to avoid environment caching
result = subprocess.run([sys.executable, '-c', '''
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import re

# Fresh load of environment
load_dotenv(override=True)

database_url = os.getenv("DATABASE_URL")
print(f"Using DATABASE_URL: {database_url}")

# Parse the database URL
pg_pattern = r"^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$"
match = re.match(pg_pattern, database_url)

if not match:
    print("[ERROR] Invalid DATABASE_URL format")
    exit(1)

username, password, host, port, database = match.groups()
print(f"Connecting to: {host}:{port}, database: {database}")

# Connect to PostgreSQL server (using 'postgres' database as default)
try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        database="postgres",  # Connect to default postgres database
        user=username,
        password=password
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Check if database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database,))
    exists = cur.fetchone()
    
    if not exists:
        print(f"Database \'{database}\' does not exist. Creating it...")
        cur.execute(f\'CREATE DATABASE "{database}" OWNER "{username}"\')
        print(f"Database \'{database}\' created successfully!")
    else:
        print(f"Database \'{database}\' already exists.")
    
    cur.close()
    conn.close()
    
    # Now restore the dump
    import subprocess
    dump_file = "sufipulse.dump"
    
    if not os.path.exists(dump_file):
        print(f"[ERROR] Dump file \'{dump_file}\' not found")
        exit(1)
    
    cmd = [
        "pg_restore",
        "--clean",
        "--if-exists", 
        "--no-owner",
        "--no-privileges",
        f"--host={host}",
        f"--port={port}",
        f"--username={username}",
        f"--dbname={database}",
        "--verbose",
        dump_file
    ]
    
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    
    print("Starting database restore...")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\\n[SUCCESS] Database restored successfully from {dump_file}!")
    else:
        print(f"\\n[ERROR] pg_restore failed with return code {result.returncode}")
        print(f"STDERR: {result.stderr}")
        
        # Try with psql as fallback
        print("\\nTrying with psql as fallback...")
        cmd_psql = [
            "psql",
            f"--host={host}",
            f"--port={port}",
            f"--username={username}",
            f"--dbname={database}",
            f"--file={dump_file}"
        ]
        
        result_psql = subprocess.run(cmd_psql, env=env, capture_output=True, text=True)
        if result_psql.returncode == 0:
            print(f"[SUCCESS] Database restored successfully using psql!")
        else:
            print(f"[ERROR] psql restore also failed: {result_psql.stderr}")
            exit(1)

except psycopg2.Error as e:
    print(f"[ERROR] Database operation failed: {e}")
    # Check if it's a connection issue
    if "Connection refused" in str(e) or "timeout" in str(e).lower():
        print("Make sure PostgreSQL is installed and running on your system.")
        print("On Windows, you might need to start the PostgreSQL service.")
    exit(1)
except FileNotFoundError as e:
    print(f"[ERROR] PostgreSQL client tools not found: {e}")
    print("Please install PostgreSQL and make sure pg_restore and psql are in your PATH")
    exit(1)
'''], capture_output=True, text=True)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)