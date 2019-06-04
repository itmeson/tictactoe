"""tictac.py

This module defines objects for use in experimenting with reinforcement learning
as well as hand-coded bots for playing tic-tac-toe.

If you want to change what kind of player your bot is 
playing against, you need to change some lines
at the very end of the program -- talk to me if you're not
sure what to do.
"""

def make_my_move(positions):
  """Your make_my_move function has to be able to read in the
  state of the board in the positions variable, decided what 
  move to make, and return an integer 1-9 as the space it wants
  to move into.  

  Some things to think about:
  1. If you select a space that is already filled or isn't 
  in the numbers 1-9, your program will crash because it
  will keep making the same bad choice over and over again.
  2. Think about how to simplify the problem with your initial
  move choices so it is easier to think about what moves
  your opponent might make.
  3. Please talk to Mark if you're getting stuck.
  """

  # not_filled will hold a list of the open board positions
  not_filled = [i for i, x in enumerate(positions) if x == "-"]
  
  turn = 11-len (not_filled)
  # in here, `write stuff to figure out your move,
  # store it in a variable called "move".
  # It is currently set to to pick the first open position
  # on the board.
  move = 0
  if turn == 1:
    move = 1
  
  elif turn == 3:
    if 3 in not_filled:
      move = 3
    else:
      move = 2
  
  elif turn == 5: 
    
    if positions[3] == "-":
      move = 3
    else:
      move = 2
  
  elif turn == 7:
    if positions[1] == "-":
     move = 1 
    else:
       move = 7
  
  # catch-all
  if move == 0:
    move = not_filled[1]

  # you must have, at the end of the function, a line that 
  # "returns" the move you want to make
  return move


class Agent:
    """An Agent is an object that knows how to produce valid moves in tic-tac-toe, given a valid state of the board.
    """

    def __init__(self, piece="X", mover="human", playbook=None):
        self.piece = piece
        movers = {
            "human": self.human_move,
            "random": self.random_move,
            "menace": self.menace_move,
            "mine": make_my_move
        }
        updaters = {
            "human": self.dummy,
            "random": self.dummy,
            "menace": self.update_menace,
            "mine": self.dummy
        }
        self.mover = movers[mover]
        self.update = updaters[mover]
        self.move_history = {}
        self.human = mover == "human"
        if not playbook:
            self.playbook = {}
        else:
            self.playbook = playbook

    def dummy(self, win):
        """The default update method for agents that do not learn.
        """
        pass

    def human_move(self, positions):
        """Update method for a human, allows the human to resign.
        """
        move_num = sum([1 if x != "-" else 0 for x in positions])
        move = input("Move #" + str(move_num + 1) +':')
        if move == "Q":
            self.quit()
            return 0
        else:
            return move

    def menace_move(self, positions):
        """Move method for menace, allows the use of a playbook to select a move.
        """
        from random import choice

        tup_positions = tuple(positions)
        if tup_positions not in self.playbook:
            move = self.random_move(positions)
            return move
        else:
            move = choice(self.playbook[tup_positions])
            return move

    def update_menace(self, win):
        """Reinforcement update method for menace.
        """
        if not win:  # it was a tie
            for position in self.move_history:
                if position in self.playbook:
                    self.playbook[position].extend([self.move_history[position]])
                else:
                    temp = [self.move_history[position]]
                    not_filled = [i for i, x in enumerate(position) if x == "-"]
                    temp.extend(not_filled[1:])
                    self.playbook[position] = temp

        elif win[1] == self.piece:  # it was a win, reinforce all the moves
            for position in self.move_history:
                if position in self.playbook:
                    self.playbook[position].extend(3 * [self.move_history[position]])
                else:
                    temp = 2 * [self.move_history[position]]
                    not_filled = [i for i, x in enumerate(position) if x == "-"]
                    temp.extend(not_filled[1:])
                    self.playbook[position] = temp

        elif win[1] != self.piece:  # it was a loss, prune once
            for position in self.move_history:
                if position in self.playbook:
                    if self.move_history[position] in self.playbook[position]:
                        self.playbook[position].remove(self.move_history[position])
                        if not self.playbook[position]:
                            self.playbook.pop(position)

    def random_move(self, positions):
        """Method for selecting a random option from the available legal moves.
        """
        from random import choice

        not_filled = [i for i, x in enumerate(positions) if x == "-"]
        return choice(not_filled[1:])

    def quit(self):
        """Method for ending a game.
        """
        import sys

        print(self.piece, " quits!")
        sys.exit()


class Board:
    """Board handles the display of the tic-tac-toe board state.
    """

    def __init__(self, turtle=False, size=200):
        self.positions = ["-"] * 10
        self.turtle = turtle
        if self.turtle:

            self.size = size
            self.squares = {
                1: [-size, size],
                2: [0, size],
                3: [size, size],
                4: [-size, 0],
                5: [0, 0],
                6: [size, 0],
                7: [-size, -size],
                8: [0, -size],
                9: [size, -size],
            }

    def turtle_display(self):
        import turtle
        import turtle_board

        turtle.reset()
        turtle.speed(0)
        turtle_board.board(size=200)

        for i in range(1, 10):
            if self.positions[i] == "X":
                turtle_board.x(self.squares[i], self.size)
            elif self.positions[i] == "O":
                turtle_board.o(self.squares[i], self.size / 2)

    def display(self, humanAgent=True, turtle=False):
        from os import system
        #from IPython.display import clear_output

        system("clear")
        #clear_output()
        for i in range(3):
            print("\t".join(self.positions[1 + i * 3 : 1 + i * 3 + 3]))
        if self.turtle:
            self.turtle_display()

    def update(self, move, piece):
        # check for clashes
        try:
            move = int(move)
            assert move >= 1 and move <= 9
        except:
            print("That was probably not a valid move, try again")
            return False
        if self.positions[move] != "-":
            print(move, self.positions)
            raise ValueError("That space is filled")
            return False
        else:
            self.positions[move] = piece
            return True

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


class Game:
    def __init__(self, board, x, o, watcher=False):
        self.board = board
        self.playerX = x
        self.playerO = o
        self.human = x.human or o.human
        self.playerX.move_history = {}
        self.playerO.move_history = {}
        self.watcher = watcher

    def play(self):
        import time

        turn = 1
        if self.watcher:
            time.sleep(1.5)
            self.board.display()

        while turn < 10:
            if turn % 2 == 1:
                move = self.playerX.mover(self.board.positions)
                if self.board.update(move, self.playerX.piece):
                    move = int(move)
                    temp = self.board.positions[:]
                    temp[move] = "-"
                    self.playerX.move_history[tuple(temp)] = move
                else:
                    continue
            else:
                move = self.playerO.mover(self.board.positions)
                if self.board.update(move, self.playerO.piece):
                    move = int(move)
                    temp = self.board.positions[:]
                    temp[move] = "-"
                    self.playerO.move_history[tuple(temp)] = move
                else:
                    continue

            self.win = self.board.is_win()
            if self.watcher:
                time.sleep(1.5)
                self.board.display()
            if self.win:
                break
            turn += 1

        if self.watcher:
            if not self.win:
                print("It was a tie")
            else:
                print(self.win[1], " wins!!")

        self.playerX.update(self.win)
        self.playerO.update(self.win)

        if self.watcher:
            time.sleep(1.5)


class Experiment:
    def __init__(self, X, O, trials, logname=None, watcher=False):
        self.trials = trials
        self.playerX = X
        self.playerO = O
        self.xwins = 0
        self.owins = 0
        self.ties = 0
        self.logname = logname
        self.watcher = watcher

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
        b = Board()
        g = Game(b, self.playerX, self.playerO, watcher=self.watcher)
        g.play()
        if not g.win:
            self.ties += 1
        elif g.win[1] == "X":
            self.xwins += 1
        elif g.win[1] == "O":
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


me = Agent(piece='X', mover='menace')
you = Agent(piece='O', mover='random')
E = Experiment(me, you, 10000, watcher=False, logname="log1.txt")
E.runExperiment()
