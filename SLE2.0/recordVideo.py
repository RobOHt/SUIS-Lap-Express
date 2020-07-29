from picamera import PiCamera
import time
import cv2
import numpy as np
import math
from scipy.stats import ttest_ind
from statistics import mean

WIDTH = 2 ** 6


def record_video():
    # counter = int(input("Please enter a random large number: "))
    counter = 0
    time_per_vid = 5
    time.sleep(5)
    print("Recording began!")

    while True:
        time_stamp = str(time.time())[-4:]
        try:
            os.mkdir("./output")
        except:
            pass

        camera.capture(f"./output/{counter}.jpg")
        print(f"photo {counter}.jpg saved!")
        counter = counter + 1


def determine_direction(img):
    direction = -10
    # ----------------------------------------------------------------------Get some sample from bottom left and bottom right
    sample_size = 10
    bottom_pixels = img[int(-2/sample_size*WIDTH):int(-1/sample_size*WIDTH)]
    sample_left, sample_right = [], []
    for row_array in bottom_pixels:
        row = [list(pixel) for pixel in row_array]
        sample_left = sample_left + row[:int(1/sample_size*WIDTH)]
        sample_right = sample_right + row[int(-1/sample_size*WIDTH):]
    #print(sample_left)
    #print(sample_right)
        
    # ----------------------------------------------------------------------Perform t-test for b, g, r pixels respectively,
    # ----------------------------------------------------------------------and produce a score
    bL, gL, rL = [pixel[0] for pixel in sample_left], [pixel[1] for pixel in sample_left], [pixel[2] for pixel in sample_left]
    bR, gR, rR = [pixel[0] for pixel in sample_right], [pixel[1] for pixel in sample_right], [pixel[2] for pixel in sample_right]
    _, bProb = ttest_ind(bL, bR)
    _, gProb = ttest_ind(gL, gR)
    _, rProb = ttest_ind(rL, rR)
    score = bProb*gProb*rProb
    
    # ----------------------------------------------------------------------Evaluate the score and steer left or right
    if score <= 1e-150:
        meanL = mean(bL + gL + rL)
        meanR = mean(bR + gR + rR)
        if meanL > meanR:  # Reaching right edge! Turn left
            direction = -1
        if meanL < meanR:  # Reaching left edge! Turn right
            direction = 1
    elif score > 1e-150:
        direction = 0
    else:
        direction = -10
    return direction


def get_frame(raw_image):
    processed_img = raw_image.reshape((WIDTH, WIDTH, 3))
    direction = determine_direction(processed_img)
    return processed_img, direction


if __name__ == "__main__":
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (WIDTH, WIDTH)
    camera.framerate = 24

    image = np.empty((WIDTH * WIDTH * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((WIDTH, WIDTH, 3))

    processed_image, direction = get_frame(image)
    print(direction)
    cv2.imshow("preview", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
