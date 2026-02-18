"""
Export PostgreSQL database schema (no data) to a SQL file.
"""
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection details
database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("[ERROR] DATABASE_URL is not set in your .env file")
    exit(1)

# Parse DATABASE_URL
import re
pg_pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$'
match = re.match(pg_pattern, database_url)

if not match:
    print("[ERROR] Invalid DATABASE_URL format")
    print("Expected format: postgresql://username:password@host:port/database")
    exit(1)

username, password, host, port, database = match.groups()

print(f"Database: {database}")
print(f"Host: {host}:{port}")
print(f"User: {username}")

# Set PGPASSWORD environment variable
env = os.environ.copy()
env['PGPASSWORD'] = password

# Output file
output_file = "schema_dump.sql"

# Run pg_dump with --schema-only flag
cmd = [
    "pg_dump",
    "--schema-only",
    "-h", host,
    "-p", port,
    "-U", username,
    "-d", database,
    "-f", output_file
]

print(f"\nRunning: {' '.join(cmd)}")
print(f"Output will be saved to: {output_file}")

try:
    result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
    print("\n[SUCCESS] Schema exported successfully!")
    print(f"Output file: {output_file}")
except subprocess.CalledProcessError as e:
    print(f"\n[ERROR] Error exporting schema: {e}")
    print(f"stderr: {e.stderr}")
    exit(1)
except FileNotFoundError:
    print("\n[ERROR] pg_dump not found!")
    print("Please ensure PostgreSQL is installed and pg_dump is in your PATH.")
    print("On Windows, add PostgreSQL bin directory to PATH (e.g., C:\\Program Files\\PostgreSQL\\15\\bin)")
    exit(1)
