
""" Siamese implementation using Tensorflow with MNIST example.
This siamese network embeds a 28x28 image (a point in 784D) 
into a point in 2D.

By Youngwook Paul Kwon (young at berkeley.edu)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.examples.tutorials.mnist import input_data # for data
import tensorflow as tf
import numpy as np
import os

import siame
import visualize

# prepare data and tf.session
mnist = input_data.read_data_sets('MNIST_data', one_hot=False)
sess = tf.InteractiveSession()

# setup siamese network
siam = siame.siamese();
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(siam.loss)
saver = tf.train.Saver()

# start training
tf.initialize_all_variables().run()

for step in range(100000):
    batch_x1, batch_y1 = mnist.train.next_batch(128)
    batch_x2, batch_y2 = mnist.train.next_batch(128)
    batch_y = (batch_y1 == batch_y2).astype('float')

    _, loss_v = sess.run([train_step, loss], feed_dict={
                        siame.x1: batch_x1, 
                        siame.x2: batch_x2, 
                        siame.y_: batch_y})

    if np.isnan(loss_v):
        print('Model diverged with loss = NaN')
        quit()

    if step % 10 == 0:
        print ('step %d: loss %.3f' % (step, loss_v))

    if step % 1000 == 0 and step > 0:
        saver.save(sess, 'model.ckpt')

# start embed (testing)
embed = siam.o1.eval({siam.x1: mnist.test.images})
embed.tofile('embed.txt')

# visualize result
x_test = mnist.test.images.reshape([-1, 28, 28])
visualize.visualize(embed, x_test)