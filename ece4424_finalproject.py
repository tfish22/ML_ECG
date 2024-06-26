# -*- coding: utf-8 -*-
"""ECE4424_FinalProject.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jFukKc7kd6evw_ikHecVZXkFsjOMSRzd
"""

from tensorflow import keras
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras.callbacks import ModelCheckpoint
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import to_categorical

class_names = {0:'Normal', 1:'Suprventricular', 2:'Ventricular', 3:'Fusion', 4:'Unknown'}
num_classes = 5
epochs = 25

from google.colab import drive
drive.mount('/content/drive')

"""Load the train data and test data"""

train_file = "/content/drive/My Drive/mitbih_train.csv"
test_file = "/content/drive/My Drive/mitbih_test.csv"
train_data = pd.read_csv(train_file)
test_data = pd.read_csv(test_file)

"""Organize Data into their Classifications:

Method for organizing data into their classifications. This is done to better understand the dataset sparsity.
"""

def generateBins(data):
  bins = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
  for i in range(len(data)):
    bins[data.iloc[i][187]] += 1
  print(bins)

train_bins = generateBins(train_data)
test_bins = generateBins(test_data)

"""Splitting Data:

Datasets are split between the ECG readings, x_train, and classification, y_train. The test dataset is split in the same way. x_train and x_test are reshaped to be valid with a convolutional neural network.
"""

x_train = train_data.iloc[:, :-1].values
y_train = train_data.iloc[:, -1].values

x_test = test_data.iloc[:, :-1].values
y_test = test_data.iloc[:, -1].values

x_train.reshape(len(x_train), x_train.shape[1], 1)
x_test.reshape(len(x_test), x_test.shape[1], 1)

"""Plotting ECG Readings:

Plots of the first 25 ECG readings in the dataset
"""

plt.figure(figsize=(10,10))
x_plots = []
y_plots = []
for i in range(len(x_train)):
  if(y_train[i] == 0):
    if(len(x_plots) == 1):
      continue
    x_plots.append(x_train[i])
    y_plots.append(y_train[i])
  if(y_train[i] == 1):
    if(len(x_plots) == 2):
      continue
    x_plots.append(x_train[i])
    y_plots.append(y_train[i])
  if(y_train[i] == 2):
    if(len(x_plots) == 3):
      continue
    x_plots.append(x_train[i])
    y_plots.append(y_train[i])
  if(y_train[i] == 3):
    if(len(x_plots) == 4):
      continue
    x_plots.append(x_train[i])
    y_plots.append(y_train[i])
  if(y_train[i] == 4):
    x_plots.append(x_train[i])
    y_plots.append(y_train[i])
    break

for i in range(5):
    plt.subplot(5,5,i+1)

    axis = plt.gca()
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    plt.plot((x_plots[i]))
    plt.title((class_names[y_plots[i]]))
plt.show()

"""CNN Model:

Model uses a 1D convolutional neural network. The network uses two stacks with two layers each. Activation used for the conbolutional layers is relu. A dropout of 0.25 is used. Optimizer used compile was adam.
"""

def first_cnn():
  model = Sequential()

  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(187, 1)))

  model.add(MaxPooling1D(pool_size=2))
  model.add(Dropout(0.25))

  model.add(Flatten())
  model.add(Dense(64, activation='relu'))
  model.add(Dropout(0.25))


  model.add(Dense(5, activation='softmax'))
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

  print(model.summary())
  return model

def second_cnn():
  model = Sequential()

  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(187, 1)))
  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(187, 1)))

  model.add(MaxPooling1D(pool_size=2))
  model.add(Dropout(0.25))

  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(187, 1)))
  model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(187, 1)))

  model.add(MaxPooling1D(pool_size=2))
  model.add(Dropout(0.25))

  model.add(Flatten())
  model.add(Dense(64, activation='relu'))
  model.add(Dropout(0.25))


  model.add(Dense(5, activation='softmax'))
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

  print(model.summary())
  return model

"""Training the Model:

Train the model and save the best model iteration. Model trains with previous created x_train, and y_train data. Model is trained over 25 epochs. Model is validated with x_test and y_test data. Lastly, the training and validation accuracies are plotted as well as the loss.
"""

history_activations = dict()
current_base = ModelCheckpoint(filepath='best_model.h5', monitor='val_accuracy', save_best_only=True)
model = first_cnn()
history = model.fit(x_train, y_train, epochs=25, batch_size=32, validation_split=0.2, callbacks=[current_base], validation_data=(x_test,y_test))

fig1, acc=plt.subplots()
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracies')
plt.legend()
plt.show()

fig2, acc=plt.subplots()
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Losses')
plt.legend()
plt.show()

best_model = load_model('best_model.h5')
scores = best_model.evaluate(x_test, y_test, verbose=1)
print('Loss {}'.format(scores[0]))
print('Test accuracy {}'.format(scores[1]))

history_activations = dict()
current_base = ModelCheckpoint(filepath='best_model.h5', monitor='val_accuracy', save_best_only=True)
model = second_cnn()
history = model.fit(x_train, y_train, epochs=25, batch_size=32, validation_split=0.2, callbacks=[current_base], validation_data=(x_test,y_test))

fig1, acc=plt.subplots()
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and Validation Accuracies')
plt.legend()
plt.show()

fig2, acc=plt.subplots()
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Losses')
plt.legend()
plt.show()

best_model = load_model('best_model.h5')
scores = best_model.evaluate(x_test, y_test, verbose=1)
print('Loss {}'.format(scores[0]))
print('Test accuracy {}'.format(scores[1]))