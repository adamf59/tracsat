# Import native modules
import numpy as np
import cv2
import sys
import os

# Import custom modules
from easygopigo3 import EasyGoPiGo3

# Import custom modules
sys.path.append(os.path.join('../comp_vision/helper'))
from ThreadWorker import *


class Camera:
    # Contructor
    def __init__(self, id):
        self._id = id
        self._cap = None
        self._obstacle_distance = None
        self._circle_center = None

    # Start camera
    def start_camera(self):
        self._cap = cv2.VideoCapture(0)
        self._cap.release()
        self._cap = cv2.VideoCapture(0)
    
    # Stop camera
    def stop_camera(self):
        self._cap.release()

    # Read and write images
    def read_and_write(self):
        ret, frame = self._cap.read()
        cv2.imwrite('frame.jpg', frame)
        image = cv2.imread('frame.jpg')
        return image

    # Circle detection and distance reading
    @staticmethod
    def circle_detect(image):
        # load the image, clone it for output, and then convert it to grayscale
        output = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect circles in the image
        circles_thread = Threader(cv2.HoughCircles)
        circles_thread.start((gray,cv2.HOUGH_GRADIENT, 1.0, 100,))
        circles = circles_thread.get_results()
        #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 400)
        circle_detected = False
        
        # Initialize variables
        dist_act = None

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                # only draw circle if it is small enough to be considered an actual object

                if (r < 200 and r > 0):
                    eta = 11.875/54;                # actual_distance/r_assoc (use one test case to calibrate correction factor)
                    offset = r * eta - 11.875;      # offset for moving object closer or greater
                    dist_act = 11.875 - offset      # subtract offset to reference distance

                    # Draw circle
                    cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                    cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    circle_detected = True

            # show the output image
            return [output, circle_detected, [x,y], dist_act]
        else:
            return [image, False, None, None]

    @staticmethod
    def show_image(image):
        cv2.imshow('img', image)

