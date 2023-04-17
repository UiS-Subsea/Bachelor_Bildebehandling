import cv2
from other_funcs import *
from trackers import EuclideanDistTracker
import time

class Frog:
    def __init__(self, rectangle):
        self.detectionCounter = 1
        self.rectangle = rectangle
        

class FrogCount:
    def __init__(self):
        self.previous_frogs = [] #List of rectangles
        self.current_frogs = [] #List of rectangles
        self.currFrogs = []
        self.prevFrogs = []
        self.frog_counter = 0
        self.detection_counter_threshold = 10
        self.frame = None
        self.fgbg = cv2.createBackgroundSubtractorKNN()
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        
        self.check_previous_algo = "BASIC"

    #takes in frame  
    def update(self, image, drawImage = False): # Launches the two detection methods
        new = self.frogdetectionNew(image)
        self.frame = image
        rectanglesNoRed = self.frogDetectionNoRed(image)
        rectanglesNoGrout = self.frogDetectionNoGrout(image)
        
        allRectangles = rectanglesNoRed + rectanglesNoGrout
        filteredRectangles, _ = self.rectangleOverlapFilter(allRectangles)
        if drawImage:
            for rect in filteredRectangles:
                x,y,w,h = rect
                cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Image", image)

            
        
        for rectangle in filteredRectangles:
            self.currFrogs.append(Frog(rectangle))
            
        self.current_frogs = filteredRectangles
        
        if self.check_previous_algo == "BASIC":
            self.checkPreviousFrogsBasic()
            
        if self.check_previous_algo == "ADVANCED":
            self.checkPreviousFrogsAdvanced()

        return self.frog_counter
    
    def checkPreviousFrogsBasic(self):
        numFrogsDetected = len(self.current_frogs)
        allFrogs = self.previous_frogs + self.current_frogs
        numAllFrogs = len(allFrogs)
        FilteredFrogs, _ = self.rectangleOverlapFilter(allFrogs)
        numRemovedFrogs = numAllFrogs - len(FilteredFrogs)
        self.frog_counter += numFrogsDetected - numRemovedFrogs

        self.previous_frogs = self.current_frogs

    def checkPreviousFrogsAdvanced(self):
        allFrogs = self.current_frogs + self.previous_frogs
        _, OverlapPairs = self.rectangleOverlapFilter(allFrogs.copy())
        for OverlapPair in OverlapPairs:
            # OverlapPair = touple of two indexes, of rectangles that overlap
            if allFrogs[OverlapPair[0]].detectionCounter <= allFrogs[OverlapPair[1]].detectionCounter:
                allFrogs[OverlapPair[0]].detectionCounter = allFrogs[OverlapPair[1]].detectionCounter + 1

        
        self.prevFrogs = self.allFrogs[0:len(self.currFrogs)]
        for frog in self.prevFrogs:
            if frog.detectionCounter == self.detection_counter_threshold:
                self.frog_counter += 1
        self.currFrogs = []
        
    def frogDetectionNoRed(self, image):
        thresh = cv2.threshold(image[:,:,0], 70, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        thresh2 = cv2.threshold(image[:,:,0], 200, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        difference = cv2.subtract(thresh2, thresh)
        blur_difference = cv2.GaussianBlur(difference, (41, 41), 0)
        new_thresh = cv2.threshold(blur_difference, 0, 255, cv2.THRESH_OTSU)[1]
        
        contours, _ = cv2.findContours(new_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        frogRectangles = self.contourFiltration(contours)
        return frogRectangles
    
    def frogDetectionNoGrout(self, image): # Does not detect frogs in dark tile grouts
        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
        gray = cv2.cvtColor(hls, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_OTSU)[1]
        thresh2 = cv2.threshold(gray, 120, 255, cv2.THRESH_TRIANGLE)[1]
        difference = cv2.subtract(thresh, thresh2)
        diff_blur = cv2.GaussianBlur(difference, (71, 71), 0)
        dilate_blur = cv2.dilate(diff_blur, None, iterations=6)
        newThreshold = cv2.threshold(dilate_blur, 0, 255, cv2.THRESH_OTSU)[1]
        
        contours, _ = cv2.findContours(newThreshold.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        frogRectangles = self.contourFiltration(contours)
        return frogRectangles


    
    def frogdetectionNew(self, image):
        fgmask = self.fgbg.apply(image)
        newmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)

        cv2.imshow("mask", newmask)
        cv2.imshow("new_mask", fgmask)
        cv2.waitKey(1)





    
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
                        rectangles.pop(index)
                        break
                    
        return rectangles, overlappedRectsPairs

def count_frogs_main(video_stream, show_video = False):
    tracker = EuclideanDistTracker()
    f = FrogCount()
    # Initialize a dictionary to store the ID of the frogs
    id_dict = {}
    while video_stream.isOpened():
        # print("Is opened")
        while(True):
            frame_available, frame = video_stream.read()
            if frame_available:
                f.update(frame, drawImage=True) 



if __name__ == "__main__":
    camera_feed = cv2.VideoCapture("video_count//Media//vannVideo_Trim.mp4")
    #camera_feed = cv2.VideoCapture(0)
    count = count_frogs_main(camera_feed, show_video = True)
    print(count)
    