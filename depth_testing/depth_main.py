import cv2
import numpy
import math
import time
from find_center_red import find_center_of_red
from depth_find import find_depth



def find_depth_main(img_left, img_right):
    base = 6 #baseline: 10cm between the two cameras [cm]
    focal_length = 2.6 #camera lense focal lenght, dont know what this means [mm] 
    fov = 70 #Camera field of view in the horisontal plane [degrees]

    red_center_left, radius_left = find_center_of_red(img_left, low_range=(0, 0, 100), high_range=(80, 80, 255))
    red_center_right, radius_right = find_center_of_red(img_right, low_range=(0, 0, 100), high_range=(80, 80, 255))
    # red_center_left, radius_left = find_center_of_red(img_left)
    # red_center_right, radius_right = find_center_of_red(img_right)
    avg_radius = (radius_left + radius_right) / 2 #avg px width of the radiuses
    depth = find_depth(red_center_left, red_center_right, img_left, img_right, base, focal_length, fov)
    return depth, avg_radius


def find_aread_of_circle(depth, radius):
    fov = 69
    frame_px_width = 1920 #CANNOT BE HARDCODED!!!
    view_width_cm = 2 * (math.tan(math.radians(fov / 2)) * depth)
    radius_width_ratio = radius / frame_px_width
    radius_in_cm = view_width_cm * radius_width_ratio
    area = math.pi * (radius_in_cm ** 2)

    return area



if __name__ == "__main__":
    img_left = cv2.imread('depth_testing/coral_top_left_view.jpg')
    img_right  = cv2.imread('depth_testing/coral_top_right_view.jpg')
    depth, avg_radius = find_depth_main(img_left, img_right)
    area = find_aread_of_circle(depth, avg_radius)
    print(f"Depth, Radius: {depth, avg_radius}")
    print(f"area in cm: {area}")
    




