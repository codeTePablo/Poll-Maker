import pytz
import datetime

from typing import List

from src.Module import database
from src.Models.connection_pool import get_connection


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.id = _id
        self.text = option_text
        self.poll_id = poll_id

    def __repr__(self) -> str:
        """
        Args:
            arg1 (self): self class

        Return:
            str: return option_text, id, poll_id
        """
        return f"Option: {self.text!r}, {self.id!r}, {self.poll_id!r}"

    def save(self):
        """
        Args:
            self : self class

        Return:
            Query: add options
        """
        with get_connection() as connection:
            new_save = database.add_option(connection, self.text, self.poll_id)
            self.id = new_save

    def vote(self, username: str):
        """
        Args:
            arg1 (str): user name to can add votes

        Return:
            Query: add vote some poll with user name
        """
        current_datetime_utc = datetime.datetime.now(tz=pytz.utc)
        current_timestamp = current_datetime_utc.timestamp()
        with get_connection() as connection:
            database.add_poll_vote(connection, username, current_timestamp, self.id)

    @property
    def votes(self) -> List[database.Vote]:
        """
        Args:
            arg1 (self): self class

        Return:
            List: List of Vote (str, int)
        """
        with get_connection() as connection:
            votes = database.get_votes_for_option(connection, self.id)
            return votes

    @classmethod
    def get(cls, option_id: int) -> "Option":
        """
        Args:
            arg1 (self): self class

        Return:
            str: return option_text, id, poll_id
        """
        with get_connection() as connection:
            option = database.get_option(connection, option_id)
            return cls(option[1], option[2], option[0])
