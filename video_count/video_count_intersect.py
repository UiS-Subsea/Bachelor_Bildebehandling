import cv2
from frog_count_func import frogDetectionMain, rectangleOverlapFilter
import numpy as np
import time

def count_frogs_main(video_stream, show_video = False):
    frogRectangles = []
    frogRectanglesPrev = []
    numFrogs = 0
    prevFrame = None
    while video_stream.isOpened():
        # print("Is opened")
        while(True):
            frame_available, frame = video_stream.read()
            if frame_available:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frogRectangles = frogDetectionMain(frame, True, False)
                allRectangles = frogRectangles + frogRectanglesPrev
                numDuplicates = rectangleOverlapFilter(allRectangles)
                numFrogs += len(frogRectangles) - numDuplicates
                if len(frogRectangles) - numDuplicates > 0 and prevFrame is not None:
                    print("added: ", len(frogRectangles) - numDuplicates)
                    for rect in frogRectangles:
                        x,y,w,h = rect
                        cv2.rectangle(prevFrame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.imshow("frame", frame)
                    cv2.imshow("prevFrame", prevFrame)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                frogRectanglesPrev = frogRectangles
                prevFrame = frame
            else:
                break
        return numFrogs
if __name__ == "__main__":
    video_stream = cv2.VideoCapture("video_count/Media/TestVideo2.mp4")
    frogs = count_frogs_main(video_stream)
    print(frogs)