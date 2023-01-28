from typing import List

import psycopg2

from connection_pool import get_connection
from models.option import Option
import database


class Poll:
    def __init__(self, title: str, owner: str, _id: int = None):
        """
        Args:
            arg1 (str): title of the poll
            arg1 (str): owner of the poll
            arg1 (int): id of the poll this database will generate automatically
        Return:
            self: parameters option_text, id, poll_id
        """
        self.id = _id
        self.title = title
        self.owner = owner

    def __repr__(self) -> str:
        """
        Args:
            arg1 (self): self class
        Return:
            str: return Poll: option_text, id, poll_id
        """
        return f"Poll({self.name!r}, {self.owner!r}, {self.id!r})"

    def add_option(self, option_text: str):
        """
        Adding options to a poll
        Args:
            arg1 (str): option text of a poll
        Return:
            str: add option inside a poll and using save method add option text
        """
        Option(option_text, self.id).save()

    def save(self):
        """
        Save new poll
        Args:
            arg1 (self): self class
        Return:
            Query: create new poll inside in database and this self.id will be
            this new poll
        """
        with get_connection() as connection:
            new_poll_id = database.create_poll(connection, self.title, self.owner)
            self.id = new_poll_id

    def delete_poll(self, drop_id: int):
        """
        Args:
            arg1 (self): self class
            arg1 (int): use id from some poll to delete
        Return:
            Query: drop poll
        """
        with get_connection() as connection:
            database.delete_poll(connection, drop_id)

    @property
    def options(self) -> List[Option]:
        """
        Args:
            arg1 (self): self class
        Return:
            List: List of options of a some poll
        """
        with get_connection() as connection:
            options = database.get_poll_options(connection, self.id)
            return [Option(option[1], option[2], option[0]) for option in options]

    @classmethod
    def get(cls, poll_id: int) -> "Poll":
        """
        Args:
            arg1 (int): poll_id to identify polls
        Return:
            Call Poll class and creates a new Poll object
            This can be execute after the class has finished processing
            Poll object: get polls
        """
        with get_connection() as connection:
            poll = database.get_poll(connection, poll_id)
            return cls(poll[1], poll[2], poll[0])

    @classmethod
    def all(cls) -> List["Poll"]:
        """
        Args:
            arg1 (cls): classmethod
        Return:
            List: List comprehension of poll to return title, owner and id of
            one poll
        """
        with get_connection() as connection:
            polls = database.get_polls(connection)
            return [cls(poll[1], poll[2], poll[0]) for poll in polls]

    @classmethod
    def latest(cls) -> "Poll":
        """
        Args:
            arg1 (cls): classmethod
        Return:
            Poll: get latest poll with title, owner and id of poll
        """
        with get_connection() as connection:
            poll = database.get_latest_poll(connection)
            return cls(poll[1], poll[2], poll[0])
