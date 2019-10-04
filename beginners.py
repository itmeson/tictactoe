from tictac import *
import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()  # an empty figure with no axes
ax1 = fig.add_subplot(1,1,1)
def animate(i):
    pullData = open("long_train.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

me = Menace(piece='X')
you = Menace(piece='O')
for i in range(1):
    E = Experiment(me, you, 10000, watcher=True, debug=True,
                mode="pyg_display", logname="long_train.txt")
    E.runExperiment()

    #pickle.dump(me, open("x-menace.p", "wb"))
    #pickle.dump(you, open("o-menace.p", "wb"))
