from PIL import Image
import cv2
import time
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
                  


class SeagrassMonitor:
    def __init__(self):
        self.done = False
        self.seagrass_counter = 0
        self.growth = 0 
        self.frame = None
        self.prev_frame = None
        self.next_frame = None
        self.counter = 0
        
    def run(self, frame_under):
        self.frame = frame_under
        self.counter += 1
        if self.counter == 1:
            self.prev_frame = self.frame
        if self.counter == 2:
            self.next_frame = self.frame
            squares_before = self.detect_squares(self.prev_frame)
            squares_after = self.detect_squares(self.next_frame)
            self.growth = self.calculate_seagrass(squares_before, squares_after) 
            self.counter = 0

        return self.growth

    def detect_squares(self, frame):
        squares = 0
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0) 
        dilated = cv2.dilate(blur, None, iterations=3)
        _, thresh = cv2.threshold(dilated, 127, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # epsilon value can be tweaked
            epsilon = 0.03*cv2.arcLength(contour, True)
            # approx is the polygonal approximation of the contour
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(dilated, [approx], 0, (0), 3)
            
            if len(approx) == 4: # 4 sides means a square
                i, j = approx[0][0]
                # x,y top left corner. w,h width and height
                x, y, w, h = cv2.boundingRect(contour)
                ratio = float(w)/h
                # how long a square side needs to be in order to be counted, to remove noise
                noise_threshhold = 20
                # ratio between 0.9 and 1.1 means a square
                if  0.9 <= ratio <= 1.1 and w > noise_threshhold < h:
                    squares += 1
                    cv2.putText(dilated, 'Square', (i, j), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        #print(squares)
        #cv2.imshow("res", dilated)
        #cv2.waitKey(0)
        return squares
    
    def calculate_seagrass(self, squares_before, squares_after):
        percentage_difference = (squares_after / squares_before) * 100
        return percentage_difference
                

if __name__ == "__main__":
    grass1 = cv2.imread("monitor_seagrass\images\Example1.png")
    grass2 = cv2.imread("monitor_seagrass\images\Example2.png")
    seagrass_monitor = SeagrassMonitor()
    seagrass_monitor.update(grass1)
    seagrass_monitor.update(grass2)
    seagrass_monitor.update()
    print(seagrass_monitor.growth)
