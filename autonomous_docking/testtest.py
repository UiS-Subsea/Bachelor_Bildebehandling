import cv2
import numpy as np

def find_cirlce(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT_ALT, 2, 100, param2=0.5)
    
    if circles is not None:
        new_circles = np.round(circles[0, :].astype("int"))

        for (x, y, r) in new_circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 3)

    else:
        print("nerd")


    cv2.imshow("img", frame)
    cv2.waitKey(0)
    





if __name__ == "__main__":
    img = cv2.imread("autonomous_docking\images\pool_test2.png")
    find_cirlce(img)


    