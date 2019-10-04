from tictac import *

me = Menace(piece='X')
you = Menace(piece='O')
for i in range(1):
    E = Experiment(me, you, 10000, watcher=True, debug=True,
                mode="pyg_display", logname="long_train.txt")
    E.runExperiment()

    #pickle.dump(me, open("x-menace.p", "wb"))
    #pickle.dump(you, open("o-menace.p", "wb"))
