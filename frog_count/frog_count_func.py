# Import libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt


def count_frogs(image_path):
    image = cv2.imread(image_path)
    test = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
    blur = cv2.GaussianBlur(test, (11, 13), 0)
    canny = cv2.Canny(blur, 50, 120, 13)
    dilated = cv2.dilate(canny, (1, 1), iterations=8)
    (cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (255, 0, 0), 5)

    # print(len(cnt))
    # cv2.imshow("Image", test)
    # cv2.imshow("Blur", blur)
    # cv2.imshow("Canny", canny)
    # cv2.imshow("Dilated", dilated)
    # cv2.imshow("Contours", rgb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return len(cnt)


if __name__ == "__main__":
    c = count_frogs('froggos/froggos6.png')
    print(f"There are {c} frogs")
