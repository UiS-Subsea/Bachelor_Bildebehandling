import cv2
import numpy as np
import matplotlib.pyplot as plt


def find_grouts(down_frame):
    low = (0, 0, 0)
    high = (100, 100, 100)

    grouts = cv2.inRange(down_frame, low, high)
    grouts_dilated = cv2.dilate(grouts, None, iterations=10)
    canny = cv2.Canny(grouts_dilated, 100, 200)
    canny_blurred = cv2.GaussianBlur(canny, (11, 13), 0)
    grout_contours, _ = cv2.findContours(grouts_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(down_frame, grout_contours, -1, (0, 255, 0), 5)


    cv2.imshow("grouts_dilated", grouts_dilated)
    cv2.imshow("canny", canny)
    cv2.imshow("Canny_blurred", canny_blurred)
    cv2.imshow("contours", down_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    cv2.imwrite("autonomous_docking//images//all_grouts.png", down_frame)
    return grout_contours


def find_relative_angle(down_frame):
    contours = find_grouts(down_frame)
    total_angle = 0
    angle_counter = 0
    
    # cv2.drawContours(down_frame, contours, -1, (0, 255, 0), 3)
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        (x, y), (w, h), angle = rect
         # Calculate the area of each contour
        area = w * h
        
        # Ignore contours that are too small or too large
        if (area >= down_frame.shape[0] * down_frame.shape[1] * 0.4) or (area < down_frame.shape[0] * down_frame.shape[1] * 0.02):
            continue
                
        if w < h:
            angle = 90 - angle
        else:
            angle = -angle

        total_angle += angle
        angle_counter += 1

        
        # if (w / h < 0.5 or w / h > 2) and cv2.contourArea(contour) > 100:
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.putText(down_frame, str(angle_counter), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.drawContours(down_frame, [box], 0, (0, 0, 255), 3)
    
    cv2.imshow("rectangles", down_frame)
    cv2.waitKey(0)
    cv2.imwrite("autonomous_docking//images//all_grouts.png", down_frame)
    cv2.destroyAllWindows()
    if angle_counter != 0:
        avg_angle = total_angle / angle_counter
    else: 
        return "SKIP"

    return avg_angle

def find_red(frame):
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # create a range for isolating only red
    lower_bound, upper_bound = (10, 10, 70), (70, 40, 255)
    #remove details from image
    blurred = cv2.GaussianBlur(frame, (11, 13), 0) 
    # creating a mask using the inRange() function and the low, high range, then dilating it
    red = cv2.inRange(blurred, lower_bound, upper_bound)
    dilated = cv2.dilate(red, None, iterations=6)
    red_isolated = cv2.bitwise_and(frame, frame, mask=dilated)
    canny = cv2.Canny(red_isolated, 100, 200)
    # use findContours to get a list of all contoures
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # there may be a lot of noise in the image, to find the correct contoure, we loop through the list of contoures
    red_center = (0, 0), 0
    for c in contours:
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > red_center[1]: # TODO may need to improve filtration of contures
            red_center = (x, y), radius
    # write center and radius as integers
    center_point = (int(red_center[0][0]), int(red_center[0][1]))
    radius = int(red_center[1])
    # draw a circle around the red dot
    cv2.circle(frame, center_point, radius, (0, 255, 0), 2)
    show_all(blurred, red, dilated, canny)
    cv2.imshow("frame", frame)
    cv2.imwrite("autonomous_docking//images//docking_red.png", frame)
    cv2.waitKey(0)
    return center_point, radius


def show_all(img1, img2, img3, img4):
    # Create a figure and axis object
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)
    img4 = cv2.cvtColor(img4, cv2.COLOR_BGR2RGB)
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8,8))

    ax[0,0].imshow(img1)
    ax[0,1].imshow(img2)
    ax[1,0].imshow(img3)
    ax[1,1].imshow(img4)

    # Set the title for each subplot
    ax[0,0].set_title('Blurred')
    ax[0,1].set_title('inRange()')
    ax[1,0].set_title('Dilated')
    ax[1,1].set_title('Canny')

    # Hide the axis tick labels
    ax[0,0].set_xticklabels([])
    ax[0,0].set_yticklabels([])
    ax[0,1].set_xticklabels([])
    ax[0,1].set_yticklabels([])
    ax[1,0].set_xticklabels([])
    ax[1,0].set_yticklabels([])
    ax[1,1].set_xticklabels([])
    ax[1,1].set_yticklabels([])

    # Show the plot
    plt.show()
    cv2.waitKey(0)

if __name__ == "__main__":
    img3 = cv2.imread("autonomous_docking//images//pool_test2.png")

    #print(find_relative_angle(img3))
    find_red(img3)

