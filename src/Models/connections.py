import psycopg2
import os


def create_connection():
    """
    Create connection to load variable environment
    Return:
        Query: create connection
    """
    return psycopg2.connect(os.environ("DATABASE_URI"))
