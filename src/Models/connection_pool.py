import os
from contextlib import contextmanager

#  Database
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

"""
    Create connection to load variable environment
    Return:
        Query: create connection
"""
DATABASE_PROMPT = "Enter the database_uri value or leave empty to load from .env file: "

database_uri = input(DATABASE_PROMPT)
if not database_uri:
    load_dotenv()
    database_uri = os.environ["DATABASE_URI"]

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_uri)

#  Context manager
@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        #  Call
        yield connection
    finally:
        pool.putconn(connection)
