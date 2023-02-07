import cv2
import numpy
import time
from find_center_of_red import find_center_of_red
from supporting_functions import *


#TODO: INTEGRARTE VIDEOSTREAM HERE!!!
def autonomous_docking(image_path):
    frame = cv2.imread(image_path)
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    center_of_frame = get_center_of_frame(frame)
    center_of_red, red_radius = find_center_of_red(frame)
    center_diff_width, center_diff_height = differance_between_centers(center_of_frame, center_of_red)
    center_area_differance = red_frame_area_percentage(red_radius, frame_width, frame_height)    

    if center_area_differance > 30:
        stop_rov()

    else:
        regulate_position()
   

    print(center_of_frame)
    print(center_of_red, red_radius)
    print(center_diff_width, center_diff_height)
    print(center_area_differance)


if __name__ == "__main__":
    autonomous_docking("autonomous_docking/images/dockingstation_stop.png")