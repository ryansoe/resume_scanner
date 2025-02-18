import psycopg2
from psycopg2.extras import RealDictCursor
import os

DATABASE_URL = "postgresql://resume_user:password@localhost/resume_db"

def get_db_connection():
    """Establish connection to PostgreSQL database."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None