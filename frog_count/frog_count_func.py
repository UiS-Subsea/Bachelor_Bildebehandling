# Import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np


def count_frogs(image_path):
    frogs = 0
    image = cv2.imread(image_path)
    # Manipulate image different ways:
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
    gray = cv2.cvtColor(hls, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(hls, (11, 13), 0)
    canny = cv2.Canny(blur, 50, 120, 13)
    blur2 = cv2.GaussianBlur(canny, (11, 13), 0)
    dilated = cv2.dilate(canny, None, iterations=3)
    dilated2 = cv2.dilate(blur2, None, iterations=10)
    erode = cv2.erode(dilated2, None, iterations=8)
    thresh = cv2.threshold(dilated2, 60, 255, cv2.ADAPTIVE_THRESH_MEAN_C)[1]
    thresh2 = cv2.threshold(dilated2, 60, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    (contours1, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (contours2, _) = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rgb = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    rgb1 = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    rgb2 = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    rgb3 = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    rgb4 = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    rgb5 = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
    #cv2.drawContours(rgb, contours, -1, (255, 0, 0), 5)
    cv2.drawContours(rgb1, contours1, -1, (255, 0, 0), 5)
    cv2.drawContours(rgb2, contours2, -1, (255, 0, 0), 5)
    cv2.drawContours(rgb3, contours, -1, (255, 0, 0), 5)
    
    #########################################################
    for contour in contours:
        # epsilon value can be tweaked, higher value allows for larger approximated polygon, more likely to have less sides
        epsilon = 0.03*cv2.arcLength(contour, True)
        # approx is the polygonal approximation of the contour
        approx = cv2.approxPolyDP(contour, epsilon, True)
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(rgb4, [box], -1, (255, 0, 0), 5)
        cv2.drawContours(rgb, [approx], -1, (255, 0, 0), 5)
        if 10 > len(approx) > 4: # More than 4 sides means its more round than a square, more sides means more circular
            # w,h width and height
            x, y, w, h = cv2.boundingRect(approx)
            if 0.7 < w/h < 1.3: # If the width and height are within 20% of each other, it is a square
                
                # Noise threshhold to ignore small and large contours, can be tweaked
                noise_threshhold_lower = 40
                noise_threshhold_upper = 300
                if  w > noise_threshhold_lower < h and w < noise_threshhold_upper > h:
                    frogs += 1
                    
                    cv2.rectangle(rgb5, (x,y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    print("Noise1")
            else:
                print("Noise2")
        else:
            print("Noise3")
        
    #########################################################

    show_images(rgb4, rgb5, rgb3, thresh2, image, rgb, thresh, dilated2)

    #########################################################
    # print(len(contours))
    return frogs

def show_images(rect, TREE, LIST, canny, image, contours, dilated, dilated2, t = None):
    fig, axs = plt.subplots(2, 4, figsize=(10, 10))
    axs[0, 0].imshow(image[:,:,0], cmap="Reds")
    axs[0, 0].set_title("Red")
    axs[0, 1].imshow(TREE)
    axs[0, 1].set_title("FROGS")
    axs[0, 2].imshow(LIST)
    axs[0, 2].set_title("RETR_LIST Countours")
    axs[0, 3].imshow(dilated)
    axs[0, 3].set_title("threshold")
    axs[1, 0].imshow(image[:,:,1], cmap="Greens")
    axs[1, 0].set_title("Green")
    axs[1, 1].imshow(image[:,:,2], cmap="Blues")
    axs[1, 1].set_title("Blue")
    axs[1, 2].imshow(contours)
    axs[1, 2].set_title("PolyDbApproxContours")
    axs[1, 3].imshow(dilated2)
    axs[1, 3].set_title("Dilated2")
    plt.show()

    if t is not None:
        plt.imshow(t)
        plt.show()

if __name__ == "__main__":
    c = count_frogs("frog_count/froggos/vann4.jpg")
    print(f"There are {c} frogs")
