from tictac import *
import pickle

me = Menace(piece='X')
you = Menace(piece='O')
for i in range(1):
    E = Experiment(me, you, 100000, watcher=False, debug=True,
                mode="text_display", logname="100000_train.txt")
    E.runExperiment()

    pickle.dump(me, open("x-100000.p", "wb"))
    pickle.dump(you, open("o-100000.p", "wb"))
