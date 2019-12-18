from tictac import *
import numpy as np
import tensorflow as tf

class NeuralAgent(Agent):
    def __init__(self, model=None, **kwargs):
        super().__init__(mover="nonhuman", **kwargs)
        self.model = model

    def mover(self, positions):
        inputs = self.encode(positions)
        output = self.net_apply(inputs)
        not_filled = [i for i, x in enumerate(positions) if x == "-"]
        not_filled.pop(0)
        while True:
            move = np.argmax(output)
            if move not in not_filled:
                #print("filled", output, move)
                output[move] = 0
            else:
                break
        return move

    def update(self, win):
        pass

    def encode(self, positions):
        encoding = {'-':0, 'X': 1, 'O': 2}
        return np.array([encoding[x] for x in positions[1:]])

    def net_apply(self, inputs):
        if self.model is None: #make a model
            self.h1_biases = np.random.rand(9)
            self.in_to_h1_weights = np.random.rand(9,9)
            self.h1_to_out_weights = np.random.rand(9,9)
            self.out_biases = np.random.rand(9)
            self.model = True
        #use the model
        wzb1_to_h = np.dot(self.in_to_h1_weights, inputs) \
                        + self.h1_biases
        act_h = sigmoid(wzb1_to_h)
        wzbh_to_o = np.dot(self.h1_to_out_weights, act_h)\
                        + self.out_biases
        return sigmoid(wzbh_to_o)

def sigmoid(z):
    return 1/(1+np.exp(-z))
