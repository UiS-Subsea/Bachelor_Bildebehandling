import cv2
import numpy
import time
from find_center_of_red import find_center_of_red
from supporting_functions import *


def autonomous_docking(frame):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    center_of_frame = get_center_of_frame(frame)
    center_of_red, red_radius = find_center_of_red(frame)
    center_diff_width, center_diff_height = differance_between_centers(center_of_frame, center_of_red)
    center_area_differance = red_frame_area_percentage(red_radius, frame_width, frame_height)    

    if center_area_differance > 30:
        s = stop_rov()
        print(s)
        return

    else:
        r = regulate_position(center_diff_width, center_diff_height, red_radius)
        print(r)


def autonomous_docking_loop(video_stream):
    teller = 0
    while video_stream.isOpened():
        while True:
            ret, frame = video_stream.read()
            if ret:
                teller += 1
                print(teller)
                a = autonomous_docking(frame)
                if a == "STOP":
                    return




if __name__ == "__main__":
    #autonomous_docking("autonomous_docking/images/dockingstation_stop.png")
    video_stream = cv2.VideoCapture("autonomous_docking/videos/Autodock1.mp4")
    autonomous_docking_loop(video_stream)
