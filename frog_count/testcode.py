# Import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
import time



def count_frogs2(image): #color either be 0, 1, 2 representing (0, 1, 2) -> (r, g, b)
    start = time.perf_counter()
    frogs = 0
    
    # Manipulate image different ways:
    thresh = cv2.threshold(image[:,:,0], 70, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
    thresh2 = cv2.threshold(image[:,:,0], 200, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
    thresh_eroded = cv2.erode(thresh, None, iterations=6)
    difference = cv2.subtract(thresh_eroded, thresh2)
    difference_eroded = cv2.erode(difference, None, iterations=2)
    difference_dilated = cv2.dilate(difference_eroded, None, iterations=10)
    difference_blurred = cv2.GaussianBlur(difference_dilated, (11, 13), 0)

    canny = cv2.Canny(difference_blurred, 50, 120, 13)
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_time = time.perf_counter() - start
    print(total_time)


    cv2.imshow("difference", difference_blurred)
    cv2.imshow("thresh2_dilated", thresh_eroded)
    cv2.imshow("image", image)
    cv2.imshow("thresh", thresh)
    cv2.imshow("canny", canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return contours

if __name__ == "__main__":
    image = cv2.imread("frog_count/froggos/vann4.jpg")
    contours = []
    c = count_frogs2(image)