import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager

# Load environment variables from .env file
load_dotenv()

print("DATABASE_URL:", os.getenv("DATABASE_URL"))

class DBConnection:
    """
    Provides database connection functionality.
    Note: For production use, consider using a connection pool like psycopg2.pool.
    """
    
    @classmethod
    def get_connection(cls):
        """Returns a new database connection for each request to avoid sharing issues."""
        try:
            database_url = os.getenv("DATABASE_URL")
            print("Attempting to connect with DATABASE_URL:", database_url)
            conn = psycopg2.connect(
                database_url,
                cursor_factory=DictCursor
            )
            print("Database connected.")
            return conn
        except psycopg2.Error as e:
            print("Error connecting to database:", e)
            raise e

    @classmethod
    @contextmanager
    def get_db_connection(cls):
        """Context manager for database connections that ensures proper cleanup."""
        conn = cls.get_connection()
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
