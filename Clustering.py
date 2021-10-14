# -*- coding: utf-8 -*-
"""SOM Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tTcZpj_KA5Kunxvky9g4kJiq7TClHydd
"""

#!pip install --upgrade tensorflow==1.15

import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class SOM:
    # self == this (js, java, c/c++)
    # Constructor
    def __init__(self, width, height, n_features, learning_rate):
        self.width = width
        self.height = height
        self.n_features = n_features
        self.learning_rate = learning_rate

        # self.cluster = [ [] for _ in range(height)]
        # ATAU
        self.cluster = []
        for i in range(height):
            self.cluster.append([])

        self.weight = tf.Variable(
            tf.random.normal(
                [width * height, n_features]
            ),
            tf.float32
        )

        self.input = tf.placeholder(tf.float32, [n_features])
        self.location = []

        for y in range(height):
            for x in range(width):
                self.location.append(
                    tf.cast([y, x], tf.float32)
                )

        self.bmu = self.get_bmu()
        self.update = self.update_neighbor() # mirip sess.run optimizer

    # [x, y, z].sum().mean()
    # [x, y, z].sum().mean()
    # [x, y, z].sum().mean()
 
    # Mencari neuron yang paling mirip
    def get_bmu(self):
        distance = tf.sqrt(
            tf.reduce_mean(
                (self.weight - self.input) ** 2, axis=1
            )
        )

        bmu_index = tf.argmin(distance)
        bmu_location = tf.cast([
            tf.div(bmu_index, self.width), 
            tf.mod(bmu_index, self.width)
            ], tf.float32)
        
        return bmu_location

    def update_neighbor(self):
        distance = tf.sqrt(
            tf.reduce_mean(
                (self.bmu - self.location) ** 2, axis=1
            )
        )

        # formula untuk rate
        sigma = tf.cast(
            tf.maximum(self.width, self.height) / 2,
            tf.float32
        )

        neighbor_strength = tf.exp(-(distance ** 2) / (2 * sigma ** 2))
        rate = neighbor_strength * self.learning_rate

        stacked_rate = []
        for i in range(self.width * self.height):
            stacked_rate.append(
                tf.tile(
                    [rate[i]],
                    [self.n_features]
                )
            )
        
        delta = stacked_rate * (self.input - self.weight)
        new_weight = self.weight + delta

        return tf.assign(self.weight, new_weight)
    
    def train(self, dataset, num_epochs):
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            for epoch in range(1, num_epochs+1):
                
                for data in dataset:
                    dic = {
                        self.input: data
                    }
                    sess.run(self.update, feed_dict = dic)
                if epoch%100 == 0:
                    print(f"Epoch {epoch}: ", end='')
                    print('Done')

            location = sess.run(self.location)
            weight = sess.run(self.weight)

            for i, loc in enumerate(location):
                self.cluster[int(loc[0])].append(weight[i])

def change_odor(data):
  if data == "a":
    return 1
  elif data == "l":
    return 2
  elif data == "c":
    return 3
  elif data == "y":
    return 4
  elif data == "f":
    return 5
  elif data == "m":
    return 6
  elif data == "n":
    return 7
  elif data == "p":
    return 8
  elif data == "s":
    return 9
  else:
    return data

def change_stalk_shape(data):
  if data == "e":
    return 1
  elif data == "t":
    return 2
  else:
    return data

def change_veil_type(data):
  if data == "p":
    return 1
  elif data == "u":
    return 2
  else:
    return data

# DATASET
dataset = pd.read_csv("clustering.csv")

#Feature Selection
for i, data in enumerate(dataset["class"]):
  dataset["odor"][i] = change_odor(dataset["odor"][i])
  dataset["stalk-shape"][i] = change_stalk_shape(dataset["stalk-shape"][i])
  dataset["veil-type"][i] = change_veil_type(dataset["veil-type"][i])

data = dataset[["bruises", "odor", "stalk-shape", "veil-type", "spore-print-color"]]

scaler = StandardScaler().fit(data)
data = scaler.transform(data)

pca = PCA(n_components = 3)
pca.fit(data)
data = pca.transform(data)

som = SOM(8, 8, 3, 0.1)
som.train(data, 2500)
plt.imshow(som.cluster)
print(plt.show)