import asyncio
import cv2

class CamerafeedAsync:
    def __init__(self, gstreamer = False, port = 5000):
        self.port = port
        if gstreamer:
            gst_feed = f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port={self.port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
        else:
            self.cap = cv2.VideoCapture(0)
            
        self.started = False
        self.grabbed, self.frame = self.cap.read()
    
    # Task to update the frame
    async def update(self):
        print(self.cap)
        while self.started:
            self.grabbed, self.frame = self.cap.read()
            await asyncio.sleep(0)
            
    # Task to show the frame
    async def show_frame(self, name):
        while self.started:
            cv2.imshow(name, self.frame)
            await asyncio.sleep(0)
    
    # Returns frame if needed (Not used)
    def read(self):
        return self.grabbed, self.frame
    
    # Task to handle key commands
    # press 'q' to quit
    # press 's' to save the frame
    async def key_commands(self):
        while self.started:
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(f"camerafeed//output//img{self.port}.jpg", self.frame)
            elif key == ord('q'):
                self.started = False
                del self
                break
            await asyncio.sleep(0)
        
    # Start running the camerafeed and collects tasks
    async def start(self):
        self.started = True
        # Add more tasks here if needed
        # Task template:
        #   async def task_name(self):
        #       while self.started:
        #           Do stuff
        #           await asyncio.sleep(0)
        
        await self.do_tasks(self.update(), self.show_frame(f"{self.port}"), self.key_commands())
        
    # Run the tasks asynchronously
    async def do_tasks(self, *tasks):
        the_tasks = []
        for task in tasks:
            the_tasks.append(task)
        await asyncio.gather(*the_tasks)
              
    # Destructor, Stops the camerafeed
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
# Main function to run the camerafeed

async def do_tasks(*tasks):
    the_tasks = []
    for task in tasks:
        the_tasks.append(task)
    await asyncio.gather(*the_tasks)
        
        
async def main(show_both = False):
    cam = CamerafeedAsync(gstreamer=False, port=5000)
    if show_both:
        cam2 = CamerafeedAsync(gstreamer=True, port=5001)
        await do_tasks(cam.start(), cam2.start())   
    else:
        await cam.start()
        
if __name__ == "__main__":
    asyncio.run(main())