import cv2
import numpy as np
import time


#takes in an image, isolates the red dot and returns, the center of the red dot and the radius
def find_center_of_red(img):
    #creating a mask using threshold over red channel (img[:, :, 2]) <-- 2 signifies red channel
    #thresholding value is 200, which means all red values over 200 are converted to 255 (white)
    ret, mask = cv2.threshold(img[:, :,2], 200, 255, cv2.THRESH_BINARY)

    cv2.imshow("mask", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #creating a second mask
    mask2 = np.zeros_like(img)
    mask2[:, :, 0] = mask #0 = B
    mask2[:, :, 1] = mask #1 = G
    mask2[:, :, 2] = mask #2 = R

    cv2.imshow("mask2", mask2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # extracting `red/ orage` region using `biteise_and`
    red = cv2.bitwise_and(img, mask2)
    img = red

    cv2.imshow("red", red)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #converting to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #create mask for gray image
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #mask for gray image, is converted to zero where there is 255, in other words from white to black
    img[thresh == 255] = 0 
    #now all but the red center is filtered and converted into black

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #blur the image to reduce noise 
    blurred = cv2.GaussianBlur(img, (11, 13), 0)

    cv2.imshow("blurred", blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #use canny edge detection to find the edges of the red circle
    canny = cv2.Canny(blurred, 70, 120, 13)

    cv2.imshow("canny", canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #use findContours to get a list of all contoures
    (cnt, hierarchy) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, cnt, -1, (255, 0, 0), 5)

    cv2.imshow("cnt", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #there may be a lot of noise in the image, to find the correct contoure, we loop through the list of contoures (cnt)
    red_center = (0, 0), 0 #used as variable to find the largest contoure
    for c in cnt: #loops through contoures and finds the largest one
        (x, y), radius = cv2.minEnclosingCircle(c) #creates a cricle around a contour
        if radius > red_center[1]:
            red_center = (x, y), radius

    center = (int(red_center[0][0]), int(red_center[0][1]))
    radius = int(red_center[1])
    cv2.circle(img, center, radius, (0, 255, 0), 2)

    cv2.imshow("circle", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return center, radius #center is a tuple of two integers: (x, y), raduis is just an integer



if __name__ == "__main__":
    img = cv2.imread('autonomous_docking/images/docking_1080p.png')
    red_center, raduius = find_center_of_red(img)
    print(red_center, raduius)
    


