import cv2
import multiprocessing as mp
import time
import functools

class CameraFeed:
    def __init__(self, gstreamer = True, port=5000):
        self.port = port
        self.started = False
        self.gstreamer = gstreamer
        # self.grabbed, self.frame = self.cap.read()
        
    def run(self):
        self.cap = cv2.VideoCapture(0)
        i = 0
        while self.started:
            grabbed, frame = self.cap.read()
            cv2.imshow("Frame", frame)
            yield frame
        
        
    def update(self):
        while self.started:
            print("Running update")
            # lock.acquire()
            if self.cap.isOpened():
                print("Grabbing frame")
                self.grabbed, self.frame = self.cap.read()
            else:
                print("Camera not opened")
            # lock.release()
        else:
            print("Stopped updating")
            
    def update_test(self):
        while self.started:
            print("Running update")
            # self.grabbed, self.frame = self.cap.read()
            # cv2.waitKey(1)
        
    def show_frame_test(self, frame = None):
        while self.started:
            print("Showing frame")
        # if self.started:
        #     if frame == None:
        #         frame = self.frame
        #     cv2.imshow("Frame", frame)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         self.started = False
        #         del self
        #         return
        
            
    def show_normal(self):
        while True:
            ret, frame = self.cap.read()
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            
    def show_frame(self, frame = None):
        while self.started:
            if frame == None:
                frame = self.frame
            # lock.acquire()
            # print("Showing frame", self.frame)
            cv2.imshow("Frame", frame)
            # lock.release()
            key = cv2.waitKey(1)
            time.sleep(0.1) 
        else:
            print("Stopped showing frame")
            
    def read(self, queue):
        print("Reading frame")
        print(self.cap.isOpened())
        grabbed, frame = self.cap.read()
        queue.put(frame)
        cv2.waitKey(1)
        # return self.grabbed, self.frame
    
    def key_commands(self):
        while self.started:
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(f"camerafeed//output//img{self.port}.jpg", self.frame)
            elif key == ord('q'):
                self.started = False
                del self
                break
        else:
            print("Stopped key commands")
    
    def run_stuff(self, arg):
        if arg == 1:
            return self.update_test()
        elif arg == 2:
            return self.show_frame_test()
        
    def create_pool(self):
        self.pool = mp.Pool(processes=4)
        self.pool.starmap_async(self.run_stuff, [(1,), (2,)])
        
        
    def start_processes(self, test=None):
        update_func = functools.partial(self.update_test)
        show_func = functools.partial(self.show_frame_test)
        
        with mp.Pool(processes=4) as pool:
            _ = pool.map(smap, [show_func, update_func])
            
        
    def start(self):
        self.started = True
        # stuff = self.run()
        self.start_processes()
        
        
        
        
        
   
        
    def __del__(self):
        # self.cap.release()
        cv2.destroyAllWindows()
        
        
    
def smap(f):
    return f()
    

if __name__ == "__main__":
    cam = CameraFeed(gstreamer=False)
    # cam.show_normal()
    cam.start()