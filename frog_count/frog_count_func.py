# Import libraries
import cv2
import matplotlib.pyplot as plt


def count_frogs(image_path):
    frogs = 0
    image = cv2.imread(image_path)
    test = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
    # gray = cv2.cvtColor(test, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(test, (11, 13), 0)
    canny = cv2.Canny(blur, 50, 120, 13)
    blur2 = cv2.GaussianBlur(canny, (11, 13), 0)
    dilated = cv2.dilate(canny, None, iterations=3)
    dilated2 = cv2.dilate(blur2, None, iterations=3)
    (cnt, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #cnt is an array of conoures
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #cv2.drawContours(rgb, cnt, -1, (255, 0, 0), 5)

    #########################################################
    
    for contour in cnt:
        # epsilon value can be tweaked
        epsilon = 0.03*cv2.arcLength(contour, True)
        # approx is the polygonal approximation of the contour
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        
        if len(approx) > 5: # More than 4 sides means its more round than a square, more sides means more circular
            # w,h width and height
            _, _, w, h = cv2.boundingRect(contour)
            # Noise threshhold to ignore small and large contours, can be tweaked
            noise_threshhold_lower = 30
            noise_threshhold_upper = 70
            if  w > noise_threshhold_lower < h and w < noise_threshhold_upper > h:
                frogs += 1
                cv2.drawContours(rgb, [approx], -1, (255, 0, 0), 5)
    
    #########################################################

    show_images(image, test, blur, canny, blur2, rgb, dilated, dilated2)

    #########################################################
    # print(len(cnt))
    return frogs

def show_images(image, converted, blur, canny, blur2, contours, dilated, dilated2, t = None):
    fig, axs = plt.subplots(2, 4, figsize=(10, 10))
    axs[0, 0].imshow(image)
    axs[0, 0].set_title("Original Image")
    axs[0, 1].imshow(converted)
    axs[0, 1].set_title("Converted Image")
    axs[0, 2].imshow(blur)
    axs[0, 2].set_title("Gaussian Blur")
    axs[0, 3].imshow(dilated)
    axs[0, 3].set_title("Dilated")
    axs[1, 0].imshow(canny)
    axs[1, 0].set_title("Canny Edge Detection")
    axs[1, 1].imshow(blur2)
    axs[1, 1].set_title("Blur2 Image")
    axs[1, 2].imshow(contours)
    axs[1, 2].set_title("Contours")
    axs[1, 3].imshow(dilated2)
    axs[1, 3].set_title("Dilated2")
    plt.show()

    if t is not None:
        plt.imshow(t)
        plt.show()

if __name__ == "__main__":
    c = count_frogs("frog_count/froggos/vann2.jpg")
    print(f"There are {c} frogs")
