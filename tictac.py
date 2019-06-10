"""tictac.py

This module defines objects for use in experimenting with reinforcement learning
as well as hand-coded bots for playing tic-tac-toe.

If you want to change what kind of player your bot is
playing against, you need to change some lines
at the very end of the program -- talk to me if you're not
sure what to do.
"""

from collections import OrderedDict

class Agent():
    def __init__(self, piece="X", mover="human", playbook=None):
        self.piece = piece
        self.move_history = {}
        self.human = mover == "human"
        if not playbook:
            self.playbook = {}
        else:
            self.playbook = playbook

    def random_move(self, positions):
        """Method for selecting a random option from the
        available legal moves.
        """
        from random import choice

        not_filled = [i for i, x in enumerate(positions) if x == "-"]
        return choice(not_filled[1:])

    def quit(self):
        """Method for ending a game.
        """
        raise Exception("User quit")
        import sys
        print(self.piece, " quits!")
        sys.exit()

    def update(self, win=None):
        """Dummy update method for non-learning agents"""
        pass

class RandomAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mover = super().random_move

class Human(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mover(self, positions):
        """Update method for a human, allows the human to resign.
        """
        move_num = sum([1 if x != "-" else 0 for x in positions])
        move = input("Move #" + str(move_num + 1) +':')
        if move == "Q":
            self.quit()
            return 0
        else:
            return move

class Menace(Agent):
    def __init__(self, **kwargs):
        super().__init__(mover="nonhuman", **kwargs)

    def position_frequency(self):
        """Computes frequency of each position seen in the playbook"""
        self.frequency = [[pos, sum([self.playbook[pos][x] for x in self.playbook[pos]])]
                           for pos in self.playbook]
        self.frequency.sort(key=lambda x: x[1], reverse=True)


    def display_playbook(self, position):
        new_positions = ['-'] + [str(self.playbook[position][i+1]) if piece == '-' else piece for i, piece in enumerate(position[1:])]
        for i in range(3):
            print("\t".join(new_positions[1 + i * 3 : 1 + i * 3 + 3]))

    def mover(self, positions):
        """Move method for menace, allows the use of a playbook to select a move.
        """
        from random import choices

        tup_positions = tuple(positions)
        if tup_positions not in self.playbook:
            move = self.random_move(positions)
            return move
        else:
            move = choices(list(self.playbook[tup_positions].keys()),
                           weights = list(self.playbook[tup_positions].values()),
                           k=1)[0]
            return move

    def update(self, win):
        """Reinforcement update method for menace.
        """

        if not win:  # it was a tie
            for position in self.move_history:
                if position in self.playbook:
                    self.playbook[position][self.move_history[position]] += 1
                else:
                    not_filled = [i for i, x in enumerate(position) if x == "-"][1:]
                    self.playbook[position] = OrderedDict([[x, 1] for x in not_filled])
                    self.playbook[position][self.move_history[position]] += 1
        elif win[1] == self.piece:  # it was a win, reinforce all the moves
            for position in self.move_history:
                if position in self.playbook:
                    self.playbook[position][self.move_history[position]] += 3
                else:
                    not_filled = [i for i, x in enumerate(position) if x == "-"][1:]
                    self.playbook[position] = OrderedDict([[x, 1] for x in not_filled])
                    self.playbook[position][self.move_history[position]] += 2
        elif win[1] != self.piece:  # it was a loss, prune once
            for position in self.move_history:
                if position in self.playbook:
                    if self.playbook[position][self.move_history[position]] > 1:
                        self.playbook[position][self.move_history[position]] -= 1
                else:
                    not_filled = [i for i, x in enumerate(position) if x == "-"][1:]
                    self.playbook[position] = OrderedDict([[x, 2] for x in not_filled])
                    self.playbook[position][self.move_history[position]] -= 1

class MyAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(mover="nonhuman", **kwargs)

    def mover(self, positions):
        """This is the function for you to work on -- the last line
        of the function should be a "return" that sends back a valid
        move number.  The body of the function should use the tup_positions
        of pieces to decide where to move next.
        Some things to think about:
        1. If you select a space that is already filled or isn't
        in the numbers 1-9, your program will crash because it
        will keep making the same bad choice over and over again.
        2. Think about how to simplify the problem with your initial
        move choices so it is easier to think about what moves
        your opponent might make.
        3. Please talk to Mark if you're getting stuck.
        """

        not_filled = [i for i, x in enumerate(positions) if x == "-"]
        turn = 11-len (not_filled)
        return not_filled[1]

    def update(self, win):
        for position in self.move_history:
            if position in self.playbook:
                self.playbook[position][self.move_history[position]] += 1
            else:
                not_filled = [i for i, x in enumerate(position) if x == "-"][1:]
                self.playbook[position] = OrderedDict([[x, 0] for x in not_filled])
                self.playbook[position][self.move_history[position]] += 1


class Board:
    """Board handles the display of the tic-tac-toe board state.
    """

    def __init__(self):
        pass

    def display(self, positions, humanAgent=True):
        from os import system

        system("clear")
        for i in range(3):
            print("\t".join(positions[1 + i * 3 : 1 + i * 3 + 3]))


class Game:
    """Game controls the execution of a single game of tic-tac-toe"""

    def __init__(self, board, x, o, watcher=False, debug=True):
        self.positions = ["-"]*10
        self.board = board
        self.playerX = x
        self.playerO = o
        self.human = x.human or o.human
        self.playerX.move_history = {}
        self.playerO.move_history = {}
        self.watcher = watcher
        self.debug = debug

    def play(self):
        import time

        turn = 1
        if self.watcher:
            time.sleep(1.5)
            self.board.display(self.positions)

        while turn < 10:
            if turn % 2 == 1:
                move = self.playerX.mover(self.positions)
                if self.update(move, self.playerX.piece):
                    move = int(move)
                    temp = self.positions[:]
                    temp[move] = "-"
                    self.playerX.move_history[tuple(temp)] = move
                else:
                    continue
            else:
                move = self.playerO.mover(self.positions)
                if self.update(move, self.playerO.piece):
                    move = int(move)
                    temp = self.positions[:]
                    temp[move] = "-"
                    self.playerO.move_history[tuple(temp)] = move
                else:
                    continue

            self.win = self.is_win()
            if self.watcher:
                time.sleep(1.5)
                self.board.display(self.positions)
            if self.win:
                break
            turn += 1

        if self.watcher:
            if not self.win:
                print("It was a tie")
            else:
                print(self.win[1], " wins!!")
            time.sleep(1.5)

        self.playerX.update(self.win)
        self.playerO.update(self.win)


    def update(self, move, piece):
        # check for clashes
        try:
            move = int(move)
            assert move >= 1 and move <= 9
        except:
            if self.debug:
                self.debugHandler(move)
                raise ValueError("Invalid move. Move must be a number between 1 and 9.")
            else:
                print("That was an invalid move, try again")
                return False

        try:
            assert self.positions[move] == "-"
        except:
            if self.debug:
                self.debugHandler(move)
                raise ValueError((move, self.positions, "Space was filled"))
            else:
                print("Space filled, try again")
                return False
        else:
            self.positions[move] = piece
            return True

    def debugHandler(self, move):
        self.board.display(self.positions)
        print("A bad move was made -- here is the error report")
        print("Move:\t", move)

    def is_win(self):
        winners = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            (1, 5, 9),
            (3, 5, 7),
        )
        for w in winners:
            test3 = [self.positions[i] for i in w]
            if test3[1] != "-" and test3.count(test3[1]) == 3:
                return (True, test3[1])
        return False


class Experiment:
    """Experiment controls the execution of a collection of games between
    two agents, potentially logging the results."""

    def __init__(self, X, O, trials, logname=None, watcher=False, debug=True):
        self.trials = trials
        self.playerX = X
        self.playerO = O
        self.xwins = 0
        self.owins = 0
        self.ties = 0
        self.logname = logname
        self.watcher = watcher
        self.debug = debug

    def logging(self):
        import os

        gp = self.xwins + self.owins + self.ties
        self.file.write(
            str(self.xwins / gp)
            + ","
            + str(self.owins / gp)
            + ","
            + str(self.ties / gp)
            + ","
            + str(len(self.playerX.playbook.keys()))
            + ","
            + str(len(self.playerO.playbook.keys()))
            + "\n"
        )
        self.file.flush()
        os.fsync(self.file.fileno())

    def one_game(self):
        self.last_board = Board()
        self.last_game = Game(self.last_board, self.playerX, self.playerO, watcher=self.watcher, debug=self.debug)
        self.last_game.play()

        if not self.last_game.win:
            self.ties += 1
        elif self.last_game.win[1] == "X":
            self.xwins += 1
        elif self.last_game.win[1] == "O":
            self.owins += 1
        if self.watcher:
            print("X Wins:\t", self.xwins)
            print("O Wins:\t", self.owins)
            print("Ties:\t", self.ties)

    def runExperiment(self):
        if self.logname:
            self.file = open(self.logname, "a", buffering=1)
        for i in range(self.trials):
            self.one_game()
            if self.logname:
                self.logging()
        if self.logname:
            self.file.close()


#me = Menace(piece='X')
#you = Menace(piece='O')
#E = Experiment(me, you, 10000, watcher=False, debug=True, logname="t.txt")
#E.runExperiment()

#player = Human(piece='X')
#E2 = Experiment(player, you, 5, watcher=True, debug=True)
#E2.runExperiment()
