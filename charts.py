import matplotlib.pyplot as plt

def chart_pie(options):
    figure = plt.figure()
    axes = figure.add_subplot()
    axes.pie(
        [option[1] for option in options], 
        labels=[option[0] for option in options], 
        autopct="%1.1f%%") 

    return figure

def one_chart_bar(poll):
    """
    only one poll for chart bar 
    """
    figure = plt.figure()
    axes = figure.add_subplot()
    axes.bar(
        1,
        [poll[1] for poll in poll],
        tick_label = [poll[0] for poll in poll]
    )

    return figure

def chart_bar(polls):
    """
    chart bar each poll opened 
    """
    figure = plt.figure()
    axes = figure.add_subplot()
    axes.bar(
        range(len(polls)),
        [poll[1] for poll in polls],  #  Height 
        tick_label = [poll[0] for poll in polls]
    )

    return figure