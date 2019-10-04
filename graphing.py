import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()  # an empty figure with no axes
ax1 = fig.add_subplot(1,1,1)
def animate(i):
    pullData = open("long_train.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    xwins = []
    owins = []
    ties = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            data = eachLine.split(',')
            xar.append(float(data[0]))
            xwins.append(float(data[1]))
            owins.append(float(data[2]))
            ties.append(float(data[3]))
    ax1.clear()
    plt1, = plt.plot(xar, xwins, label="Wins for X")
    plt2, = plt.plot(xar, owins, label="Wins for O")
    plt3, = plt.plot(xar, ties, label="Ties")
    plt.legend([plt1, plt2, plt3], ["X", "O", "Ties"])

ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()
