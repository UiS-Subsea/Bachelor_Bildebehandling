from PIL import Image
import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt

# Monitor seagrass
# Detect whether there is more or less seagrass between two images.
# Seagrass represented by 8x8 grid with green and white tiles. Green = seagrass, white = not seagrass.
# Illustrated on page 31 here: https://files.materovcompetition.org/2023/EXPLORER_Prop_Building_2023_Final.pdf

def calculate_seagrass_percent(img_name): # Takes in image name, returns percentage of area covered in seagrass. Example: image1.png
    img_path = "monitor_seagrass\images\\" + img_name
    
    # RGB values from example image:
    # Green squares:     rgba(5,   102, 69,  255)
    # White squares:     rgba(171, 186, 219, 255)
    # White background:  rgba(179, 196, 216, 255)
    # grey square lines: rgba(120, 145, 172, 255)
    
    with Image.open(img_path) as img:
        img = img.convert("RGB") # instead of RGBA for efficiency
        grey_px_count = 0
        size_x, size_y = img.size
        px = img.load() # Pixel matrix
        
        test_img = Image.new(mode = "RGB", size= (size_x, size_y), color=(255, 255, 255))
        
        for x in range(size_x):
            for y in range(size_y):
                if is_grey(px[x, y]):
                    grey_px_count += 1
                    test_img.putpixel((x, y), px[x, y])
        
        ## gray image + Gaussian Blur
        #img = cv2.imread(img_path)
        ##converted = convert_hls(img)
        #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #kernel_size = 5
        #blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
        #
        ##Edge detection w canny
        #low_threshold = 50
        #high_threshold = 150
        #edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
        #
        ##HoughLinesP to get lines
        #rho = 1  # distance resolution in pixels of the Hough grid
        #theta = np.pi / 180  # angular resolution in radians of the Hough grid
        #threshold = 10  # minimum number of votes (intersections in Hough grid cell)
        #min_line_length = 30  # minimum number of pixels making up a line
        #max_line_gap = 10  # maximum gap in pixels between connectable line segments
        #line_image = np.copy(img) * 0  # creating a blank to draw lines on
#
        ## Run Hough on edge detected image
        ## Output "lines" is an array containing endpoints of detected line segments
        #lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
        #            min_line_length, max_line_gap)
#
        #for line in lines:
        #    for x1,y1,x2,y2 in line:
        #        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
        #
        #lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
        #cv2.imshow("res", lines_edges)
        #cv2.waitKey(0)  
        
        return test_img, grey_px_count
                    
                    
                    
def is_grey(px):
    if 80 < px[0] < 155 and 130 < px[1] < 175 and 130 < px[2] < 205:
        return True
    return False

def detect_squares(img_path):
    squares = 0
    
    img = cv2.imread(img_path)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    #cv2.imshow("blur", blur)
    #canny = cv2.Canny(blur, 50, 200)
    #cv2.imshow("canny", canny)
    dilated = cv2.dilate(blur, None, iterations=3)
    #cv2.imshow("dilated", dilated)
    
    _, thresh = cv2.threshold(dilated, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # epsilon value can be tweaked
        epsilon = 0.015*cv2.arcLength(contour, True)
        # approx is the polygonal approximation of the contour
        approx = cv2.approxPolyDP(contour, epsilon, True)
        cv2.drawContours(dilated, [approx], 0, (0), 3)
        
        if len(approx) == 4: # 4 sides
            i, j = approx[0][0]
            # x,y top left corner. w,h width and height
            x, y, w, h = cv2.boundingRect(contour)
            ratio = float(w)/h
            if ratio >= 0.9 and ratio <= 1.1 and w > 20 and h > 20:
                squares += 1
                cv2.putText(dilated, 'Square', (i, j), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
    #cv2.imshow("res", dilated)
    print(squares)
    #cv2.waitKey(0)
    return squares

if __name__ == "__main__":
    #picture, amount = calculate_seagrass_percent("Example1_grey.png")
    #print(amount)
    #picture.show()
    squares = detect_squares("monitor_seagrass\images\Example1.png")
    