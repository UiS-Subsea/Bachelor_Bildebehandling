from matplotlib import pyplot as plt
import cv2
import math

def show_images(image, converted, blur, canny, blur2, contours, t = None):
    fig, axs = plt.subplots(2, 3, figsize=(10, 10))
    axs[0, 0].imshow(image)
    axs[0, 0].set_title("Original Image")
    axs[0, 1].imshow(converted)
    axs[0, 1].set_title("Converted Image")
    axs[0, 2].imshow(blur)
    axs[0, 2].set_title("Gaussian Blur")
    axs[1, 0].imshow(canny)
    axs[1, 0].set_title("Canny Edge Detection")
    axs[1, 1].imshow(blur2)
    axs[1, 1].set_title("Blur2 Image")
    axs[1, 2].imshow(contours)
    axs[1, 2].set_title("Contours")
    plt.show()

    if t is not None:
        plt.imshow(t)
        plt.show()


def show_image(image):
    plt.imshow(image)
    plt.show()