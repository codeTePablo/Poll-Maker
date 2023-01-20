from typing import List, Tuple
from contextlib import contextmanager


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


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
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
        arg1 (): connection database
    Return:
        List: List of Poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_POLLS)
        return cursor.fetchall()


def get_poll(connection, poll_id: int) -> Poll:
    """
    Args:
        arg1 (int): select of some poll_id
    Return:
        Query: return this poll_id of a poll
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL, (poll_id,))
        return cursor.fetchone()


def get_latest_poll(connection) -> List[Poll]:
    """
    Args:
        arg1 (): connection database
    Return:
        List = List of poll with options
    """
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_LATEST_POLL)
        return cursor.fetchall()


def get_poll_options(connection, poll_id: int) -> List[Option]:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
        return cursor.fetchall()


# -- options --


def get_option(connection, option_id: int) -> Option:
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_OPTION, (option_id,))
        return cursor.fetchone()


def add_option(connection, option_text: str, poll_id: int):
    """
    Args:
        arg1 (): connection database
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
