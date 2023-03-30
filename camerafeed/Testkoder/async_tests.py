import asyncio
import cv2
import time
class CamerafeedAsync:
    def __init__(self,name="Cam1", gstreamer=False, port=5000) -> None:
        self.name = name
        if gstreamer:
            gst_feed = f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port={port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
        else:
            self.cap = cv2.VideoCapture(0)
        self.started = False
        self.frame, self.grabbed = self.cap.read()
        self.prev_time = 0
    
    async def update(self):
        while self.started:
            self.grabbed, self.frame = self.cap.read()
            self.new_time = time.time()
            self.fps = 1/(self.new_time - self.prev_time)
            self.prev_time = self.new_time
            await asyncio.sleep(0)
            
    async def show_frame(self):
        while self.started:
            cv2.putText(self.frame, str(int(self.fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            if self.name != "Cam1":
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow(self.name, self.frame)
            await asyncio.sleep(0)
            
    def read(self):
        return self.grabbed, self.frame
    
    async def key_commands(self):
        while self.started:
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite("camerafeed//output//img3.jpg", self.frame)
            elif key == ord('q'):
                self.started = False
                del self
                break
            await asyncio.sleep(0)
        
    async def start(self):
        self.started = True
        # tasks = [self.update(), self.show_frame(), self.key_commands()]
        # await asyncio.gather(*tasks)
        await self.do_tasks(self.update(), self.show_frame(), self.key_commands())
        
    async def do_tasks(self, *tasks):
        the_tasks = []
        for task in tasks:
            the_tasks.append(task)
        await asyncio.gather(*the_tasks)
              
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
        
async def do_tasks(*tasks):
    the_tasks = []
    for task in tasks:
        the_tasks.append(task)
    await asyncio.gather(*the_tasks)


async def main(show_both = False):
    cam = CamerafeedAsync(name="Cam1", gstreamer=True, port=5000)
    if show_both:
        cam2 = CamerafeedAsync(name="Cam2", gstreamer=True, port=5001)
        await do_tasks(cam.start(), cam2.start())   
    else:
        await cam.start()
        
if __name__ == "__main__":
    asyncio.run(main())