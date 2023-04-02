import cv2
import time
from trackers import EuclideanDistTracker
from other_funcs import count_frog

class FrogCount:
    def __init__(self):
        self.previous_frogs = [] #List of rectangles
        self.current_frogs = [] #List of rectangles
        self.frog_counter = 0
        self.tracker = EuclideanDistTracker()
        
    def frog_detect_video(self, video):
        cap = cv2.VideoCapture(video)
        id_dict = {}
        while cap.isOpened():
            while True:
                ret, frame = cap.read()
                
                NoRedContours = self.frogDetectionNoRed(frame)
                NoGroutContours = self.frogDetectionNoGrout(frame)
                sumContours = NoRedContours + NoGroutContours
                
                frog_detections = []

                for countor in sumContours:
                    (x_coord, y_coord, width, height) = cv2.boundingRect(countor)
                    frog_detections.append([x_coord, y_coord, width, height])
                    
                bounding_box_list = self.tracker.update(frog_detections)
                
                for box in bounding_box_list:
                    x, y, w, h, id = box
                    # Put a text on each box with the ID of the frog, and draw a rectangle around it
                    # (x, y-15) means top left of the box, (255,0,0) is the color of the text
                    cv2.putText(frame, str(id), (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    id_dict[id] = True
                
                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            print("Video not opened")
            
        return count_frog(id_dict)
        
    def frogDetectionMain(self, image, drawImage = False): # Launches the two detection methods
        rectanglesNoRed = self.frogDetectionNoRed(image)
        rectanglesNoGrout = self.frogDetectionNoGrout(image)
        allRectangles = rectanglesNoRed + rectanglesNoGrout
        filteredRectangles = self.rectangleOverlapFilter(allRectangles)
        if drawImage:
            for rect in filteredRectangles:
                x,y,w,h = rect
                cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        self.current_frogs = filteredRectangles
        
        numFrogsDetected = len(self.current_frogs) # 3
        allFrogs = self.previous_frogs + self.current_frogs # 3
        numAllFrogs = len(allFrogs) # 3
        FilteredFrogs = self.rectangleOverlapFilter(allFrogs) # 3
        numRemovedFrogs = numAllFrogs - len(FilteredFrogs) # 3 - 3 = 0
        self.frog_counter += numFrogsDetected - numRemovedFrogs # 3 - 0 = 3

        self.previous_frogs = self.current_frogs
        
        return self.frog_counter, self.current_frogs
        
    def frogDetectionNoRed(self, image):
        thresh = cv2.threshold(image[:,:,0], 70, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        thresh2 = cv2.threshold(image[:,:,0], 200, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
        difference = cv2.subtract(thresh2, thresh)
        blur_difference = cv2.GaussianBlur(difference, (41, 41), 0)
        new_thresh = cv2.threshold(blur_difference, 0, 255, cv2.THRESH_OTSU)[1]
        cv2.imshow("red_tresh", new_thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        contours, _ = cv2.findContours(new_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        new_contours = self.contourFiltration(contours)
        return new_contours
    
    def frogDetectionNoGrout(self, image): # Does not detect frogs in dark tile grouts
        hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
        gray = cv2.cvtColor(hls, cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_OTSU)[1]
        thresh2 = cv2.threshold(gray, 150, 255, cv2.THRESH_TRIANGLE)[1]
        difference = cv2.subtract(thresh, thresh2)
        diff_blur = cv2.GaussianBlur(difference, (71, 71), 0)
        dilate_blur = cv2.dilate(diff_blur, None, iterations=6)
        newThreshold = cv2.threshold(dilate_blur, 0, 255, cv2.THRESH_OTSU)[1]
        cv2.imshow("grout_tresh", newThreshold)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        contours, _ = cv2.findContours(newThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        new_contours = self.contourFiltration(contours)
        return new_contours
    
    def contourFiltration(self, contours, epsilonValue = 0.03, noise_threshhold_lower = 40, noise_threshhold_upper = 300): # Finds frogs using various filters
        new_contours = []
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
                        new_contours.append(contour)
        return new_contours
    
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

if __name__ == "__main__": 
    # tik = time.perf_counter()
    frame = cv2.imread("camerafeed/Main_Classes/images/vann2.jpg")
    video_path = "video_count/Media/vannVideo_Trim.mp4"
    frogCount = FrogCount()
    count = frogCount.frog_detect_video(video_path)
    print(count)
    