from AALoad_Model import predict_model
import os
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
while True:
    igray = cv2.imread("output/4633.png")
    igray = cv2.cvtColor(igray, cv2.COLOR_RGB2GRAY)
    print(igray.shape)
    predict_model(igray, "SIZE80_40EPOCHS7")
