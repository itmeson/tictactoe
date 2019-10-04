from tictac import *
import pickle

for i in range(100):
    computer = pickle.load(open("o-menace.p", "rb"))
    player = Pyg(piece='X')
    E2 = Experiment(player, computer, 5, watcher=True, debug=False,
                    mode="pyg_display")
    E2.runExperiment()
