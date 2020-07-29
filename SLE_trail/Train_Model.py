from Alexnet import alexnet
from tensorflow.keras.callbacks import TensorBoard
import tensorflow as tf
import numpy as np
from random import shuffle
from collections import Counter

physical_devices = tf.config.list_physical_devices('GPU')
print(physical_devices)
tf.config.experimental.set_memory_growth(physical_devices[0], True)

WIDTH = 98
HEIGHT = 98
EPOCHS = 8  # Standard: 8
MODEL_NAME = f"SIZE{WIDTH}_{HEIGHT}EPOCHS{EPOCHS}"
model = alexnet(WIDTH, HEIGHT)
tensorboard = TensorBoard(log_dir='logs/{name}'.format(name=MODEL_NAME))

train = np.load('training_data-SIZE100005-TIME63899.npy', allow_pickle=True)
print(Counter([i[1] for i in train]))

# -------------------------------------------------------------------------------------------------Balance training data
steer_list = [direction for direction in Counter([i[1] for i in train])]  # get a list of all the steering angles
train_balanced = []
class_cash = []
print("balancing data...")
for direction in steer_list:
    class_cash = []
    for xy in train:
        img = xy[0]
        steer = xy[1]
        if steer == direction:
            class_cash.append(xy)
    train_balanced = train_balanced + class_cash[:7500]
shuffle(train_balanced)
print(Counter([i[1] for i in train_balanced]))
train = train_balanced
# --------------------------------------------------------------------------------Get data into x and y
# X
X = np.array([i[0] for i in train]).reshape((-1, WIDTH, HEIGHT, 1))
# Y
Y_list = [int(i[1]) for i in train]
Y = np.array(Y_list).reshape(-1)

# -------------------------------------------------------------------------------Train model
model.fit(X, Y, epochs=EPOCHS, validation_split=0.3, batch_size=128, callbacks=[tensorboard])
model.save(MODEL_NAME)
