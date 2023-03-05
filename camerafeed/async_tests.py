import asyncio
import cv2

class CamerafeedAsync:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.started = False
        self.frame, self.grabbed = self.cap.read()
    
    async def update(self):
        while self.started:
            self.grabbed, self.frame = self.cap.read()
            await asyncio.sleep(0)
            
    async def show_frame(self):
        while self.started:
            cv2.imshow("frame", self.frame)
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
        
        
async def main():
    cam = CamerafeedAsync()
    await cam.start()
        
if __name__ == "__main__":
    asyncio.run(main())