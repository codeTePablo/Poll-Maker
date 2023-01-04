# Testing connection  
import os
import psycopg2
from dotenv import load_dotenv

# not able to use env 
load_dotenv() # environment variables
# able to use env

# connection = psycopg2.connect(os.environ["DATABASE_URL"]) # protect URL and User

# DDL
CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls 
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);""" 
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options 
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, 
FOREIGN KEY(poll_id) REFERENCES polls(id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER,
FOREIGN KEY(option_id) REFERENCES options(id));"""

# DML
SELECT_ALL_POLLS = """SELECT * FORM polls;"""
SELECT_POLL_WITH_OPTIONS = """ SELECT * FROM polls
JOIN options ON polls_id = options.poll_id
WHERE polls.id = %s;"""

INSERT_OPTION = """INSERT INTO options (option_text, poll_id) 
VALUES %s;""" # use %s to declare input user 
INSERT_VOTE = """INSERT INTO votes (username, option_id) VALUES (%s,%s);"""

def create_tables(connection):
    """ crate different tables if not exist """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)

def get_polls(connection):
    """ return all polls created """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()

def get_latest_poll(connection):
    """ return last poll created """
    with connection:
        with connection.cursor() as cursor:
            pass

def get_poll_details(connection, poll_id):
    """ get details from specific poll """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id))
            return cursor.fetchall()

def get_poll_and_vote_results(connection, poll_id):
    """ show result of poll ended """
    with connection:
        with connection.cursor() as cursor:
            pass

def get_random_poll_vote(connection, option_id):
    """  """
    with connection:
        with connection.cursor() as cursor:
            pass

def create_poll(connection, title, owner, options):
    """ create new poll """
    with connection:
        with connection.cursor() as cursor:
            pass

def add_poll_vote(connection, username, option_id):
    """ vote in anyone poll """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))