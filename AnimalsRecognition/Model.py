import tensorflow as tf
import json


class Model():

    def __init__(self):
        with open("Conf/dataset.json") as file:
            self.config = json.load(file)
            self.imageSize = self.config["imageSize"]
            self.numClasses = len(self.config["labels"])
            self.channels = self.config["channels"]
        return

    def createCompGraph(self):
        # todo improve the model. model has staggering accuracy at 50 percent
        self.input = tf.placeholder(tf.float32, shape=[None, self.imageSize, self.imageSize, self.channels],
                                    name="input")
        self.output = tf.placeholder(tf.float32, shape=[None, self.numClasses], name="output")

        inputImage = tf.reshape(self.input, shape=[-1, self.imageSize, self.imageSize, self.channels])

        conv1 = tf.layers.conv2d(inputImage, 8, kernel_size=[5, 5], strides=(2, 2), padding="SAME")
        self.pool1 = tf.layers.average_pooling2d(conv1, pool_size=[2, 2], strides=[2, 2])

        flat = tf.layers.flatten(self.pool1)

        dropout = tf.layers.dropout(flat, self.config["model"]["dropout"])

        dense = tf.layers.dense(dropout, units=self.numClasses)

        self.logits = tf.nn.softmax(dense)

        self.loss = tf.losses.softmax_cross_entropy(logits=self.logits, onehot_labels=self.output)

        self.accuracy = tf.reduce_mean(
            tf.cast(
                tf.equal(tf.arg_max(self.logits, 1), tf.arg_max(self.output, 1))
                , tf.float32
            )
        )

        self.learningRate = self.config["model"]["learningRate"]

        self.optimizer = tf.train.GradientDescentOptimizer(self.learningRate).minimize(self.loss)

        return

    def intializeModel(self):
        self.sess = tf.InteractiveSession()
        tf.initialize_all_variables().run()
        return

    def train(self, images, output):
        _, acc, lo = self.sess.run([self.optimizer, self.accuracy, self.loss], feed_dict={
            self.input: images,
            self.output: output
        })

        return acc, lo

    def test(self, images, output):
        acc, lo = self.sess.run([self.accuracy, self.loss], feed_dict={
            self.input: images,
            self.output: output
        })

        return acc, lo

    def predict(self, images):
        labels = self.sess.run([self.logits], feed_dict={
            self.input: images
        })
        return labels

    def visualize(self, images):
        layer = self.sess.run([self.pool1], feed_dict={
            self.input: images
        })
        return layer
