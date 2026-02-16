import subprocess
import os
from dotenv import load_dotenv

# Load environment
load_dotenv(override=True)
database_url = os.getenv("DATABASE_URL")

# Parse the database URL
import re
pg_pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$'
match = re.match(pg_pattern, database_url)

if not match:
    print("[ERROR] Invalid DATABASE_URL format")
    exit(1)

username, password, host, port, database = match.groups()

print(f"Restoring to database: {database} on {host}:{port}")

# Try to restore with more compatible options
cmd = [
    'pg_restore',
    '--verbose',
    '--host', host,
    '--port', port,
    '--username', username,
    '--dbname', database,
    '--no-owner',
    '--no-privileges',
    'sufipulse.dump'
]

env = os.environ.copy()
env['PGPASSWORD'] = password

print("Running command:", ' '.join(cmd))
result = subprocess.run(cmd, env=env, capture_output=True, text=True)

if result.returncode == 0:
    print("[SUCCESS] Database restored successfully!")
    print(result.stdout[-500:])  # Show last 500 chars of output
else:
    print(f"[ERROR] pg_restore failed with return code {result.returncode}")
    print("STDOUT:", result.stdout[-1000:])  # Show last 1000 chars of stdout
    print("STDERR:", result.stderr[:1000])   # Show first 1000 chars of stderr
    
    # Alternative: Convert to SQL and import
    print("\nTrying to convert dump to SQL format first...")
    sql_convert_cmd = [
        'pg_restore',
        '--clean',
        '--if-exists',
        '--no-owner',
        '--no-privileges',
        '--file', 'temp_dump.sql',
        'sufipulse.dump'
    ]
    
    convert_result = subprocess.run(sql_convert_cmd, env=env, capture_output=True, text=True)
    if convert_result.returncode == 0:
        print("Converted dump to SQL format successfully")
        
        # Now import the SQL file
        import_cmd = [
            'psql',
            f'--host={host}',
            f'--port={port}',
            f'--username={username}',
            f'--dbname={database}',
            f'--file=temp_dump.sql'
        ]
        
        import_result = subprocess.run(import_cmd, env=env, capture_output=True, text=True)
        if import_result.returncode == 0:
            print("[SUCCESS] Database imported from converted SQL file!")
            # Clean up temp file
            os.remove('temp_dump.sql')
        else:
            print(f"[ERROR] Import from SQL failed: {import_result.stderr}")
    else:
        print(f"[ERROR] Conversion to SQL failed: {convert_result.stderr}")