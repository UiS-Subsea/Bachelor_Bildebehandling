# Import libraries
import cv2
import matplotlib.pyplot as plt


def count_frogs(image_path):
    frogs = 0
    image = cv2.imread(image_path)
    blurred = cv2.GaussianBlur(image, (11, 13,), 0)
    
    low = (20, 40, 20) #lowest end of the range (black)
    high = (60, 80, 60) #highest end of the range (red)

    mask1 = cv2.inRange(blurred, low, high)
    dilated = cv2.dilate(mask1, None, iterations=8)

    darkgray_lines = cv2.bitwise_and(image, image, mask=dilated)

    cv2.imshow("dark_gray", darkgray_lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(len(cnt))
    return frogs



if __name__ == "__main__":
    c = count_frogs("frog_count/froggos/vann2.jpg")
    print(f"There are {c} frogs")
