import os
import random

#  Time
import pytz
import datetime
from typing import List

#  Database
import psycopg2
from src.Models.connection_pool import get_connection

#  Variables
from dotenv import load_dotenv

#  Modules
from src.Module import database
from src.Models.poll import Poll
from src.Models.option import Option

DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "
MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Exit

Enter your choice: """
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll():
    """
    Args:

    Return: create new poll.
    """
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    poll = Poll(poll_title, poll_owner)
    poll.save()

    while new_option := input(NEW_OPTION_PROMPT):
        poll.add_option(new_option)


def list_open_polls():
    """
    Args:

    Return:
        Query: show all polls
    """
    for poll in Poll.all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    """
    Args:

    Return:
        Query: all vote into a poll
    """
    poll_id = int(input("Enter poll would you like to vote on: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    Option.get(option_id).vote(username)


def _print_poll_options(options: List[Option]):
    """
    Args:
        arg1 (List): print List of poll with options
    Return:
        List: print in console poll and options
    """
    for option in options:
        print(f"{option.id}: {option.text}")


def show_poll_votes():
    """
    Args:

    Return:
        Query: show result of poll
    """
    poll_id = int(input("Enter poll you would like to see votes for: "))
    poll = Poll.get(poll_id)
    options = poll.options
    votes_per_option = [len(option.votes) for option in options]
    total_votes = sum(votes_per_option)

    try:
        for option, votes in zip(options, votes_per_option):
            percentage = votes / total_votes * 100
            print(f"{option.text} for {votes} ({percentage:.2f}% of total)")
    except ZeroDivisionError:
        print("No votes yet cast for this poll.")

    vote_log = input("Would you like to see the vote log? (y/N) ")

    if vote_log == "y":
        _print_votes_for_options(options)


def _print_votes_for_options(options: List[Option]):
    for option in options:
        print(f"-- {option.text} --")
        for vote in option.votes:
            naive_datetime = datetime.datetime.utcfromtimestamp(vote[2])
            utc_date = pytz.utc.localize(naive_datetime)
            local_date = utc_date.astimezone(pytz.timezone("Mexico/General")).strftime(
                "%Y-%m-%d %H:%M"
            )
            print(f"\t- {vote[0]} on {local_date}")


def randomize_poll_winner():
    """
    Args:
        arg1 (connection): connection database.
    Return:
        Query: print poll options (List) and winner of that poll
    """
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(
        input(
            "Enter which is the winning option, we'll pick a random winner from voters: "
        )
    )
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")


def new_user():
    """
    Args:
        arg1 :
    Return:
        Query:
    """
    pass


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner,
}


def menu():
    """
    Args:
        arg1 (): N.
    Return:
        Query: print poll options (List) and winner of that poll
    """
    with get_connection() as connection:
        database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")
