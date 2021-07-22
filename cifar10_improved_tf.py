# -*- coding: utf-8 -*-
"""CIFAR10_IMPROVED_TF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ymR8-zbgTDO0_nWcMSXpx6TltpW49grk
"""

# Author -- Berkant Bayraktar

import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import Input
from tensorflow.keras import utils
from tensorflow.keras import datasets
from tensorflow.keras import preprocessing

import matplotlib.pyplot as plt
import numpy as np

import requests
requests.packages.urllib3.disable_warnings()
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

cifar10 = datasets.cifar10.load_data() # Load CIFAR10 Dataset using Keras API

((x_train, y_train),(x_test, y_test)) = cifar10

print('Train: X=%s, y=%s' % (x_train.shape, y_train.shape))
print('Test: X=%s, y=%s' % (x_test.shape, y_test.shape))
# plot first few images
for i in range(9):
	# define subplot
	plt.subplot(330 + 1 + i )
	# plot raw pixel data
	plt.imshow(x_train[i], cmap=plt.get_cmap('gray'))
# show the figure
plt.show()

(x_train, x_test) = (x_train / 255, x_test / 255)
y_train = utils.to_categorical(y_train, 10)
y_test = utils.to_categorical(y_test, 10)

class ConvolutionNET:
    def __init__(self,number_of_classes):
        self.model = None
        self.number_of_classes = number_of_classes
    def createModel(self):
        self.model = models.Sequential([
            Input(shape = (32,32,3)), 
            layers.Conv2D(32,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_1"),
            #layers.BatchNormalization(),
            layers.Conv2D(32,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_2"),
            #layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size = (2,2), strides = 2),
            
            layers.Conv2D(64,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_3"),
            #layers.BatchNormalization(),
            layers.Conv2D(64,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_4"),
            #layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size = (2,2), strides = 2),
            
            layers.Conv2D(128,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_5"),
            #layers.BatchNormalization(),
            layers.Conv2D(128,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_6"),
            #layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size = (2,2), strides = 2),

            layers.Flatten(),
            layers.Dropout(rate = 0.5),
            layers.Dense(1024, activation= 'relu'),
            layers.Dropout(rate = 0.25),
            layers.Dense(128, activation= 'relu'),
            layers.Dropout(rate = 0.2),
            layers.Dense(10, activation='softmax')
        ])

Cnet = ConvolutionNET(number_of_classes=10)
Cnet.createModel()

optimizer = optimizers.Adam(learning_rate = 0.001)
Cnet.model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics= ['accuracy'])
res = Cnet.model.fit(x = x_train, y = y_train, epochs=15, batch_size = 32, validation_data = (x_test,y_test))

plt.plot(res.history['loss'], label = 'loss')
plt.plot(res.history['val_loss'], label = 'val_loss')
plt.legend()

plt.plot(res.history['accuracy'], label = 'accuracy')
plt.plot(res.history['val_accuracy'], label = 'val_accuracy')
plt.legend()

Cnet.model.summary()

Cnet = ConvolutionNET(number_of_classes=10)
Cnet.createModel()
optimizer = optimizers.Adam(learning_rate = 0.001)
Cnet.model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics= ['accuracy'])
data_generator = preprocessing.image.ImageDataGenerator(width_shift_range= 0.1, height_shift_range= 0.1 , horizontal_flip= True)
train_generator = data_generator.flow(x=x_train, y=y_train, batch_size= 32)
steps_per_epoch = len(train_generator)

res = Cnet       .model.fit_generator(generator=train_generator, steps_per_epoch= steps_per_epoch ,validation_data= (x_test, y_test), epochs = 15)

plt.plot(res.history['loss'], label = 'loss')
plt.plot(res.history['val_loss'], label = 'val_loss')
plt.legend()

plt.plot(res.history['accuracy'], label = 'accuracy')
plt.plot(res.history['val_accuracy'], label = 'val_accuracy')
plt.legend()



