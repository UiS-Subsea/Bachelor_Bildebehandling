import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
from find_center_red import find_center_of_red
from depth_find import find_depth



def find_depth_grid(img_left, img_right):
    base = 6 #baseline: 10cm between the two cameras [cm]
    focal_length = 2.6 #camera lense focal lenght, dont know what this means [mm] 
    fov = 70 #Camera field of view in the horisontal plane [degrees]

    height_right, width_right, depth_right = img_right.shape
    height_left, width_left, depth_left = img_left.shape

    x_points = []
    y_points = []
    for x in range(0, width_right, width_right // 11):
        x_points.append(x)

    for y in range(0, height_left, height_left // 11):
        y_points.append(y)

    x = np.linspace(-2, 2, 5)
    y = np.linspace(-2, 2, 5)
    X, Y = np.meshgrid(x, y)

    z = []
    Z = []

    for x in x_points:
        for y in y_points:
            d = find_depth(x, y)
            z.append(d)
        
        Z.append(z)
        z = []


    Z = np.matrix(Z)
    print(Z)
            


    print(x_points)
    print(y_points)

    
    
    print(f"width right, height right: {width_right, height_right}")
    print(f"width left, height left: {width_left, height_left}")





if __name__ == "__main__":
    img_left = cv2.imread('depth_testing/coral_top_left_view.jpg')
    img_right  = cv2.imread('depth_testing/coral_top_right_view.jpg')
    f = find_depth_grid(img_left, img_right)
