import cv2
import numpy as np
import time


#takes in an image, isolates the red dot and returns, the center of the red dot and the radius
def find_center_of_red(img):
    #create a range for isolating only red
    #the values in the range may be tweaked for any color or colorvariation
    low = (0, 0, 0) #lowest end of the range (black)
    high = (100, 100, 255) #highest end of the range (red)

    #creating a mask using the inRange() function and the low, high range
    mask1 = cv2.inRange(img, low, high)

    #using bitwise_and() to convert from mask to actual image format 
    red_isolated = cv2.bitwise_and(img, img, mask=mask1)

    #use canny edge detection to find the edges of the red circle
    #input 2 and 3 specify min and max Val for detecting edge, though using different-
    #values dont seem to have much effect
    canny = cv2.Canny(red_isolated, 100, 200)

    #use findContours to get a list of all contoures represented as cnt
    #cv2.RETR_EXTERNAL (retrieve external) means contour of the outside of object
    #cv2.CHAIN_APPROX_SIMPLE means the contour is defined by a simple chain of point and not every single point-
    #to save performance
    (cnt, hierarchy) = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(red_isolated, cnt, -1, (255, 0, 0), 7)

    #there may be a lot of noise in the image, to find the correct contoure, we loop through the list of contoures (cnt)
    red_center = (0, 0), 0 #used as variable to find the largest contoure
    for c in cnt: #loops through contoures and finds the largest one
        (x, y), radius = cv2.minEnclosingCircle(c) #creates a cricle around a contour
        if radius > red_center[1]:
            red_center = (x, y), radius

    center = (int(red_center[0][0]), int(red_center[0][1]))
    radius = int(red_center[1])
    cv2.circle(img, center, radius, (0, 255, 0), 2)

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return center, radius #center is a tuple of two integers: (x, y), raduis is just an integer



if __name__ == "__main__":
    img = cv2.imread('depth_testing/3dmodel_img1.png')
    red_center, raduius = find_center_of_red(img)
    print(red_center, raduius)