import cv2
from other_funcs import *
from trackers import EuclideanDistTracker
import time

def count_frogs_main(video_stream):
    tracker = EuclideanDistTracker()
    while video_stream.isOpened():
        while(True):
            frame_available, frame = video_stream.read()
            if frame_available:
                contours = find_contours(frame, 0)
                # OpenCV opens frames in BGR, Convert the frame to RGB
                rgb = bgr2rgb(frame)
            else:
                break

            detections = []

            for countor in contours:
                (x_coord, y_coord, width, height) = cv2.boundingRect(countor)
                detections.append([x_coord, y_coord, width, height])

            bounding_box_list = tracker.update(detections)
            
            # Initialize a dictionary to store the ID of the frogs
            id_dict = {}
            for box in bounding_box_list:
                x, y, w, h, id = box
                # Put a text on each box with the ID of the frog, and draw a rectangle around it
                # (x, y-15) means top left of the box, (255,0,0) is the color of the text
                cv2.putText(rgb, str(id), (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.rectangle(rgb, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # cv2.imshow("Image", rgb)
                # cv2.imshow("Blur", img1)
                # cv2.imshow("Canny", img2)
                # cv2.imshow("Blur2", img3)
                # cv2.imshow("Dilated", img4)
                # show_images(rgb, blur, canny, blur2, dilated)
                id_dict[id] = True
                
        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                video_stream.release()
                cv2.destroyAllWindows()
                break
        cv2.destroyAllWindows()
    else:
        "Video not opened"

    return count_frog(id_dict)

    








if __name__ == "__main__":
    camera_feed = cv2.VideoCapture("video_count/Media/TestVideo1.mp4")
    c = count_frogs_main(camera_feed)
    