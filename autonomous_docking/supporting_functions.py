import math

#takes in a frame
#returns frame width and frame height as a tuple
def get_center_of_frame(frame):
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]
    return (frame_width // 2, frame_height // 2)


#takes in two center points as tuples (width, height)
#returns the differance as a one tuple (width, height)
#positive direction is upwards and rightwards
def differance_between_centers(frame_center, red_center):
    return ((frame_center[0] - red_center[0]) * (-1), frame_center[1] - red_center[1])


def red_frame_area_percentage(red_radius, frame_width, frame_height):
    frame_area = frame_width * frame_height
    red_area = math.pi * (red_radius ** 2)
    percent_diff = (red_area / frame_area) * 100
    return round(percent_diff, 3)


#takes in a displacement as a tuple (width, height) as x, y axis and size of red circle as radius
#returns regulation movement to move ROV back on course
#TODO: ADD LOGIC FOR REGULATION HERE
def regulate_position(displacement_x, displacement_y):
    drive_command = ""
    if displacement_x > 10:
        drive_command = "GO LEFT"
    
    elif displacement_x < -10:
        drive_command = "GO RIGHT"

    elif displacement_y > 10:
        drive_command = "GO DOWN"

    elif displacement_y < -10:
        drive_command = "GO UP"
    else:
        drive_command = "GO FORWARD"
        
    return drive_command


#function for stopping ROV
#returns stopping message
#TODO: ADD LOGIC FOR STOPPING THE ROV HERE!
def stop_rov():
    return "STOP"