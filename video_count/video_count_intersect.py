import cv2
from frog_count.frog_count_func import frogDetectionMain, rectangleOverlapFilter
import time

def count_frogs_main(video_stream, show_video = False):
    frogRectangles = []
    frogRectanglesPrev = []
    numFrogs = 0
    while video_stream.isOpened():
        # print("Is opened")
        while(True):
            frame_available, frame = video_stream.read()
            if frame_available:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                _, frogRectangles = frogDetectionMain(frame)
                allRectangles = frogRectangles + frogRectanglesPrev
                filteredRectangles = rectangleOverlapFilter(allRectangles)
                numFrogs += len(filteredRectangles)
                frogRectanglesPrev = frogRectangles
                
            else:
                break
    return numFrogs
if __name__ == "__main__":
    video_stream = cv2.VideoCapture("video_count/Media/TestVideo1.mp4")
    frogs = count_frogs_main(video_stream)
    print(frogs)