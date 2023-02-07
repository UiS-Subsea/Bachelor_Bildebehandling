import cv2
from other_funcs import *
from trackers import EuclideanDistTracker
import time


tracker = EuclideanDistTracker()
###########################################################################################

# image = cv2.imread("video_count/froggos4.jpg")
# real_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# test = cv2.cvtColor(real_image, cv2.COLOR_RGB2HLS_FULL)
# blur = cv2.GaussianBlur(test, (11, 13), 0)
# canny = cv2.Canny(blur, 50, 120, 13)
# blur2 = cv2.GaussianBlur(canny, (11, 13), 0)
# (cnt, hierarchy) = cv2.findContours(blur2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #cnt is an array of conoures
# rgb = cv2.cvtColor(real_image, cv2.COLOR_BGR2RGB)

###########################################################################################

cap = cv2.VideoCapture("video_count/Froggies3.mp4")
while cap.isOpened():
    while(True):
        ret, frame = cap.read()
        if ret:
            contours = find_contours(frame)
            rgb = bgr2rgb(frame)
        else:
            break

    ###########################################################################################
        detections = []

        for countor in contours:
            (x, y, w, h) = cv2.boundingRect(countor)
            detections.append([x, y, w, h])

        boxes_ids = tracker.update(detections)
        id_dict = {}
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(rgb, str(id), (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(rgb, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow("Image", rgb)
            # cv2.imshow("Blur", blur)
            # cv2.imshow("Canny", canny)
            # cv2.imshow("Blur2", blur2)
            # cv2.imshow("Dilated", dilated)
            # show_images(rgb, blur, canny, blur2, dilated)
            id_dict[id] = True
            
    
    # key = cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    # if key == ord("q"):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    "Video not opened"

print(f"Number of frogs: {(count_frog(id_dict))} \n")

# show_images(real_image, test, blur, canny, blur2, rgb)
