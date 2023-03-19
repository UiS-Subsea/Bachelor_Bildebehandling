import cv2
import numpy as np


def find_grouts(down_frame):
    low = (1, 1, 1)
    high = (100, 100, 100)

    grouts = cv2.inRange(down_frame, low, high)
    grouts_dilated = cv2.dilate(grouts, None, iterations=10)
    canny = cv2.Canny(grouts_dilated, 100, 200)
    canny_blurred = cv2.GaussianBlur(canny, (11, 13), 0)
    grout_contours, _ = cv2.findContours(grouts_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(grout_contours))
    cv2.drawContours(down_frame, grout_contours, -1, (0, 255, 0), 5)


    cv2.imshow("grouts_dilated", grouts_dilated)
    cv2.imshow("canny", canny)
    cv2.imshow("Canny_blurred", canny_blurred)
    cv2.imshow("contours", down_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
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
        area = cv2.contourArea(contour)
        #print(f"area: {area}")
        
        # Ignore contours that are too small or too large
        if (area >= down_frame.shape[0] * down_frame.shape[1] * 0.4) or (area < down_frame.shape[0] * down_frame.shape[1] * 0.02):
            continue
                
        if w < h:
            angle = 90 - angle
        else:
            angle = -angle

        total_angle += angle
        angle_counter += 1

        # print(i)
        # print(angle)
        
        # if (w / h < 0.5 or w / h > 2) and cv2.contourArea(contour) > 100:
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.putText(down_frame, str(angle_counter), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.drawContours(down_frame, [box], 0, (0, 0, 255), 3)
    
    cv2.imshow("rectangles", down_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if angle_counter != 0:
        avg_angle = total_angle / angle_counter
    else: 
        return "SKIP"

    # print(F"largest area: {down_frame.shape[0] * down_frame.shape[1]}")
    return avg_angle



if __name__ == "__main__":
    img1 = cv2.imread("autonomous_docking//images//transect1.png")
    img2 = cv2.imread("autonomous_docking//images//transect2.png")
    img3 = cv2.imread("autonomous_docking//images//transect3.png")

    print(find_relative_angle(img3))
