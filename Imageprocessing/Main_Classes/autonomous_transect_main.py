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
        self.driving_data = [0, 0, 0, 0, 0, 0, 0, 0]
        self.frame = None

    #takes in frame, finds all the contours of objects with dark blue color
    #returns angle between             
    def run(self, frame):
        self.frame = frame
        self.update()
        data = self.get_driving_data()
        return self.frame, data
        
    def update(self):
        self.stabilize_angle()
        self.stabilize_alignment()
        
    def get_driving_data(self):
        data = self.driving_data.copy()
        self.driving_data = [0, 0, 0, 0, 0, 0, 0, 0]
        return data

    def get_angle_between_pipes(self, pipe1, pipe2):
        angle1 = pipe1[2]
        angle2 = pipe2[2]
        if angle1 > 45:
            angle1 -= 90
        if angle2 > 45:
            angle2 -= 90
        # avg angle = 0 means pipes are parallel, negative means pipes tilt to left, positive right
        avg_angle = (angle1 + angle2) / 2 #average angle of the pipes to find direction
        # print("Average angle: ", avg_angle)
        return avg_angle


    #takes in a list of contours
    #filters the contours according to 
    def find_pipes(self):
        contours = self.find_dark_blue_contours()
        pipes = [] #pipe looks like -> ((x, y), (w, h), angle)
    
        for contour in contours:
            rect = cv2.minAreaRect(contour)
            (x, y), (w, h), angle = rect
    
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            if w > 1 and h > 1:
                if (w / h < 0.25 or w / h > 2) and cv2.contourArea(contour) > 300 and (w > self.frame.shape[0] - 200 or h > self.frame.shape[0] - 200 or w > self.frame.shape[1] - 200 or h > self.frame.shape[1] - 200):
                    straightRect = cv2.boundingRect(contour)
                    x, y, w, h = straightRect
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 100, 0), 2)
                    cv2.drawContours(self.frame, [box], 0, (0, 0, 255), 3)    
                    # print((x, y), (w, h), angle)
    
                    pipes.append(rect)
        if len(pipes) == 2:
            return pipes
            
        else:
            # print("No pipes found")
            return "SKIP"
      
        
    def find_dark_blue_contours(self):
        low_blue_range = (0, 0, 0) #b, g, r, TODO should mabye be (70, 0, 0)
        high_blue_range = (255, 60, 60)
    
        transect_pipe_mask = cv2.inRange(self.frame, low_blue_range, high_blue_range)
        pipe_contours, _ = cv2.findContours(transect_pipe_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # cv2.drawContours(frame, pipe_contours, -1, (0, 255, 0), 5)
        # cv2.imshow("contours", frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return pipe_contours
    
    # driving packet: [id, [x, y, z, r, 0, 0, 0, 0]]
    
    def stabilize_angle(self):
        pipes = self.find_pipes()
        if pipes == "SKIP":
            return
            
        
        transect_angle = self.get_angle_between_pipes(pipes[0], pipes[1])
        
        if transect_angle < -2:
            # print("Turn left")
            self.driving_data = [0, 0, 0, -10, 0, 0, 0, 0]
    
        elif transect_angle > 2:
            self.driving_data = [0, 0, 0, 10, 0, 0, 0, 0]
            # print("Turn right")
            
        else:
            # print("Clear for stabilization")
            self.canStabilize = True
        

    def stabilize_alignment(self):
        if self.canStabilize:
            pipes = self.find_pipes()
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
            distanceFromRightPipe = self.frame.shape[1] - rightPipe[0][0]
            ratio = distanceFromLeftPipe / distanceFromRightPipe # ratio = 1 means perfect
            
            # print("Distance from left pipe: ", distanceFromLeftPipe)
            # print("Distance from right pipe: ", distanceFromRightPipe)
            # print("Ratio: ", ratio)
            
            if 0.95 > ratio:
                self.driving_data = [-10, 0, 0, 0, 0, 0, 0, 0]
                # print("Move to left")
                
            elif 1.05 < ratio:
                # print("Move to right")
                self.driving_data = [10, 0, 0, 0, 0, 0, 0, 0]
                
            else:
                # print("Go forward")
                self.driving_data = [0, 10, 0, 0, 0, 0, 0, 0]

            self.canStabilize = False
            return
            
        else:
            # print("Waiting for ROV to stabilize angle")
            return
        


class Frog:
    def __init__(self, rectangle):
        self.detectionCounter = 1
        self.rectangle = rectangle
        

class FrogCount:
    def __init__(self):
        self.currFrogs = [] # List of currently detected Frog objects
        self.prevFrogs = [] # List of detected Frog objects in previous frame
        self.frog_counter = 0
        self.detection_counter_threshold = 5
        self.frame = None
        self.fgbg = cv2.createBackgroundSubtractorKNN()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        
        self.check_previous_algo = "ADVANCED"

    # Starts the frog counting process
    def update(self, image, drawImage = False):
        self.frame = image
        
        # Calling the frog detection functions
        rectanglesNoRed = self.frogDetectionNoRed(image)
        rectanglesNoGrout = self.frogDetectionNoGrout(image)
        allRectangles = rectanglesNoRed + rectanglesNoGrout
        filteredRectangles = self.rectangleOverlapFilter(allRectangles)
        
        if drawImage:
            for rect in filteredRectangles:
                x,y,w,h = rect
                cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Image", image)

        # Converts the rectangles into Frog objects, used for Advanced frog counting algorithm
        frogRectangles = []
        for rectangle in filteredRectangles:
            frogRectangles.append(Frog(rectangle))
        
        self.currFrogs = frogRectangles
        
        if self.check_previous_algo == "BASIC":
            self.checkPreviousFrogsBasic()
            
        if self.check_previous_algo == "ADVANCED":
            self.checkPreviousFrogsAdvanced()

        return self.frog_counter
    
    # Basic algorithm for checking if a frog has been detected in last frame. Only works if detection is extremely accurate, ie. no noise and frogs always detected. Not used in final version
    def checkPreviousFrogsBasic(self): 
        numFrogsDetected = len(self.currFrogs)
        allFrogs = self.prevFrogs + self.currFrogs
        numAllFrogs = len(allFrogs)
        FilteredFrogs = self.rectangleOverlapFilter(allFrogs)
        numRemovedFrogs = numAllFrogs - len(FilteredFrogs)
        self.frog_counter += numFrogsDetected - numRemovedFrogs
        self.prevFrogs = self.currFrogs

    # Advanced algorithm for checking if a frog has been detected in last frame. Less susceptible to noise and missed detections
    def checkPreviousFrogsAdvanced(self):
        allFrogs = self.currFrogs + self.prevFrogs
        theRectangles = []
        for frog in allFrogs:
            theRectangles.append(frog.rectangle)
        OverlapPairs = self.rectangleOverlapFilterNoRemove(theRectangles.copy())
        for OverlapPair in OverlapPairs:
            # OverlapPair = touple of two indexes, of rectangles that overlap
            if allFrogs[OverlapPair[0]].detectionCounter <= allFrogs[OverlapPair[1]].detectionCounter:
                
                allFrogs[OverlapPair[0]].detectionCounter = allFrogs[OverlapPair[1]].detectionCounter + 1
        
        self.prevFrogs = self.currFrogs
        for frog in self.prevFrogs:
            if frog.detectionCounter == self.detection_counter_threshold:
                self.frog_counter += 1
        self.currFrogs = []
        
    def frogDetectionNoRed(self, image): # Does not detect red frogs
        # Threshold for red color of the image. Goal is for thresh1 to detect the grouts, and thresh2 to detect the grouts and frogs
        # the difference would then be only the frogs
        thresh1 = cv2.threshold(image[:,:,0], 70, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        thresh2 = cv2.threshold(image[:,:,0], 200, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        difference = cv2.subtract(thresh2, thresh1)
        
        # Blur to remove noise
        blur_difference = cv2.GaussianBlur(difference, (41, 41), 0)
        new_thresh = cv2.threshold(blur_difference, 0, 255, cv2.THRESH_OTSU)[1]
        
        contours, _ = cv2.findContours(new_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        frogRectangles = self.contourFiltration(contours)
        return frogRectangles
    
    def frogDetectionNoGrout(self, image): # Does not detect frogs in dark tile grouts or frogs which match the pool floor color
        # Same process as frogDetectionNoRed, but with different thresholds and now using grayscale image instead of red channel
        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
        gray = cv2.cvtColor(hls, cv2.COLOR_RGB2GRAY)
        thresh1 = cv2.threshold(gray, 90, 255, cv2.THRESH_OTSU)[1]
        thresh2 = cv2.threshold(gray, 120, 255, cv2.THRESH_TRIANGLE)[1]
        difference = cv2.subtract(thresh1, thresh2)
        diff_blur = cv2.GaussianBlur(difference, (71, 71), 0)
        dilate_blur = cv2.dilate(diff_blur, None, iterations=6)
        newThreshold = cv2.threshold(dilate_blur, 0, 255, cv2.THRESH_OTSU)[1]
        
        contours, _ = cv2.findContours(newThreshold.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        frogRectangles = self.contourFiltration(contours)
        return frogRectangles

    
    def contourFiltration(self, contours, epsilonValue = 0.03, noise_threshhold_lower = 40, noise_threshhold_upper = 300): # Finds frogs using various filters
        frog_rectangles = []
        for contour in contours:
            # epsilon value can be tweaked, higher value allows for larger approximated polygon, more likely to have less sides
            epsilon = epsilonValue * cv2.arcLength(contour, True)
            # approx is the polygonal approximation of the contour
            approx = cv2.approxPolyDP(contour, epsilon, True)
            # rect = cv2.minAreaRect(contour)
            # box = cv2.boxPoints(rect) # Rectangle, not rotated
            # box = np.int0(box)
            if 10 > len(approx) > 4: # More than 4 sides means its more round than a square, more sides means more circular
                # w,h width and height
                x, y, w, h = cv2.boundingRect(approx) # Rectangle, rotated
                if 0.7 < w/h < 1.3: # If the width and height are within 20% of each other, it is a square
                    # Noise threshhold to ignore small and large contours, can be tweaked
                    if  w > noise_threshhold_lower < h and w < noise_threshhold_upper > h:
                        frog_rectangles.append((x,y,w,h))
                        cv2.rectangle(self.frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        return frog_rectangles
    
    def rectangleOverlapFilter(self, rectangles): # Filters out rectangles that overlap O(n^2)
        if len(rectangles) >= 2:
            n = 0
            for rectangle in rectangles:
                n += 1
                for index in range(n, len(rectangles)):
                    x,y,w,h = rectangle
                    x2,y2,w2,h2 = rectangles[index]
                    
                    # Checks if rectangles overlap in x and y axis
                    # From https://www.geeksforgeeks.org/find-two-rectangles-overlap/
                    if x + w < x2 or x2 + w2 < x:
                        continue
                    
                    elif y + h < y2 or y2 + h2 < y:
                        continue
                    
                    else:
                        rectangles.pop(index)
                        break
                    
        return rectangles
    
    def rectangleOverlapFilterNoRemove(self, rectangles): # Finds rectangles that overlap, but does not remove them. Returns a list of pairs of overlapping rectangles
        overlappedRectsPairs = []
        if len(rectangles) >= 2:
            n = 0
            for rectangle in rectangles:
                n += 1
                for index in range(n, len(rectangles)):
                    x,y,w,h = rectangle
                    x2,y2,w2,h2 = rectangles[index]
                    
                    # Checks if rectangles overlap in x and y axis
                    # From https://www.geeksforgeeks.org/find-two-rectangles-overlap/
                    if x + w < x2 or x2 + w2 < x:
                        continue
                    
                    elif y + h < y2 or y2 + h2 < y:
                        continue
                    
                    else:
                        overlappedRectsPairs.append((n, index))
                        break
                    
        return overlappedRectsPairs


    
if __name__ == "__main__":
    frame = cv2.imread("camerafeed/Other_Classes/images/transect1.png")
    transect = AutonomousTransect()
    transect.run(frame)
