import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
import numpy as np

np.random.seed(1000)


def alexnet(width, height):
    # Instantiate an empty model
    model = Sequential()

    # 1st Convolution Layer
    model.add(Conv2D(filters=96, input_shape=(width, height, 1), kernel_size=(5, 5), strides=(2, 2), padding="valid"))
    model.add(Activation("relu"))
    # Max Pooling
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid"))

    # 2nd Convolution Layer
    model.add(Conv2D(filters=256, kernel_size=(3, 3), strides=(1, 1), padding="valid"))
    model.add(Activation("relu"))
    # Max Pooling
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding="valid"))

    # 3rd Convolution Layer
    model.add(Conv2D(filters=384, kernel_size=(3, 3), strides=(1, 1), padding="valid"))
    model.add(Activation("relu"))

    # 4th Convolution Layer
    model.add(Conv2D(filters=384, kernel_size=(3, 3), strides=(1, 1), padding="valid"))
    model.add(Activation("relu"))

    # 5th Convolution Layer
    model.add(Conv2D(filters=256, kernel_size=(2, 2), strides=(1, 1), padding="valid"))
    model.add(Activation("relu"))
    # Max Pooling
    model.add(MaxPooling2D(pool_size=(1, 1), strides=(1, 1), padding="valid"))

    # Passing it to a Fully Connected layer
    model.add(Flatten())
    # 1st Fully Connected Layer
    model.add(Dense(4096, input_shape=(width * height * 1,)))
    model.add(Activation("relu"))
    # Add Dropout to prevent overfitting
    model.add(Dropout(0.4))

    # 2nd Fully Connected Layer
    model.add(Dense(4096))
    model.add(Activation("relu"))
    # Add Dropout
    model.add(Dropout(0.4))

    # 3rd Fully Connected Layer
    model.add(Dense(1000))
    model.add(Activation("relu"))
    # Add Dropout
    model.add(Dropout(0.4))

    # Output Layer
    model.add(Dense(1))

    model.summary()

    # Compile the model
    model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])

    return model
