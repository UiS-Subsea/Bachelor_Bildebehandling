import cv2
import numpy as np
import time

# What to tweak for water test:
# 1. cv2.inRange() lower and upper range
# 2. Range of acceptable angles
# 3. Range of acceptable ratios of displacement from center

class AutonomousTransect:
    def __init__(self):
        self.canStabilize = False
        self.driveCommand = "GO FORWARD"

    #takes in frame, finds all the contours of objects with dark blue color
    #returns angle between             
    
    def update(self, frame):
        self.autonomous_transect_maneuver(frame)
        self.doStabilize(frame)
        print("Ran")
        
    def get_angle_between_pipes(self, pipe1, pipe2):
        angle1 = pipe1[2]
        angle2 = pipe2[2]
        if angle1 > 45:
            angle1 -= 90
        if angle2 > 45:
            angle2 -= 90
        # avg angle = 0 means pipes are parallel, negative means pipes tilt to left, positive right
        avg_angle = (angle1 + angle2) / 2 #average angle of the pipes to find direction
        print("Average angle: ", avg_angle)
        return avg_angle


    #takes in a list of contours
    #filters the contours according to 
    def find_pipes(self, frame):
        contours = self.find_dark_blue_contours(frame)
        pipes = [] #pipe looks like -> ((x, y), (w, h), angle)
    
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            (x, y), (w, h), angle = rect
    
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            if w > 1 and h > 1:
                if (w / h < 0.25 or w / h > 2) and cv2.contourArea(contour) > 300 and (w > frame.shape[0] - 200 or h > frame.shape[0] - 200 or w > frame.shape[1] - 200 or h > frame.shape[1] - 200):
                    straightRect = cv2.boundingRect(contour)
                    x, y, w, h = straightRect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 100, 0), 2)
                    cv2.drawContours(frame, [box], 0, (0, 0, 255), 3)    
                    print((x, y), (w, h), angle)
    
                    pipes.append(rect)

        cv2.imshow("filtered", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            
            
        if len(pipes) == 2:
            return pipes
            
        else:
            print("No pipes found")
            return "SKIP" # Skip frame, innocuous result TODO 
      
        
    def find_dark_blue_contours(self, frame):
        low_blue_range = (50, 0, 0) #b, g, r
        high_blue_range = (255, 60, 60)
    
        transect_pipe_mask = cv2.inRange(frame, low_blue_range, high_blue_range)
        pipe_contours, _ = cv2.findContours(transect_pipe_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.drawContours(frame, pipe_contours, -1, (0, 255, 0), 5)
        # cv2.imshow("contours", frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return pipe_contours
    
    
    def autonomous_transect_maneuver(self, frame):
        pipes = self.find_pipes(frame)
        if pipes == "SKIP":
            return "SKIP"
        
        transect_angle = self.get_angle_between_pipes(pipes[0], pipes[1])
        
        if transect_angle < -5:
            print("Turn left")
            # TODO run some function to turn left and stabilize
    
        elif transect_angle > 5:
            print("Turn right")
            
            # TODO run some function to turn right and stabilize
        else:
            print("Go forward")
            self.canStabilize = True
            return "GO FORWARD"
    
        #call go center function
        

    def doStabilize(self, frame):
        if self.canStabilize:
            pipes = self.find_pipes(frame)
            if pipes == "SKIP":
                print("SKIPPING FRAME")
                return
            
            # Find leftmost pipe:
            if pipes[0][0] < pipes[1][0]:
                leftPipe = pipes[0]
                rightPipe = pipes[1]
            else:
                leftPipe = pipes[1]
                rightPipe = pipes[0]
            distanceFromLeftPipe = leftPipe[0][0]
            distanceFromRightPipe = frame.shape[1] - rightPipe[0][0]
            ratio = distanceFromLeftPipe / distanceFromRightPipe # ratio = 1 means perfect
            
            print("Distance from left pipe: ", distanceFromLeftPipe)
            print("Distance from right pipe: ", distanceFromRightPipe)
            print("Ratio: ", ratio)
            
            if 0.95 > ratio:
                print("Move to left")
                
            elif 1.05 < ratio:
                print("Move to right")
                
            else:
                print("Go forward")
        else:
            print("Can't stabilize yet")
         



# TODO implement into Camerafeed_MP_Main.py
def run_autonomous_transect(frame):
    autonomous_transect_instance = AutonomousTransect(frame)
    
    while True:
        autonomous_transect_instance.autonomous_transect_maneuver(frame)
        autonomous_transect_instance.doStabilize(frame)
        print("Ran")

    
if __name__ == "__main__":
    frame = cv2.imread("autonomus_handling/autonomous_transect/transect2.png")
    start = run_autonomous_transect(frame)
    