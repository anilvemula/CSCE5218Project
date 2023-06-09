import numpy as np
import pandas as pd
from keras.utils import load_img, img_to_array
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.callbacks import ModelCheckpoint

from keras.models import load_model

import os
print(os.listdir("fer2013/"))

filename = 'fer2013/fer2013.csv'
label_map = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
names = ['emotion', 'pixels', 'usage']
df = pd.read_csv('fer2013/fer2013.csv', names=names, na_filter=False)
im = df['pixels']
df.head(10)

def getData(filename):
    Y = []
    X = []
    first = True
    for line in open(filename):
        if first:
            first = False
        else:
            row = line.split(',')
            Y.append(int(row[0]))
            X.append([int(p) for p in row[1].split()])

    X, Y = np.array(X) / 255.0, np.array(Y)
    return X, Y

X, Y = getData(filename)
num_class = len(set(Y))
print(num_class)

N, D = X.shape
X = X.reshape(N, 48, 48, 1)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
y_train = (np.arange(num_class) == y_train[:, None]).astype(np.float32)
y_test = (np.arange(num_class) == y_test[:, None]).astype(np.float32)

def my_model():
    model = Sequential()
    input_shape = (48, 48, 1)
    model.add(Conv2D(64, (5, 5), input_shape=input_shape, activation='relu', padding='same'))
    model.add(Conv2D(64, (5, 5), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (5, 5), activation='relu', padding='same'))
    model.add(Conv2D(128, (5, 5), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(7))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

    return model


model = my_model()
model.summary()

path_model = 'model_filter.h5'
model = load_model(path_model)

from keras import backend as K
# save model at this location after each epoch
K.clear_session()
# destroys the current graph and builds a new one
model = my_model()
# create the model
K.set_value(model.optimizer.lr, 1e-3)
# set the learning rate
# fit the model
h = model.fit(x=X_train, y=y_train, batch_size=64, epochs=20, verbose=1, validation_data=(X_test, y_test), shuffle=True,
              callbacks=[
                  ModelCheckpoint(filepath=path_model), ])

objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
y_pos = np.arange(len(objects))
print(y_pos)

def emotion_analysis(emotions):
    objects = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, emotions, align='center', alpha=0.9)
    plt.tick_params(axis='x', which='both', pad=10, width=4, length=10)
    plt.xticks(y_pos, objects)
    plt.text(200, 200, "texting", fontsize=12, transform=plt.gcf().transFigure, color='blue')
    plt.ylabel('percentage')
    plt.title('emotion')

plt.show()

y_pred = model.predict(X_test)
y_test.shape

img = load_img('input/Shawon.jpg', grayscale=True, color_mode="grayscale", target_size=(48, 48))
show_img = load_img('input/Shawon.jpg', grayscale=False, target_size=(200, 200))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)

x /= 255

custom = model.predict(x)
emotion_analysis(custom[0])

x = np.array(x, 'float32')
x = x.reshape([48, 48])

plt.gray()
plt.imshow(show_img)
plt.show()

m = 0.000000000000000000001
a = custom[0]
for i in range(0, len(a)):
    if a[i] > m:
        m = a[i]
        ind = i

print('Expression Prediction:', objects[ind])

img = load_img('input/testimages/wallpaper2you_443897.jpg', grayscale=True, color_mode="grayscale", target_size=(48, 48))
show_img = load_img('input/testimages/wallpaper2you_443897.jpg', grayscale=False, target_size=(200, 200))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)

x /= 255

custom = model.predict(x)
# print(custom[0])
emotion_analysis(custom[0])

x = np.array(x, 'float32')
x = x.reshape([48, 48])

plt.gray()
plt.imshow(show_img)
plt.show()

m = 0.000000000000000000001
a = custom[0]
for i in range(0, len(a)):
    if a[i] > m:
        m = a[i]
        ind = i

print('Expression Prediction:', objects[ind])