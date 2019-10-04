from tictac import *
import pickle

for i in range(100):
    opponent = "start"
    while opponent not in "123":
        opponent = input("Level 1, 2, 3, or 4?")
        print(opponent)
        if opponent == "1":
            fname = "o-100.p"
        elif opponent == "4":
            fname = "o-million.p"
        elif opponent == "2":
            fname = "o-10000.p"
        elif opponent == "3":
            fname = "o-100000.p"
        else:
            print("Please select 1, 2, 3, or 4")

    computer = pickle.load(open(fname, "rb"))
    player = Pyg(piece='X')
    E2 = Experiment(player, computer, 5, watcher=True, debug=False,
                    mode="pyg_display")
    E2.runExperiment()
