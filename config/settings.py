from dotenv import load_dotenv
import os
# Load environment variables from the .env file in the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Default to localhost if not specified in environment
HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', '8000')


# Database configuration - load from environment variables
DB_HOST = os.getenv('DB_HOST', os.getenv('DATABASE_HOST', 'localhost'))
DB_NAME = os.getenv('DB_NAME', os.getenv('DATABASE_NAME', os.getenv('DATABASE')))
DB_USER = os.getenv('DB_USER', os.getenv('DATABASE_USER', os.getenv('USER')))
DB_PASSWORD = os.getenv('DB_PASSWORD', os.getenv('DATABASE_PASSWORD', os.getenv('PASSWORD')))
DB_PORT = int(os.getenv('DB_PORT', os.getenv('DATABASE_PORT', '5432')))

DATABASE_CONFIG = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "port": DB_PORT,
}
