import matplotlib.pyplot as plt

def chart_pie(options):
    """
    Args:
        arg1 (List): list of option and count of votes obtain of query from 
        database (get_polls_and_votes) where using join's return total of 
        votes for each option 
    Return:
        Plot: return specific pie chart  
    """
    figure = plt.figure()
    axes = figure.add_subplot()
    # print(options)

    poll_options = [poll[1] for poll in poll]
    poll_names = [poll[0] for poll in poll]

    axes.pie(
        poll_options,  #  List of quantities of poll options  
        labels=poll_names,  #  List of names of each option
        autopct="%1.1f%%")  #  Format to show percentage 

    return figure


def one_chart_bar(poll):
    """
    Args:
        arg1 (List): list of option and count of votes obtain of query from 
        database (get_polls_and_votes) where using join's return total of 
        votes for each option 
    Return:
        Plot: return specific bar chart   
    """
    figure = plt.figure()
    axes = figure.add_subplot()
    # print(poll)

    poll_options = [poll[1] for poll in poll]
    poll_names = [poll[0] for poll in poll]

    axes.bar(
        1,
        poll_options,  #  List of quantities of poll options
        tick_label = poll_names  #  List of names of each option
    )

    return figure


def chart_bar(polls):
    """
    Args:
        arg1 (List): list of poll and count of votes obtain of query from 
        database (get_polls_and_votes) where using join's to return total 
        of votes for each option 
    Return:
        Plot: return bar chart with all polls available 
    """
    figure = plt.figure(figsize=(10,10))  #  1 inch = 100 px
    figure.subplots_adjust(bottom=0.36)
    axes = figure.add_subplot()
    # print(polls)
    axes.set_title("Polls and their vote counts")
    axes.set_ylabel("Vote count")

    size_x = range(len(polls))
    poll_height = [poll[1] for poll in polls]
    poll_names_option = [poll[0] for poll in polls] 

    axes.bar(
        size_x,  #  Size of x
        poll_height,  #  Height of each column 
        tick_label = poll_names_option  #  Names of each poll
    )
    plt.xticks(rotation=30, ha="right")  #  Adjust names with inclination and set correct position

    return figure


def chart_stacked():
    pass
