import cv2
import numpy
import math
import time
from find_center_red import find_center_of_red
from depth_find import find_depth

base = 9 #baseline: 10cm between the two cameras [cm]
focal_length = 6 #camera lense focal lenght, dont know what this means [cm]
fov = 56.6 #Camera field of view in the horisontal plane [degrees]

img_left = cv2.imread('depth_testing/3dmodel_img1.png')
red_center_left, radius_left = find_center_of_red(img_left)

img_right = cv2.imread('depth_testing/3dmodel_img2.png')
red_center_right, radius_right = find_center_of_red(img_right)

depth = find_depth(red_center_left, red_center_right, img_left, img_right, base, focal_length, fov)

print(depth)




