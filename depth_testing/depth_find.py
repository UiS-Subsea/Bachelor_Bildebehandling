import cv2
import numpy as np
import time

def find_depth(center_left, center_right, frame_left, frame_right, baseline=6, focal=2.6, fov=70):
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_left == width_right:
        f_pixel = (width_right * 0.5) / np.tan(fov * 0.5 * np.pi/180)

    else:
        print("Left and right camera frames do not have same pixel width!") 

    x_right = center_right[0] #x_koordinate value
    x_left = center_left[0] #x_koordinate value
    y_right = center_left[1]
    y_left = center_left[1]

    disparity_x = x_left - x_right
    disparity_y = y_left - y_right
    total_disparity = np.sqrt((disparity_x ** 2) + (disparity_y ** 2)) #if the two cameras are not properly alligned, this handles that problem
    zDepth = (baseline * f_pixel) / total_disparity

    return abs(zDepth)
