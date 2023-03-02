import asyncio
import cv2
from async_class import AsyncClass, AsyncObject, task, link

# cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

class Camerafeed_Async(AsyncClass):
    def __init__(self, gstreamer=True, port=5000):
        if gstreamer:
            # gst_feed = f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true multicast-iface=eth0 port={port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            # self.cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
            pass
        elif not gstreamer:
            self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.ret = None
        self.running = True
        # self.task = asyncio.create_task(self.update())
        
    async def update(self):
        self.ret, self.frame = self.cap.read()
            
    async def show_frame(self):
        cv2.imshow("frame", self.frame)
        
        
    async def __adel__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        

async def update_routine(camerafeed):
    await camerafeed.update()
    # print(camerafeed.ret)
    # asyncio.sleep(1)
    print("Update Routine Done")
    
async def show_routine(camerafeed):
    await camerafeed.show_frame()
    # asyncio.sleep(2)
    print("Show Routine Done")

async def main():
    camera = Camerafeed_Async(gstreamer=False)
    # tasks = [update_routine(camera), show_routine(camera)]
    # while True:
    #     await asyncio.gather(*tasks)
    event_loop = asyncio.get_event_loop()
    
    event_loop.create_task(update_routine(camera))
    event_loop.run_forever()
    
    
    #
        
if __name__== "__main__":
    asyncio.run(main())