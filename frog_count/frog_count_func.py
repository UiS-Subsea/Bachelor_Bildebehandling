# Import libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt


def count_frogs(image_path):
    image = cv2.imread(image_path)
    test = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
    # gray = cv2.cvtColor(test, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(test, (11, 13), 0)
    canny = cv2.Canny(blur, 50, 120, 13)
    dilated = cv2.dilate(canny, (1, 1), iterations=8)
    (cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (255, 0, 0), 5)

    #########################################################

    # show_images(image, test, blur, canny, dilated, rgb, extra = None)

    #########################################################
    # print(len(cnt))
    return len(cnt)

def show_images(image, converted, blur, canny, dilated, contours, t = None):
    fig, axs = plt.subplots(2, 3, figsize=(10, 10))
    axs[0, 0].imshow(image)
    axs[0, 0].set_title("Original Image")
    axs[0, 1].imshow(converted)
    axs[0, 1].set_title("Converted Image")
    axs[0, 2].imshow(blur)
    axs[0, 2].set_title("Gaussian Blur")
    axs[1, 0].imshow(canny)
    axs[1, 0].set_title("Canny Edge Detection")
    axs[1, 1].imshow(dilated)
    axs[1, 1].set_title("Dilated Image")
    axs[1, 2].imshow(contours)
    axs[1, 2].set_title("Contours")
    plt.show()

    if t is not None:
        plt.imshow(t)
        plt.show()

if __name__ == "__main__":
    c = count_frogs('froggos/froggos8.png')
    print(f"There are {c} frogs")
