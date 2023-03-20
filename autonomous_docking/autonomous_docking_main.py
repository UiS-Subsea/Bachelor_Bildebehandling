import cv2
import numpy
import time
from find_center_of_red import find_center_of_red
from supporting_functions import *
from find_relative_angle import *



class AutonomousDocking:
    def __init__(self, video_stream):
        self.video_stream = video_stream

    #takes in a frame
    #regulates position or stops based on the computer vision
    def autonomous_docking(self, frame):
        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        center_of_frame = get_center_of_frame(frame)
        center_of_red, red_radius = find_center_of_red(frame)
        if center_of_red == (0, 0) and red_radius == 0: #center = (0, 0) and r = 0 are default values, meaning no red conture is found
            print("No docking station found!")
            return "No docking station found!"

        center_diff_width, center_diff_height = differance_between_centers(center_of_frame, center_of_red)
        print(center_diff_width, center_diff_height)
        center_area_differance = red_frame_area_percentage(red_radius, frame_width, frame_height)    

        #checks whether or not it should stop
        if center_area_differance > 30:
            s = stop_rov()
            print(s)
            return s #STOP
        #regulates position of ROV
        else:
            docking_command = regulate_position(center_diff_width, center_diff_height)
            print(docking_command)
            return docking_command
        

    def rotation_commands(self, down_frame):
        angle = find_relative_angle(down_frame)
        if angle == "SKIP":
            return "SKIP", angle
        if angle < -2:
            # angle = 90 + angle
            return "ROTATE LEFT", angle
        
        elif angle > 2:
            # angle = 90 - angle
            return "ROTATE RIGHT", angle
        
        else:
            return "GO FORWARD", angle


    def update(self, frame):
        rotation = self.rotation_commands(frame)
        if rotation == "GO FORWARD":
            docking_command = self.autonomous_docking(frame)
            return docking_command

        elif rotation != "SKIP":
            return rotation
        else:
            return "SKIP"


    #ONLY FOR TESTING
    #takes in videostream
    def autonomous_docking_loop(self):
        teller = 0
        #while video_stream.isOpened():
        while True:
            ret, frame = self.video_stream.read()
            if ret:
                teller += 1
                print(teller)
                update = self.update(frame)
                print(update)
                if update == "STOP":
                    return



if __name__ == "__main__":
    #autonomous_docking("autonomous_docking/images/dockingstation_stop.png")
    video_stream = cv2.VideoCapture("autonomous_docking/videos/Pool_test.mp4")
    autonomous = AutonomousDocking(video_stream)
    autonomous.autonomous_docking_loop()