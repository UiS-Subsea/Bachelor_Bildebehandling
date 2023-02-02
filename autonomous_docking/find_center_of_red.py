import cv2
import numpy as np
import time


#takes in an image, isolates the red dot and returns, the center of the red dot and the radius
def find_center_of_red(img):
    ret, mask = cv2.threshold(img[:, :,2], 200, 255, cv2.THRESH_BINARY)

    mask3 = np.zeros_like(img)
    mask3[:, :, 0] = mask
    mask3[:, :, 1] = mask
    mask3[:, :, 2] = mask

    # extracting `red/ orage` region using `biteise_and`
    orange = cv2.bitwise_and(img, mask3)
    img = orange
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY) #gray is the image we apply the threshold, it is between gray color 200 and 255
    img[thresh == 255] = 0 #here we say that the threshold, is converted to zero, in other words converted to black
    canny = cv2.Canny(img, 70, 120, 13)

    (cnt, hierarchy) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    (x, y), radius = cv2.minEnclosingCircle(cnt[0])
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(img, center, radius, (0, 255, 0), 2)

    # cv2.imshow("canny", canny)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow("orange", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return center, radius #center is a tuple of two integers: (x, y), raduis is just an integer



if __name__ == "__main__":
    start = time.perf_counter()
    img = cv2.imread('autonomous_docking/images/dockingstation2.png')
    new_img = find_center_of_red(img)
    end = time.perf_counter()
    print(start - end)


