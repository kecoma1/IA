"""
In this file we are going to define our neural network
The neural nextwork is going to have the following inputs:
-
-
-
The output of the neural network represents the value of the evaluation
function

The network must be trained, for this we developed
the backpropagation algorithm.
"""
import numpy as np


def compute(layer_weights, values):
    next_laxer = layer_weights.dot(values)
    return next_laxer


# inputs = np.random.rand(2,1)
inputs = np.matrix('1 ; 0')
print("Inputs")
print(inputs)
print()

# We initialize the initial weights with random values
# first_layer_weights = np.random.rand(3,2)
first_layer_weights = np.matrix([[0, 0],
                                 [1, 1],
                                 [0, 1]])
print("First layer weights")
print(first_layer_weights)
print()

# Computing the value of the next layer
next_layer = compute(first_layer_weights, inputs)
print("Second laxer values (neurons)")
print(next_layer)
print()

# We initialize the second layer weights with
# random values
# second_layer_weights = np.random.rand(2,3)
second_layer_weights = np.array([[0, 0, 0],
                                 [1, 1, 1]])
print("Second laxer weights")
print(second_layer_weights)
print()


# Computing the value of the output
output = compute(second_layer_weights, next_layer)
print(output)
