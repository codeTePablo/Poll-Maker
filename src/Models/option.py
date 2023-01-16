from src.Module import database
from src.Models.connections import create_connection


class Option:
    def __init__(self, _id: None, option_text: str, poll_id: int):
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
        connection = create_connection()
        new_save = database.add_option(connection, self.text, self.poll_id)
        connection.close()
        self.id = new_save

    def vote(self, user_name: str):
        """
        Args:
            arg1 (str): user name to can add votes

        Return:
            Query: add vote some poll with user name
        """
        connection = create_connection()
        new_option_id = database.add_poll_vote(connection, user_name, self.id)
        connection.close()

    @property
    def votes(self) -> list[database.Vote]:
        """
        Args:
            arg1 (self): self class

        Return:
            list: list of Vote (str, int)
        """
        connection = create_connection()
        votes = database.get_votes_for_option(connection, self.id)
        connection.close()
        return votes

    @classmethod
    def get(cls, option_id: int):
        """
        Args:
            arg1 (self): self class

        Return:
            str: return option_text, id, poll_id
        """
        connection = create_connection()
        option = database.get_option(connection, option_id)
        connection.close()
        return cls(option[1], option[2], option[0])
