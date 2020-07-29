import tensorflow as tf
import os
import cv2
import numpy as np

# physical_devices = tf.config.list_physical_devices('GPU')
# print(physical_devices)
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

WIDTH = 80
HEIGHT = 40


def predict_model(raw_input, model_name):
    global WIDTH, HEIGHT

    image = raw_input
    image = image.reshape((-1, WIDTH, HEIGHT, 1))
    model = tf.keras.models.load_model(model_name)
    result = model.predict(image)[0]
    print(result)

    return None


# predict_model(cv2.imread("output/16481.png"), "MODELalexnetv2EPOCHS7")
