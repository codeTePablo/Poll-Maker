from typing import List

import random
import datetime
import pytz
import matplotlib.pyplot as plt

import charts
import database

from connection_pool import get_connection
from models.option import Option
from models.poll import Poll


MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Charts
7) Bar chart all polls 
8) Drop poll
9) Exit

Enter your choice: """

MENU_PROMPT_CHART = """-- Menu --
1) Pie chart
2) Bar chart
3) Exit
""" 
NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll():
    """
    Return:
        Query: create and add options to poll
    """
    title = input("Enter poll title: ")
    owner = input("Enter poll owner: ")
    poll = Poll(title, owner)
    poll.save()

    while (new_option := input(NEW_OPTION_PROMPT)):
        poll.add_option(new_option)


def list_open_polls():
    """
    Return:
        Query: show all poll available
    """
    for poll in Poll.all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    """
    Return:
        Query: add vote with username to poll
    """
    poll_id = int(input("Enter poll would you like to vote on: "))

    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    Option.get(option_id).vote(username)


def _print_poll_options(options: List[Option]):
    """
    plt
    Args:
        arg1 (List): List of Option model 
    Return:
        Query: print each option id and option text
    """
    for option in options:
        print(f"{option.id}: {option.text}")


def show_poll_votes():
    """
    Return:
        Query: 
    """
    poll_id = int(input("Enter poll you would like to see votes for: "))
    poll = Poll.get(poll_id)  #  Get poll from specific poll 
    options = poll.options  #  Get options
    votes_per_option = [len(option.votes) for option in options]  # Get total votes and show how many votes have each option (list)   
    # print(votes_per_option)
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
    """
    Args:
        arg1 (List): List of Option model 
    Return:
        str: Using pytz display in what zonetime someone add vote and this had to insert how is    
    """
    for option in options:
        print(f"-- {option.text} --")
        for vote in option.votes:  #  Get votes
            naive_datetime = datetime.datetime.utcfromtimestamp(vote[2])
            utc_date = pytz.utc.localize(naive_datetime)
            local_date = utc_date.astimezone(pytz.timezone("Mexico/General")).strftime("%Y-%m-%d %H:%M")  #  Format to display hour
            print(f"\t- {vote[0]} on {local_date}")


def randomize_poll_winner():
    """
    Return:
        Query: add option to poll
    """
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    poll = Poll.get(poll_id)
    _print_poll_options(poll.options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")

#  CHARTS


def all_bar_chart():
    """
    Return:
        Plot: Get from database all polls and votes and make bar chart
    """
    charts.chart_bar(database.get_polls_and_votes())
    plt.show()


def select_chart(poll_id: int):
    """
    Args:
        arg1 (int): poll id to can select poll 
    Return:
        Menu: From MENU_PROMPT_CHART select what kind of chart view
    """
    while (selection := input(MENU_PROMPT_CHART)) != "6":

        try:
            MENU_OPTIONS_CHARTS[selection](poll_id)

        except KeyError:
            print("Invalid input selected. Please try again.")


def pie_chart(poll_id: int):
    """
    plt
    Args:
        arg1 (int): poll id to can select poll
    Return:
        Plot: Get from database this poll and votes and make pie chart
    """
    options = database.get_options(poll_id)
    charts.chart_pie(options)
    plt.show()

def bar_chart(poll_id: int):
    """
    plt
    Args:
        arg1 (int): poll id to can select poll
    Return:
        Plot: Get from database this poll and votes and make bar chart
    """
    charts.one_chart_bar(database.get_polls_and_votes())
    plt.show()



MENU_OPTIONS_CHARTS = {
    "1": pie_chart,
    "2": bar_chart
}

def select_poll():  
    """
    Return:
        Query: add option to poll
    """
    try:
        for poll in Poll.all():  #  Show all polls to know which someone can vote 
            print(f"{poll.id}: {poll.title} (created by {poll.owner})")

        poll_id = int(input("Enter poll would you like see stats: "))
        select_chart(poll_id)  #  Menu of charts 

    except KeyError:
        print("Invalid input selected. Please try again.")


def drop_poll():
    """
    Return:
        Query: delete poll
    """
    delete_poll = int(input("what poll do you want drop: "))
    poll = Poll(title=None, owner=None)
    poll.delete_poll(delete_poll)


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner,
    "6": select_poll, 
    "7": all_bar_chart,
    "8": drop_poll
}


def menu():
    """
    Return:
        Menu: main menu to forward what kind of section view 
    """
    with get_connection() as connection:
        database.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "9":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again.")
