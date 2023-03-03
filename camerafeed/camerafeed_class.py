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
        ret, frame = self.cap.read()
        return (ret, frame)
            
    async def show_frame(self):
        cv2.imshow("frame", self.frame)
        
        
    async def __adel__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        

async def update_routine(camerafeed):
    while True:
        ret, frame = camerafeed.cap.read()
        if not ret:
            print("no frame")
            continue
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) == ord("q"):
            break
        await camerafeed.__adel__()
        await asyncio.sleep(0.01)  
    
async def main():
    camera = Camerafeed_Async(gstreamer=False)
    await update_routine(camera)
    
    #
        
if __name__== "__main__":
    asyncio.run(main())