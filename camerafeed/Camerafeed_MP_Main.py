import cv2
import time
import multiprocessing as mp
import functools
import asyncio
import matplotlib.pyplot as plt

class CameraFeed:
    def __init__(self, cam_name="Cam1", gstreamer=False, port=5000):
        self.name = cam_name
        self.started = False
        self.prev_time = 0
        self.gstreamer = gstreamer
        self.port = port
        self.frame = None
        self.recording = False
                
    def get_frame(self):
        return self.frame
        
    def update(self):
        if self.started:
            # print("Updating")
            self.ret, self.frame = self.cap.read()
            if self.recording:
                self.videoresult.write(self.frame)
            self.new_time = time.time()
            self.fps = 1 / (self.new_time - self.prev_time)
            self.prev_time = self.new_time
            
    def show_frame(self):
        if self.started:
            # print("Showing frame")
            if self.ret:
                resized = cv2.resize(self.frame, (640, 480))
                cv2.putText(resized, str(int(self.fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                cv2.imshow(self.name, resized)
                
        
    def start(self):
        self.started = True
        if self.gstreamer:
            gst_feed = f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port={self.port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
        else:   
            self.cap = cv2.VideoCapture(0)
            
        self.videoresult = cv2.VideoWriter(f'{self.name}.avi', cv2.VideoWriter_fourcc(*'MJPG'),30, (int(self.cap.get(3)), int(self.cap.get(4))))
        while self.started:
            self.update()
            self.show_frame()
            key = cv2.waitKey(1)
            if key == ord("q"):
                self.started = False
                break
            elif key == ord("s"):
                cv2.imwrite("test.jpg", self.frame)
            elif key == ord("r"):
                self.recording = not self.recording
                print(f"Recording" + self.name)
            elif key == ord("t"):
                print("Stopped recording" + self.name)
                self.videoresult.release()
    
            
def fmap(func):
    return func()

if __name__ == "__main__":
    cam = CameraFeed("Cam1", gstreamer=True, port=5000)
    # cam = CameraFeed("Cam1", gstreamer=False)
    cam2 = CameraFeed("Cam2", gstreamer=True, port=5001)
    with mp.Pool(2) as p:
            p.map(fmap, [cam.start, cam2.start])

