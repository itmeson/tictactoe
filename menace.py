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
