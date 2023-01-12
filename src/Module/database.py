from psycopg2.extras import execute_values

#  Type hinting
User = tuple[int, str, str]
Poll = tuple[int, str, str]
Vote = tuple[str, int]
PollWithOptions = tuple[int, str, str, int, str, int]
PollResults = tuple[int, str, int, float]

#  DDL
CREATE_USER = """CREATE TABLE IF NOT EXISTS user_to_login
(id SERIAL PRIMARY KEY, username TEXT, password TEXT);"""  #  Check this to gui
CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls 
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""
CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options 
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER, 
FOREIGN KEY(poll_id) REFERENCES polls(id));"""
CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER,
FOREIGN KEY(option_id) REFERENCES options(id));"""

#  DML
SELECT_ALL_POLLS = """SELECT * FROM polls;"""
SELECT_USERNAME = """SELECT * FROM user_to_login 
where username = %s AND password = %s"""  #  Check this to gui
SELECT_POLL_WITH_OPTIONS = """ SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = %s and password = %s;"""
SELECT_LATEST_POLL = """SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls_id (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1
);"""  #  Nested query
SELECT_RANDOM_VOTE = (
    """SELECT * FROM votes WHERE option_id = %s ORDER BY RANDOM() LIMIT 1;"""
)
SELECT_POLL_VOTE_DETAILS = """SELECT
    options.id,
    options.option_text,
    COUNT(votes.option_id),
    COUNT(votes.option_id) / sum(count(votes.option_id)) OVER() * 100.0
FROM options
LEFT JOIN votes on options.id = votes.option_id
WHERE options.poll_id = %s
GROUP BY options.id;"""

INSERT_POLL_RETURN_ID = (
    """INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"""
)
INSERT_OPTION = """INSERT INTO options (option_text, poll_id) 
VALUES %s;"""  #  Use %s to declare input user
INSERT_VOTE = """INSERT INTO votes (username, option_id) VALUES (%s,%s);"""


def create_tables(connection):
    """
    Return:
        Query: execute query to create tables if not exist
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_USER)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)


def create_users(connection, username: str, password: str) -> list[User]:
    """
    Args:
        param p1 (): connection database
        param p2 (str): create new username
        param p3 (str): create new password associated with username
    Return:
        Query: list of user to connect username and password to login
    """
    with connection:
        with connection.cursor() as cursor:
            # create function to access with user and pass
            pass


def get_polls(connection) -> list[Poll]:
    """
    Args:
    param p1: connection database
    Return:
        list: list of Poll
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()


def get_latest_poll(connection) -> list[PollWithOptions]:
    """
    Args:
        param p1: connection database
    Return:
        list = list of poll with options
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LATEST_POLL)
            return cursor.fetchall()


def get_poll_details(connection, poll_id: int) -> list[PollWithOptions]:
    """
    Args:
        param p1: connection database
        param p2 (int): attribute (poll_id) form table options
    Return:
        list = list of poll with options
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id,))
            return cursor.fetchall()


def get_poll_and_vote_results(connection, poll_id: int) -> list[PollResults]:
    """
    Args:
        param p1: connection database
        param p2 (int): attribute (poll_id) form table options
    Return:
        list = list of poll with results
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_VOTE_DETAILS, (poll_id,))
            return cursor.fetchall()  # return multiple options


def get_random_poll_vote(connection, option_id: int) -> Vote:
    """
    Args:
        param p1: connection database
        param p2 (int): attribute (option_id) form table votes
    Return:
        Vote: get random vote from some poll
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_VOTE, (option_id))
            return cursor.fetchone()


def create_poll(connection, title: str, owner: str, options: list[str]):
    """create new poll
    Args:
        param p1 (): connection database
        param p2 (str): title of the poll
        param p3 (str): owner has create poll
        param p4 (list[str]): options has contains the poll
    Return:
        Query: cursor insert new poll in database
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                INSERT_POLL_RETURN_ID, (title, owner)
            )  # return set with one row and one column

            poll_id = cursor.fetchone()[0]  # access column 0
            # for each option_text contains the option_text and poll_id
            option_values = [
                (option_text, poll_id) for option_text in options
            ]  # comprehension list to list each option
            # execute the cursor, query and the list of values
            execute_values(
                cursor, INSERT_OPTION, option_values
            )  # do for loop as the same way as for loop below
            # for option_value in option_values:
            # cursor.execute(INSERT_OPTION, option_value) # for each option value in option_values insert into table options


def add_poll_vote(connection, username: str, option_id: int):
    """vote in anyone poll

    :param p1: connection database
    :param p2: username how can vote on polls
    :param p3: attribute (option_id) form table votes
    :return: add one vote to poll
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))
