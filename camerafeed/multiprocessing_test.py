import cv2
import time
import multiprocessing as mp
import functools
import asyncio
import matplotlib.pyplot as plt
class CameraFeed:
    def __init__(self):
        self.started = False
        # self.process = mp.Process(target=self.start)
        self.prev_time = 0
        with mp.Pool(5) as p:
            p.map(self.map_func, [self.start])
        # self.frame = self.cap.read()[1]
        
    # def init_camera(self):
    #     global cap
    #     cap = cv2.VideoCapture(0)
        
    def update_loop(self):
        while self.started:
            print("Updating (Loop)")
            self.frame = self.cap.read()[1]
            cv2.waitKey(1)
            # yield frame
        
    def show_frame_loop(self):
        while self.started:
            print("Showing frame (Loop)")
            cv2.imshow("Frame", self.frame)
            # cv2.waitKey(1)
            
    def update(self):
        if self.started:
            # print("Updating")
            self.ret, self.frame = self.cap.read()
            self.new_time = time.time()
            self.fps = 1 / (self.new_time - self.prev_time)
            self.prev_time = self.new_time
            
    def show_frame(self):
        if self.started:
            # print("Showing frame")
            if self.ret:
                cv2.putText(self.frame, str(int(self.fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                cv2.imshow("LMAO", self.frame)
                
            
    def map_func(self, func):
        return func()
        
    def start(self):
        self.started = True
        self.cap = cv2.VideoCapture(0)
        while True:
            self.update()
            self.show_frame()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
        
    
def fmap(func):
    return func()

if __name__ == "__main__":
    cam = CameraFeed()

