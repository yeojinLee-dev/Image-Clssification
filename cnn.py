# -*- coding: utf-8 -*-
"""CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sxg02gsiXQ-KDZ7W9yBrLpq5XUTh3XRC
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

# 0~255의 픽셀값을 가지는 이미지들을 CNN 모델에 입력하기 위해 0~1의 값을 갖도록 조정
(x_train, x_test) = (x_train / 255, x_test / 255)
y_train = utils.to_categorical(y_train, 10)
y_test = utils.to_categorical(y_test, 10)

class berkantNET:
    def __init__(self,number_of_classes):
        self.model = None
        self.number_of_classes = number_of_classes
    def createModel(self):
        self.model = models.Sequential([
            Input(shape = (32,32,3)), 
            layers.Conv2D(32,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_1"),
            layers.Dropout(rate = 0.2),
            layers.Conv2D(32,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_2"),
            layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size = (2,2), strides = 2),
            layers.Conv2D(64,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_3"),
            layers.BatchNormalization(),
            layers.Dropout(rate = 0.2),
            layers.Conv2D(64,(3,3), strides=(1,1), padding= 'same', activation = 'relu', use_bias=True, name = "layer_4"),
            layers.BatchNormalization(),
            layers.MaxPooling2D(pool_size = (2,2), strides = 2),
            
            layers.Flatten(),
            layers.Dropout(rate = 0.2),
            layers.Dense(1024, activation= 'relu'),
            layers.Dropout(rate = 0.2),
            layers.Dense(10, activation='softmax')
        ])

bnet = berkantNET(number_of_classes=10)
bnet.createModel()

optimizer = optimizers.Adam(learning_rate = 0.001)
bnet.model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics= ['accuracy'])
res = bnet.model.fit(x = x_train, y = y_train, epochs=100, batch_size = 32, validation_data = (x_test,y_test))

plt.plot(res.history['loss'], label = 'loss')
plt.plot(res.history['val_loss'], label = 'val_loss')
plt.legend()

plt.plot(res.history['accuracy'], label = 'accuracy')
plt.plot(res.history['val_accuracy'], label = 'val_accuracy')
plt.legend()

bnet.model.summary()

bnet = berkantNET(number_of_classes=10)
bnet.createModel()
optimizer = optimizers.Adam(learning_rate = 0.001)
bnet.model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics= ['accuracy'])
data_generator = preprocessing.image.ImageDataGenerator(width_shift_range= 0.1, height_shift_range= 0.1 , horizontal_flip= True)
train_generator = data_generator.flow(x=x_train, y=y_train, batch_size= 32)
steps_per_epoch = len(train_generator)

res = bnet.model.fit_generator(generator=train_generator, steps_per_epoch= steps_per_epoch ,validation_data= (x_test, y_test), epochs = 100)

plt.plot(res.history['loss'], label = 'loss')
plt.plot(res.history['val_loss'], label = 'val_loss')
plt.legend()

plt.plot(res.history['accuracy'], label = 'accuracy')
plt.plot(res.history['val_accuracy'], label = 'val_accuracy')
plt.legend()
