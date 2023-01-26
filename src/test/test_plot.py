import matplotlib.pyplot as plt

#  Lines

#  Figure = plt.figure()
# figure, (ax1, ax2) = plt.subplots(1,2)

#  The grid of space have 2 rows and 3 columns (6 spaces in total)

#  Axes = figure.add_subplot(1,2,1)  #  Row, column and index for his axes 
#  Axes1 = figure.add_subplot(1,2,2)


#  Axes.set_title("Line")
#  Axes.set_xlabel("Number")
#  Axes.set_ylabel("Person")
# ax1.plot([1,2,3,4], [1,2,3,4])
# ax2.plot([1,2,3,7], [2,5,6,7])

#  Line = plt.plot([1,2,3,4], [1,2,3,4], "o")  #  Only circle points where 'x' and 'y' intersect 
# plt.show()


#  Pie chart

# Figure = plt.figure()
# axes = Figure.add_subplot()

# number = [15, 35, 50]
# names = [
#     "Java", 
#     "Python",
#     "None"
# ]

# axes.pie(
#     number, 
#     labels=names, 
#     explode=[0.1, 0, 0],  #  Explode first argument (java) leaving a white space two unseparated
#     autopct="%1.1f%%")  #  Show percent 
# plt.show()

#  Bar chart 

# Figure = plt.figure()
# axes = Figure.add_subplot()
# axes.bar(
#     [1,2,3,4],
#     [1,2,3,4], 
#     )

# plt.show()

#  Stacked chart 
# we need 2 options to compare (title, men, woman)
polls = [
    ("Flask vs. Django", 60, 19),
    ("Who will win the election?", 15, 36),
    ("Python vs. Java", 26, 40),
    ("Mac vs. Windows", 25, 34),
    ("What is the most popular type of graph?", 20, 13),
    ("Who is the podcasting king?", 11, 6),
]

figure = plt.figure(figsize=(6,6))
figure.subplots_adjust(bottom=0.1)
axes = figure.add_subplot()

poll_titles = [poll[0] for poll in polls]
poll_men = [poll[1] for poll in polls]
poll_woman = [poll[2] for poll in polls]
poll_x_coordinates = range(len(polls))

men_plot = axes.bar(
    poll_x_coordinates, 
    poll_men
)

women_plot = axes.bar(
    poll_x_coordinates, 
    poll_woman,
    bottom=poll_men
)

axes.legend((men_plot, women_plot), ("Man", "Women"))  #  Show label of any labels

plt.xticks(poll_x_coordinates, poll_titles, rotation=30, ha="right")

plt.show()


#  Generate image
#  Ask user if want save image 
# figure.savefig("graph1.png", bbox_inches="tight")