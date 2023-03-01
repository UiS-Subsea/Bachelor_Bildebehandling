import cv2
import numpy as np
import time

def find_depth(center_left, center_right, frame_left, frame_right, baseline, focal, fov):
    height_right, width_right, depth_right = frame_right.shape
    height_left, width_left, depth_left = frame_left.shape

    if width_left == width_right:
        f_pixel = (width_right * 0.5) / np.tan(fov * 0.5 * np.pi/180)

    else:
        print("Left and right camera frames do not have same pixel width!")

    x_right = center_right[0] #x_koordinate value
    x_left = center_left[0] #x_koordinate value

    disparity = x_left - x_right
    zDepth = (baseline * f_pixel) / disparity

    return abs(zDepth)
