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

# axes.pie(number, 
#     labels=names, 
#     explode=[0.1, 0, 0],  #  Explode first argument (java) leaving a white space two unseparated
#     autopct="%1.1f%%")  #  Show percent 
# plt.show()

#  Bar chart 

Figure = plt.figure()
axes = Figure.add_subplot()
axes.bar(
    [1,2,3,4],
    [1,2,3,4], 
    )

plt.show()

