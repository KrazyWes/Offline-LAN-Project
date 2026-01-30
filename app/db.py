# db.py
import psycopg2  # type: ignore[reportMissingImports]
from psycopg2 import OperationalError  # type: ignore[reportMissingImports]
import config  # Import your settings from config.py

def get_connection():
    """Returns a connection object to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS,
            port=config.DB_PORT,
            connect_timeout=5  # Prevents app hanging on bad Wi-Fi
        )
        print(f"Connected to {config.DB_HOST} successfully!")
        return conn
    except OperationalError as e:
        print(f"Error: Could not connect to the database.\n{e}")
        return None

def fetch_data(query):
    """Example helper function to run a query."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []
