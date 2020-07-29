from picamera import PiCamera
import time
import os
import cv2
import numpy as np
from collections import Counter
from sklearn.cluster import DBSCAN
from sklearn.linear_model import LinearRegression
import math
from math import pi, atan

WIDTH = 2 ** 10


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


def draw_lines(img, lines):
    coordinates = []
    for line in lines:
        coords = line[0]
        x1, y1 = coords[0], coords[1]
        x2, y2 = coords[0 + 2], coords[1 + 2]
        #cv2.line(img, (x1, y1), (x2, y2), [255, 255, 255], 3)
        gradient = (y2 - y1) / (x2 - x1 + 0.0000001)
        c = y1 - x1 * gradient

        # Create 5 points in between the two coordinates, if the line's gradient is great enough
        if abs(gradient) >= 0.5:
            y_interval = abs(y2 - y1) / 100
            for i in range(100 + 1):
                current_y = min([y1, y2]) + y_interval * i
                current_x = (current_y-c)/gradient
                if current_x <= WIDTH and current_y <= WIDTH: 
                    coordinates.append([current_x, current_y])
                    cv2.circle(img, (int(current_x), int(current_y)), 2, [255, 255, 255], 2)

    # The all the coordinates with a DBSCAN clustering algorithm
    try:
        clustering = DBSCAN(eps=400, min_samples=30).fit(np.array(coordinates))
    except ValueError:
        print("No lanes found")
    cluster_labels = clustering.labels_
    label_brief = [label for label in Counter(cluster_labels)]

    # Sort coordinates into individual clusters
    cluster_coor = [[] for i in range(len(label_brief))]
    for index, coor in enumerate(coordinates):
        label = cluster_labels[index]
        cluster_coor[label].append(coor)

    # Fit every cluster with a linear regression algorithm and hence get one major line for each cluster
    major_lines = []
    for coor_group in cluster_coor:
        X = np.array([coor[0] for coor in coor_group])
        y = np.array([coor[1] for coor in coor_group])

        reg = LinearRegression().fit(X.reshape(-1, 1), y)
        Xmax, Xmin = int(max(X)), int(min(X))
        ymax, ymin = int(reg.predict(np.array([[Xmax]]))), int(reg.predict(np.array([[Xmin]])))
        score = len(coor_group) * 0.3 + math.sqrt((ymax - ymin) ** 2 + (Xmax - Xmin) ** 2) * 0.7
        major_lines.append([[Xmax, ymax], [Xmin, ymin], score])  # major_lines: [coor1, coor2, score]
        cv2.line(img, (Xmax, ymax), (Xmin, ymin), [255, 255, 255], 5)

    # Sort major_lines by the amount of coordinates represented by this line
    major_lines = sorted(major_lines, key=lambda major_lines: major_lines[2])
    for i in range(2 if len(major_lines) > 2 else len(major_lines)):  # Only loop through the first two detected lines
        line = major_lines[i]
        max_coor = tuple(line[0])
        min_coor = tuple(line[1])
        cv2.line(img, max_coor, min_coor, [255, 255, 255], 30)

    # return the two most dominant lines
    return major_lines[:2]


def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked


def determine_direction(lanes):  # lanes: [[coor1, coor2, score], [coor1, coor2, score]]
    all_lines = [line[:2] for line in lanes]  # all_lines: [[coor1, coor2], [coor1, coor2]]
    direction = -10
    # Get the left most line if there are two lines:
    if len(all_lines) == 2:
        line = sorted(all_lines, key=lambda line: line[0][0]+line[1][0])[0]  # line: [[x1, y1], [x2, y2]]
    elif len(all_lines) == 1:
        line = all_lines[0]
    else:
        line = None
        print("No lane detected!")

    # -------------------------------------------------priority 1: make sure that line is aligned
    bottom_coor = sorted(line, key=lambda coor: coor[1])[-1]  # bottom_coor: [x2, y2]
    top_coor = sorted(line, key=lambda coor: coor[1])[0]  # bottom_coor: [x1, y1]
    bttmX, bttmY = bottom_coor[0], bottom_coor[1]
    tpX, tpY = top_coor[0], top_coor[1]
    if bttmX > WIDTH/2+WIDTH/9:  # Line is right of vehicle
        direction = 1
    elif bttmX < WIDTH/2-WIDTH/9:  # Line is left of vehicle
        direction = -1
    elif WIDTH/2-WIDTH/9 <= bttmX <= WIDTH/2+WIDTH/9:  # Vehicle is on track
        direction = 0

    return direction


def get_frame(raw_image):
    image = raw_image.reshape((WIDTH, WIDTH, 3))
    processed_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Start processing image
    vertices = np.array([[0, WIDTH], [0, (1 / 4) * WIDTH], [WIDTH, (1 / 4) * WIDTH], [WIDTH, WIDTH],
                         ], np.int32)
    processed_img = cv2.Canny(processed_img, threshold1=70, threshold2=70)
    processed_img = cv2.GaussianBlur(processed_img, (7, 7), 0)
    # processed_img = roi(processed_img, [vertices])
    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180, 180, np.array([]), 0,
                            100)  # Last two values are: min length, max gap
    result_lines = draw_lines(processed_img, lines)
    direction = determine_direction(result_lines)
    return processed_img, direction


if __name__ == "__main__":
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (WIDTH, WIDTH)
    camera.framerate = 24

    image = np.empty((WIDTH * WIDTH * 3,), dtype=np.uint8)
    camera.capture(image, 'rgb')
    image = image.reshape((WIDTH, WIDTH, 3))

    processed_image, direction = get_frame(image)
    print(direction)
    cv2.imshow("preview", processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
