from matplotlib import pyplot as plt
import cv2
import math
import numpy as np

def show_images(image1, image2, image3 = None, image4 = None, image5 = None, image6 = None, t = None):
    fig, axs = plt.subplots(2, 3, figsize=(10, 10))

    axs[0, 0].imshow(image1)
    axs[0, 0].set_title("Image 1")

    axs[0, 1].imshow(image2)
    axs[0, 1].set_title("Image 2")

    if image3 is not None:
        axs[0, 2].imshow(image3)
        axs[0, 2].set_title("Image 3")
    if image4 is not None:
        axs[1, 0].imshow(image4)
        axs[1, 0].set_title("Image 4")
    if image5 is not None:
        axs[1, 1].imshow(image5)
        axs[1, 1].set_title("Image 5")
    if image6 is not None:
        axs[1, 2].imshow(image6)
        axs[1, 2].set_title("Image 6")
    
   
    plt.show()
    if t is not None:
        plt.imshow(t)
        plt.show()


def show_image(image):
    plt.imshow(image)
    plt.show()


def count_frog(dict):
    return max(dict.keys()) + 1 # +1 because the first frog is ID 0


def find_contours(frame, mode = 0):
    if mode == 0:
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        test = cv2.cvtColor(frame1, cv2.COLOR_RGB2HLS_FULL)
        blur = cv2.GaussianBlur(test, (13, 13), 0)
        canny = cv2.Canny(blur, 70, 270, 13)
        blur2 = cv2.GaussianBlur(canny, (11, 13), 0)
        dilated = cv2.dilate(blur2, None, iterations=7)
        (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #cnt is an array of conoures
        return contours, [test, blur, canny, blur2, dilated]
    
    elif mode == 1:
        color_converted = cv2.cvtColor(frame, cv2.COLOR_RGB2HLS_FULL)
        blur = cv2.GaussianBlur(color_converted, (13, 13), 0)
        canny = cv2.Canny(blur, 50, 120, 13)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(canny, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours, [color_converted, blur, canny, dilated]
    
    elif mode == 2:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (13, 13), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours, [gray, blur, thresh, dilated]

def bgr2rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def unpack(n, seq):
    it = iter(seq)
    for _ in range(n - 1):
        yield next(it, None)
    yield tuple(it)



if __name__ == "__main__":
    print("This is a module, not a program")
    print("Please import this module and use its functions")
    print("For example: from other_funcs import show_images")
    print("For example: from other_funcs import count_frog")
    print("For example: from other_funcs import find_contours")
    print("For example: from other_funcs import bgr2rgb")