import cv2
import numpy
import math
import time
from find_center_red import find_center_of_red
from depth_find import find_depth



def find_depth_main(image1, image2):
    base = 6 #baseline: 10cm between the two cameras [cm]
    focal_length = 0.26 #camera lense focal lenght, dont know what this means [cm]
    fov = 73 #Camera field of view in the horisontal plane [degrees]
    red_center_left, radius_left = find_center_of_red(img_left)
    red_center_right, radius_right = find_center_of_red(img_right)
    depth = find_depth(red_center_left, red_center_right, img_left, img_right, base, focal_length, fov)
    return depth



if __name__ == "__main__":
    img_left = cv2.imread('depth_testing/3dmodel_img1.png')
    img_right  = cv2.imread('depth_testing/3dmodel_img2.png')
    print(find_depth_main(img_left, img_right))




