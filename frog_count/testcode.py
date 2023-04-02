# Import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time

def show(img, name):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_func(img_path):
    img = cv2.imread(img_path)
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
    
    horizontal = bw.copy()
    vertical = bw.copy()
    
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    
    hor_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    
    horizontal = cv2.erode(horizontal, hor_structure)
    # horizontal = cv2.dilate(horizontal, hor_structure)
    # horizontal = cv2.bitwise_not(horizontal)

    rows = vertical.shape[0]
    vertical_size = rows // 30
    
    ver_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
    vertical = cv2.erode(vertical, ver_structure)
    # vertical = cv2.dilate(vertical, ver_structure)
    # vertical = cv2.bitwise_not(vertical)
    edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
    edges2 = cv2.adaptiveThreshold(horizontal, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel)
    edges2 = cv2.dilate(edges2, kernel)
    
    smooth = np.copy(vertical)
    smooth = cv2.blur(smooth, (2, 2))
    smooth2 = np.copy(horizontal)
    smooth2 = cv2.blur(smooth2, (2, 2))
    
    
    (rows, cols) = np.where(edges != 0)
    (rows2, cols2) = np.where(edges2 != 0)
    
    horizontal[rows2, cols2] = smooth2[rows2, cols2]
    
    vertical[rows, cols] = smooth[rows, cols]
    
    horizontal = cv2.dilate(horizontal, hor_structure, iterations=8)
    vertical = cv2.dilate(vertical, ver_structure, iterations=8)
    
    
    
    grids = cv2.add(horizontal, vertical)
    test = cv2.subtract(bw, grids)
    
    test = cv2.bitwise_not(test)
    test = cv2.adaptiveThreshold(test, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, -2)
    
    kernel1 = np.ones((2,3),np.uint8)
    kernel2 = np.ones((3,3),np.uint8)
    test = cv2.erode(test, kernel1, iterations=3)
    test = cv2.dilate(test, kernel2, iterations=12)
    cv2.imshow("Grouts", np.hstack([horizontal, vertical]))
    cv2.imshow("Input", output)
    cv2.imshow("Output", test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def test_func2(img_path):
    img = cv2.imread(img_path)
    output = img.copy()
    
    img = cv2.GaussianBlur(img,(5,5), 0)
    bins = np.array([0,51,102,153,204,255])
    img[:,:,:] = np.digitize(img[:,:,:],bins,right=True)*51
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,background = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
    ret,foreground = cv2.threshold(gray,0,255,cv2.THRESH_TOZERO_INV+cv2.THRESH_OTSU)  #Currently foreground is only a mask
    foreground = cv2.bitwise_and(img,img, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
    final = foreground + background
    
    cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=True)
    cv2.imshow("Dangyo", np.hstack([output, final]))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    test_func("frog_count/froggos/vann1.jpg")
