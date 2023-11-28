# inputs = [1,2,3,2.5]
# weights = [
#     [0.2, 0.8, -0.5, 1],
#     [0.5, -0.91, 0.26, -0.5],
#     [-0.26, -0.27, 0.17, 0.87]
# ]
# biases = [2, 3, 0.5]

# layer_outputs = []

# for n_weights, n_bias in zip(weights, biases):
#     neuron_output = 0

#     for n_input, weight, in zip(inputs, n_weights):
#         neuron_output += n_input*weight

#     neuron_output += n_bias

#     layer_outputs.append(neuron_output)

# print(layer_outputs)

# ------------------------------------------
# ReLu, forwarding
# ------------------------------------------

import numpy as np
import nnfs
from nnfs.datasets import spiral_data
from nnfs.datasets import vertical_data
import matplotlib.pyplot as plt
import math

nnfs.init()


class Layer_Dense:
    # Initialize weights and biases
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))

    # Forward Pass
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class Activation_ReLU:
    # Forward pass
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

# X, y = spiral_data(samples=100, classes=3)

# dense1 = Layer_Dense(2, 3)

# activation1 = Activation_ReLU()

# dense1.forward(X)

# activation1.forward(dense1.output)

# print(activation1.output[:5])

# plt.scatter(X[:, 0], X[:, 1], c=y, cmap='brg')
# plt.show()

# -----------------------------------------------
# Softmax
# -----------------------------------------------
# import math
# layer_outputs = [4.8, 1.21, 2.385] 
# E = math.e     # ~2.71828182846

# exp_values = []
# for output in layer_outputs:
#     exp_values.append(E**output)

# print('Exponentiated Values:')
# print(exp_values)

# norm_base = sum(exp_values)
# norm_values = []
# for value in exp_values:
#     norm_values.append(value / norm_base)

# print('Normalized Exponential values:')
# print(norm_values)

# print('Sum of normalized values:', sum(norm_values))


# -----------------------------------------------
# Numpy version
# -----------------------------------------------

# import numpy as np

# # layer_outputs = [4.8, 1.21, 2.385]
# layer_outputs = np.array([
#     [4.8, 1.21, 2.385],
#     [8.9, -1.81, 0.2],
#     [1.41, 1.051, 0.026]
# ])

# # calculate exponential values for each value in vector
# exp_values = np.exp(layer_outputs)
# print('exponentiated values:')
# print(exp_values)

# # Normalize values
# norm_values = exp_values / np.sum(exp_values)
# print('normalized exponentiated values:')
# print(norm_values)
# print('sum of normalized values:', np.sum(norm_values))

# print(np.sum(layer_outputs, axis=1, keepdims=True))


# -----------------------------------------------
# Softmax activation
# -----------------------------------------------

class Activation_Softmax:
    
    # Forward pass
    def forward(self, inputs):

        # get unnormalized probabilities
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))

        # Normalize them for each sample
        probilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)

        self.output = probilities


# X, y = spiral_data(samples=100, classes=3)

# # # Create dense layer with 2 input and 3 outpet
# dense1 = Layer_Dense(2, 3)
# # # Create reLU activation used with Dense Layer
# activation1 = Activation_ReLU()

# # # Create second Dense layer with 3 input (adding output of previous layer) 3 output
# dense2 = Layer_Dense(3, 3)
# # # Create Softmax activation used with Dense layer
# activation2 = Activation_Softmax()

# # # Forward pass of training data
# dense1.forward(X)
# # # Forward pass through activation function using output of dense layer
# activation1.forward(dense1.output)
# # # Forward pass through second dense layer
# dense2.forward(activation1.output)
# # # Make a forward pass through activation function
# activation2.forward(dense2.output)

# print(activation2. output[:5])

# -----------------------------------------------
# 5. Loss Functions
# -----------------------------------------------


# ------
# - Categorical Cross-Entropy Loss
# ------

# import math

# softmax_output = [0.7,0.1,0.2]
# target_output = [1,0,0]

# loss = -(math.log(softmax_output[0])*target_output[0] +
#          math.log(softmax_output[1])*target_output[1] +
#          math.log(softmax_output[2])*target_output[2]
#          )
# loss_optimized = -math.log(softmax_output[0])

# print(loss, loss_optimized)

# -------------------------
softmax_outputs = np.array([[0.7,0.1,0.2],
                            [0.1,0.5,0.4],
                            [0.02,0.9,0.08]])

softmax_outputs2 = np.array([[0.7,0.1,0.2],
                            [0.5,0.1,0.4],
                            [0.02,0.9,0.08]])

class_targets1 = np.array([0,1,1])
class_targets2 = np.array([[1,0,0],
                        [0,1,0],
                        [0,1,0]])

# if len(class_targets2.shape) == 1:
#     correct_confidences = softmax_outputs[
#         range(len(softmax_outputs)),
#         class_targets2
#     ]
# elif len(class_targets2.shape) == 2:
#     correct_confidences = np.sum(
#         softmax_outputs * class_targets2,
#         axis=1
#     )
# neg_log = -np.log(correct_confidences)
# average_loss = np.mean(neg_log)
# print(average_loss)

# ------
# Common loss class
# ------

class Loss:
    def calculate(self, output, y):
        
        sample_losses = self.forward(output, y)

        data_loss = np.mean(sample_losses)

        return data_loss
    
# ------
# Cross-entropy loss class
# ------

class Loss_CategoricalCrossentropy(Loss):

    def forward(self, y_pred, y_true):

        samples = len(y_pred)

        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[
                range(samples),
                y_true
            ]
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(
                y_pred_clipped * y_true,
                axis=1
            )
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods
    
# X, y = spiral_data(samples=100, classes=3)

# # # Create dense layer with 2 input and 3 outpet
# dense1 = Layer_Dense(2, 3)
# # # Create reLU activation used with Dense Layer
# activation1 = Activation_ReLU()

# # # Create second Dense layer with 3 input (adding output of previous layer) 3 output
# dense2 = Layer_Dense(3, 3)
# # # Create Softmax activation used with Dense layer
# activation2 = Activation_Softmax()

# loss_function = Loss_CategoricalCrossentropy()
# # # Forward pass of training data
# dense1.forward(X)
# # # Forward pass through activation function using output of dense layer
# activation1.forward(dense1.output)
# # # Forward pass through second dense layer
# dense2.forward(activation1.output)
# # # Make a forward pass through activation function
# activation2.forward(dense2.output)

# print(activation2. output[:5])

# loss = loss_function.calculate(activation2.output, y)
# print('Loss:',loss)

# --------

# predictions = np.argmax(softmax_outputs2, axis=1)

# if len(class_targets1.shape) == 2:
#     class_targets1 = np.argmax(class_targets1, axis=1)

# accuracy = np.mean(predictions==class_targets1)

# --------

# predictions = np.argmax(activation2.output, axis=1)

# if len(y.shape) == 2:
#     y = np.argmax(y, axis=1)
#     # class_targets1 = np.argmax(class_targets1, axis=1)

# accuracy = np.mean(predictions==y)

# print('Accuracy', accuracy)


# -----------------------------------------------
# 6. Intro to Optimization
# -----------------------------------------------

# Create dataset
X, y = vertical_data(samples=100, classes=3)
plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap='brg')
plt.show()
# Create manual
dense1 = Layer_Dense(2,3)
activation1 = Activation_ReLU()
dense2 = Layer_Dense(3,3)
activation2 = Activation_Softmax()


# Create loss function
loss_function = Loss_CategoricalCrossentropy()

# Helper variables
lowest_loss = 9999999
best_dense1_weights = dense1.weights.copy()
best_dense1_biases = dense1.biases.copy()
best_dense2_weights = dense2.weights.copy()
best_dense2_biases = dense2.biases.copy()

for iteration in range(10000):

    # Update weights with some small random values
    dense1.weights += 0.05 * np.random.randn(2,3)
    dense1.biases += 0.05 * np.random.randn(1,3)
    dense2.weights += 0.05 * np.random.randn(3,3)
    dense2.biases += 0.05 * np.random.randn(1,3)

    # Perform a forward pass of our training data through this layer
    dense1.forward(X)
    activation1.forward(dense1.output)
    dense2.forward(activation1.output)
    activation2.forward(dense2.output)

    # Perform a forward pass through activation function
    # Takes output of second dense layer here and returns loss
    loss = loss_function.calculate(activation2.output, y)

    # Calculate accuracy from output of activation2 and targets
    # Calculate values along first axis
    predictions = np.argmax(activation2.output, axis=1)
    accuracy = np.mean(predictions==y)

    # If loss is smaller - print and save weights and biases aside
    if loss < lowest_loss:
        print('New set of weights found, iteration:', iteration, 
              'Loss:', loss, 
              'Accuracy:', accuracy)
        best_dense1_weights = dense1.weights.copy()
        best_dense1_biases = dense1.biases.copy()
        best_dense2_weights = dense2.weights.copy()
        best_dense2_biases = dense2.biases.copy()
        lowest_loss = loss

    # Revert weights and biases
    else:
        dense1.weights = best_dense1_weights.copy()
        dense1.biases = best_dense1_biases.copy()
        dense2.weights = best_dense2_weights.copy()
        dense2.biases = best_dense2_biases.copy()
