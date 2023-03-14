# Import libraries
import cv2
import time
    
def frogDetectionMain(image, drawImage = False): # Launches the two detection methods
    rectanglesNoRed = frogDetectionNoRed(image)
    rectanglesNoGrout = frogDetectionNoGrout(image)
    allRectangles = rectanglesNoRed + rectanglesNoGrout
    filteredRectangles = rectangleOverlapFilter(allRectangles)
    if drawImage:
        for rect in filteredRectangles:
            x,y,w,h = rect
            cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return len(filteredRectangles), filteredRectangles
    
def frogDetectionNoRed(image): # 
    thresh = cv2.threshold(image[:,:,0], 70, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    thresh2 = cv2.threshold(image[:,:,0], 200, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    difference = cv2.subtract(thresh2, thresh)
    blur_difference = cv2.GaussianBlur(difference, (41, 41), 0)
    new_thresh = cv2.threshold(blur_difference, 0, 255, cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(new_thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    frogRectangles = contourFiltration(contours)
    return frogRectangles

def frogDetectionNoGrout(image): # Does not detect frogs in dark tile grouts
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
    gray = cv2.cvtColor(hls, cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_OTSU)[1]
    thresh2 = cv2.threshold(gray, 120, 255, cv2.THRESH_TRIANGLE)[1]
    difference = cv2.subtract(thresh, thresh2)
    diff_blur = cv2.GaussianBlur(difference, (71, 71), 0)
    dilate_blur = cv2.dilate(diff_blur, None, iterations=6)
    newThreshold = cv2.threshold(dilate_blur, 0, 255, cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(newThreshold.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    frogRectangles = contourFiltration(contours)
    return frogRectangles

def contourFiltration(contours, epsilonValue = 0.03, noise_threshhold_lower = 40, noise_threshhold_upper = 300): # Finds frogs using various filters
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
    return frog_rectangles

def rectangleOverlapFilter(rectangles): # Filters out rectangles that overlap O(n^2)
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

def show_images(images):
    for img in images:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__": 
    # tik = time.perf_counter()
    frogs, frogRectangles = frogDetectionMain(cv2.imread("frog_count/froggos/froggos9.png"), True)
    # tok = time.perf_counter() - tik
    # print(f"Time: {tok} seconds")
    print(f"There are {frogs} frogs")
