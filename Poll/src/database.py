from psycopg2.extras import execute_values

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
SELECT_LATEST_POLL = """SELECT * FROM polls
JOIN options ON polls_id = options.poll_id
WHERE polls_id (
    SELECT id FROM polls ORDER BY id DESC LIMIT 1
);""" # nested query
SELECT_RANDOM_VOTE = """SELECT * FROM votes WHERE option_id = %s ORDER BY RANDOM() LIMIT 1;"""

INSERT_POLL_RETURN_ID = """INSERT INTO polls (title, owner_username) VALUES (%s, %s) RETURNING id;"""
INSERT_OPTION = """INSERT INTO options (option_text, poll_id) 
VALUES %s;""" # use %s to declare input user 
INSERT_VOTE = """INSERT INTO votes (username, option_id) VALUES (%s,%s);"""

def create_tables(connection):
    """
    :return: execute query to create tables if not exist 
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)

def get_polls(connection):
    """
    :return: all polls created 
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()

def get_latest_poll(connection):
    """
    :return: last poll created 
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LATEST_POLL)
            return cursor.fetchall()

def get_poll_details(connection, poll_id):
    """ 
    :param p1: attribute (poll_id) form table options 
    :return: get details from specific poll 
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id))
            return cursor.fetchall()

def get_poll_and_vote_results(connection, poll_id):
    """ 
    :param p1: attribute (poll_id) form table options 
    :return: show result of poll ended 
    """
    with connection:
        with connection.cursor() as cursor:
            pass

def get_random_poll_vote(connection, option_id):
    """  
    :param p1: attribute (option_id) form table votes
    :return: get random vote from some poll
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOM_VOTE, (option_id))
            return cursor.fetchone()

def create_poll(connection, title, owner, options):
    """ create new poll 
    :param p1: connection with database
    :param p2: title of the poll 
    :param p3: owner has create poll
    :param p4: options has contains the poll
    :return: insert new poll in database
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_POLL_RETURN_ID, (title, owner)) # return set with one row and one column
            
            poll_id = cursor.fetchone()[0] # access column 0
            # for each option_text contains the option_text and poll_id
            option_values = [(option_text, poll_id) for option_text in options] # comprehension list to list each option
            # execute the cursor, query and the list of values
            execute_values(cursor, INSERT_OPTION, option_values) # do for loop as the same way as for loop below
            # for option_value in option_values:
                # cursor.execute(INSERT_OPTION, option_value) # for each option value in option_values insert into table options

def add_poll_vote(connection, username, option_id):
    """ vote in anyone poll 
    :param p1: username how can vote on polls
    :param p2: attribute (option_id) form table votes
    :return: add one vote to poll
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))