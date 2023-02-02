from matplotlib import pyplot as plt
import cv2
import math

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