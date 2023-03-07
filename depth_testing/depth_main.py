import cv2
import numpy
import math
import time
from find_center_red import find_center_of_red
from depth_find import find_depth



def find_depth_main(img_left, img_right):
    base = 6 #baseline: 10cm between the two cameras [cm]
    focal_length = 2.6 #camera lense focal lenght, dont know what this means [mm] 
    fov = 69 #Camera field of view in the horisontal plane [degrees]

    # red_center_left, radius_left = find_center_of_red(img_left, low_range=(47, 37, 65), high_range=(55, 47, 75))
    # red_center_right, radius_right = find_center_of_red(img_right, low_range=(60, 50, 80), high_range=(80, 60, 100))
    red_center_left, radius_left = find_center_of_red(img_left)
    red_center_right, radius_right = find_center_of_red(img_right)
    depth = find_depth(red_center_left, red_center_right, img_left, img_right, base, focal_length, fov)
    return depth





if __name__ == "__main__":
    img_left = cv2.imread('depth_testing/93cm_test1_1080.png')
    img_right  = cv2.imread('depth_testing/93cm_test2_1080.png')
    print(find_depth_main(img_left, img_right))




