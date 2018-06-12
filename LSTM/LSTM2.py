""" Recurrent Neural Network.
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Links:
    [Long Short Term Memory](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn

import numpy
import csv

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

'''
To classify images using a recurrent neural network, we consider every image
row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
handle 28 sequences of 28 steps for every sample.
'''

"""
이전노드위도, 이전노드경도, 현재위도, 현재경도, 다음노드위도, 다음노드경도
이탈
"""




# Training Parameters
learning_rate = 0.001
training_steps = 10000
batch_size = 128
display_step = 10

# Network Parameters
num_input = 6 # 입력변수의 크기
timesteps = 1
num_hidden = 128 # hidden layer num of features
num_classes = 2 # MNIST total classes (0-9 digits)

# tf Graph input
X = tf.placeholder("float", [None, timesteps, num_input])
Y = tf.placeholder("float", [None, num_classes])

# Define weights
weights = {
    'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([num_classes]))
}


def RNN(x, weights, biases):

    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)


    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


logits = RNN(X, weights, biases)
prediction = tf.nn.softmax(logits)

# Define loss and optimizer
loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=logits, labels=Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

# Evaluate model (with test logits, for dropout to be disabled)
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training

batch_x, batch_y = mnist.train.next_batch(batch_size)


# print(batch_x.reshape(128, 28, 28).tolist())

# print(len(batch_x)) #128
# print(len(batch_x[0])) #28*28
# print("\n\n\n\n")
# batch_x = batch_x.reshape((batch_size, timesteps, num_input)) #128*28*28 형태로 변환
# print(batch_x)
#
# print(len(batch_y))
# print(len(batch_y[0])) #128 * 10
# for i in range(10):
#     print(batch_y[i])


data = []
with open('trainingData.csv','r') as csvfile:
    plot = csv.reader(csvfile, delimiter=',')
    for row in plot:
        data += [row]

train_x = []
train_y = []

size = (len(data) - len(data)%batch_size)

tx = list()
ty = []
for i in range(0, size):
    if i % batch_size == 0:
        train_x += [tx]
        train_y += [ty]
        tx = []
        ty = []
    else:
        tx.append([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5]])
        if data[i][0] == 0:
            ty += [[1, 0]]
        else:
            ty += [[0, 1]]

print(tx)
print(len(tx))
print(tx[0])


# xxx = numpy.asarray(train_x)
# print(list(train_x))
# print(len(xxx))
# print(len(xxx[0]))
# with tf.Session() as sess:
#
#     # Run the initializer
#     sess.run(init)
#
#
#     for step in range(0, len(train_x)):
#         # batch_x, batch_y = mnist.train.next_batch(batch_size)
#
#         batch_x = train_x[step]
#         batch_y = train_y[step]
#
#         print(batch_x)
#         batch_x = numpy.asarray(batch_x)
#
#         batch_x = batch_x.reshape((batch_size, num_input))
#         # batch_y = batch_y.reshape((batch_size, num_classes))
#         # Reshape data to get 28 seq of 28 elements
#         # batch_x = batch_x.reshape((batch_size, num_input))
#         # Run optimization op (backprop)
#         sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
#         if step % display_step == 0 or step == 1:
#             # Calculate batch loss and accuracy
#             loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
#                                                                  Y: batch_y})
#             print("Step " + str(step) + ", Minibatch Loss= " + \
#                   "{:.4f}".format(loss) + ", Training Accuracy= " + \
#                   "{:.3f}".format(acc))
#
#     print("Optimization Finished!")
#
#     # Calculate accuracy for 128 mnist test images
#     test_len = 128
#     test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
#     test_label = mnist.test.labels[:test_len]
#     print("Testing Accuracy:", \
#         sess.run(accuracy, feed_dict={X: test_data, Y: test_label}))
#
