import cv2
import multiprocessing

class CameraFeed:
    def __init__(self, gstreamer = False, port=5000):
        self.port = port
        if gstreamer:
            gst_feed = f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port={self.port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
        else:
            self.cap = cv2.VideoCapture(0)
            
        self.started = False
        self.grabbed, self.frame = self.cap.read()
        
    def update(self, lock):
        while self.started:
            lock.acquire()
            self.grabbed, self.frame = self.cap.read()
            lock.release()
            
    def show_frame(self, lock):
        while self.started:
            lock.acquire()
            cv2.imshow(f"{self.port}", self.frame)
            lock.release()
            
    def read(self):
        return self.grabbed, self.frame
    
    def key_commands(self, lock):
        while self.started:
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(f"camerafeed//output//img{self.port}.jpg", self.frame)
            elif key == ord('q'):
                self.started = False
                del self
                break
            
    def start(self):
        self.started = True
        self.start_processes()
        
        
    def start_processes(self):
        lock = multiprocessing.Lock()
        process1 = multiprocessing.Process(target=self.update, args=(lock,))
        process2 = multiprocessing.Process(target=self.show_frame, args=(lock,))
        process3 = multiprocessing.Process(target=self.key_commands, args=(lock,))
        process1.start()
        process2.start()
        process3.start()
        process1.join()
        process2.join()
        process3.join()
        
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
        
    

    

if __name__ == "__main__":
    cam = CameraFeed(gstreamer=False)
    cam.start()