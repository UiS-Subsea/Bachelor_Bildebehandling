import cv2
import time
import multiprocessing as mp
import functools
import asyncio

global cap
class CameraFeed:
    def __init__(self):
        global cap
        cap = cv2.VideoCapture(0)
        self.started = False
        self.frame = cap.read()[1]
        
    # def init_camera(self):
    #     global cap
    #     cap = cv2.VideoCapture(0)
        
    async def update_loop(self):
        while self.started:
            print("Updating (Loop)")
            self.frame = cap.read()[1]
            cv2.waitKey(1)
            # yield frame
            await asyncio.sleep(0)
        
    async def show_frame_loop(self):
        while self.started:
            print("Showing frame (Loop)")
            cv2.imshow("Frame", self.frame)
            # cv2.waitKey(1)
            await asyncio.sleep(0)
            
    def update(self):
        if self.started:
            print("Updating")
            
    def show_frame(self):
        if self.started:
            print("Showing frame")
            
    def map_func(self, func):
        return func()
        
    def start_update(self):
        p1 = mp.Pool(5)
        p1.apply_async(target=self.update_loop)
        
    def start_show_frame(self):
        p2 = mp.Pool(5)
        p2.apply_async(target=self.show_frame_loop)
        
    async def start(self):
        self.started = True
        await asyncio.gather(self.start_update, self.start_show_frame)
        
async def main():
    cam = CameraFeed()
    await cam.start()
    

if __name__ == "__main__":
    asyncio.run(main())


    