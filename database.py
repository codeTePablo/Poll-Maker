from typing import List, Tuple
from contextlib import contextmanager

import psycopg2
import os
from dotenv import load_dotenv


Poll = Tuple[int, str, str]
Option = Tuple[int, str, int]
Vote = Tuple[str, int]


CREATE_POLLS = "CREATE TABLE IF NOT EXISTS polls (id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"
CREATE_OPTIONS = "CREATE TABLE IF NOT EXISTS options (id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);"
CREATE_VOTES = "CREATE TABLE IF NOT EXISTS votes (username TEXT, option_id INTEGER, vote_timestamp INTEGER);"


SELECT_ALL_POLLS = "SELECT * FROM polls;"
SELECT_POLL = "SELECT * FROM polls WHERE id = %s;"
SELECT_LATEST_POLL = """SELECT * FROM polls
WHERE polls.id = (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1
);"""
SELECT_POLL_OPTIONS = "SELECT * FROM options WHERE poll_id = %s;"
SELECT_OPTION = "SELECT * FROM options WHERE id = %s;"

SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE option_id = %s;"

INSERT_POLL_RETURN_ID = (
    "INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"
)
INSERT_OPTION = (
    "INSERT INTO options (option_text, poll_id) VALUES (%s, %s) RETURNING id;"
)
INSERT_VOTE = (
    "INSERT INTO votes (username, option_id, vote_timestamp) VALUES (%s, %s, %s);"
)

#  Charts

load_dotenv()
#  Connection for charts 
connection_plot = psycopg2.connect(os.environ.get("DATABASE_URI"))

SELECT_ONE_POLL = "SELECT * FROM polls WHERE id = %s;"
SELECT_OPTIONS_IN_POLL = """
SELECT options.option_text, COUNT(votes.option_id) FROM options
JOIN polls ON options.poll_id = polls.id
JOIN votes ON options.id = votes.option_id
WHERE polls.id = %s
GROUP BY options.option_text;"""
SELECT_EACH_POLLS = """
SELECT polls.title, COUNT(votes.option_id) FROM polls
JOIN options ON options.poll_id = polls.id
JOIN votes ON options.id = votes.option_id
GROUP BY polls.title;"""


@contextmanager
def get_cursor(connection):
    """
    Args:
        arg1 (str): connection to database
    Return:
        connection: this simplify so much to make connections, only we can call function
        and wait cursor to execute after of any transaction
    """
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
    """
    Args:
        arg1 (str): connection to database
    Return:
        Query: create polls
    """
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_POLLS)
        cursor.execute(CREATE_OPTIONS)
        cursor.execute(CREATE_VOTES)


# -- polls --


def create_poll(connection, title: str, owner: str) -> int:
    """create new poll
    Args:
        arg1 (): connection database
        arg2 (str): title of the poll
        arg3 (str): owner has create poll
        arg4 (List[str]): options has contains the poll
    Return:
        Query: cursor insert new poll in database
    """
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))

        poll_id = cursor.fetchone()[0]
        return poll_id


def get_polls(connection) -> List[Poll]:
    """
    Args:
        arg1 (str): connection to database
    Return:
        List: List of Poll to select all polls into database
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POLLS)
        return cursor.fetchall()


def get_poll(connection, poll_id: int) -> Poll:
    """
    Args:
        arg1 (str): connection to database
        arg2 (int): select poll with poll id
    Return:
        Query: return this poll_id of a poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL, (poll_id,))
        return cursor.fetchone()


def get_latest_poll(connection) -> List[Poll]:
    """
    Args:
        arg1 (): connection to database
    Return:
        List = List of poll with options
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POLL)
        return cursor.fetchall()


def get_poll_options(connection, poll_id: int) -> List[Option]:
    """
    Args:
        arg1 (str): connection to database
        arg2 (int):  poll_id
    Return:
        List: list of Option with polls and options   
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
        return cursor.fetchall()


def get_poll_bar(poll_id: int):
    """
    Args:
        arg1 (int): select poll with poll id  
    Return:
        Query: return poll 
    """
    with connection_plot:
        with connection_plot.cursor() as cursor:
            cursor.execute(SELECT_ONE_POLL, (poll_id,))
            return cursor.fetchone()


def get_polls_and_votes():
    """
    Args:
        arg1 (): 
    Return:
        Query: return all poll with votes 
    """
    with connection_plot:
        with connection_plot.cursor() as cursor:
            cursor.execute(SELECT_EACH_POLLS)
            return cursor.fetchall()


# -- options --


def get_option(connection, option_id: int) -> Option:
    """
    Args:
        arg1 (str): connection to database
        arg1 (int): option id of some poll
    Return:
        Query: return text of option with option id  
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_OPTION, (option_id,))
        return cursor.fetchone()

def get_options(poll_id: int):
    """
    plt
    Args:
        arg1 (int): select some poll with poll id 
    Return:
        Query: return options of poll 
    """
    with connection_plot:
        with connection_plot.cursor() as cursor:
            cursor.execute(SELECT_OPTIONS_IN_POLL, (poll_id,))
            return cursor.fetchall()


def add_option(connection, option_text: str, poll_id: int):
    """
    Args:
        arg1 (): connection to database
        arg2 (str): option_text to add option inside a poll
        arg3 (int): poll id to can add option
    Return:
        Query: add option to poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_OPTION, (option_text, poll_id))


# -- votes --


def get_votes_for_option(connection, option_id: int) -> List[Vote]:
    """
    Args:
        arg1 (): connection database
        arg2 (int): option id of option (index)
    Return:
        Query: add one vote to poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id,))
        return cursor.fetchall()


def add_poll_vote(connection, username: str, vote_timestamp: float, option_id: int):
    """
    Args:
        arg1 (): connection database
        arg2 (str): connection database
        arg3 (int): username how can vote on polls
        arg3 (int): timezone in someone vote
    Return:
        Query: add one vote to poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_VOTE, (username, option_id, vote_timestamp))
