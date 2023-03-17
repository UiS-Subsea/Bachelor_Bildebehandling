import cv2
import multiprocessing as mp
from Other_Classes.autonomous_transect_main import AutonomousTransect

class CameraFeed:
    def __init__(self, cam_name="Cam1", gstreamer=False, port=5000, mode = None):
        self.name = cam_name
        self.started = False
        self.gstreamer = gstreamer
        self.port = port
        self.frame = None
        self.mode = mode
        self.timer = cv2.getTickCount()
        self.recording = False
        self.Transect = AutonomousTransect()
                
    # Function for returning frame
    def get_frame(self):
        return self.frame
        
    # Function for updating frame
    def update(self):
        if self.started:
            # print("Updating")
            self.ret, self.frame = self.cap.read()
            if self.recording:
                self.videoresult.write(self.frame)
                
            self.fps = cv2.getTickFrequency()/(cv2.getTickCount()-self.timer)
            self.timer = cv2.getTickCount()
            
    # Function for showing frame
    def show_frame(self):
        if self.started:
            # print("Showing frame")
            if self.ret:
                resized = cv2.resize(self.frame, (640, 480))
                cv2.putText(resized, str(int(self.fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                cv2.imshow(self.name, resized)
                
        
    def start(self):
        self.started = True
        # Checks for gstreamer
        if self.gstreamer:
            gst_feed = f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port={self.port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
        else:   
            self.cap = cv2.VideoCapture(0)
        # Sets up a video writer if we need to record
        self.videoresult = cv2.VideoWriter(f'{self.name}.avi', cv2.VideoWriter_fourcc(*'MJPG'),30, (int(self.cap.get(3)), int(self.cap.get(4))))
        # Starts the camera
        while self.started:
            # Updates the frames and shows them
            self.update()
            self.show_frame()
            
            if self.mode == "Docking":
                # Docking code here
                # Docking = DockingClass()
                # Docking.update(self.frame)
                pass
            elif self.mode == "Transect":
                # Transect code here
                self.Transect.update(self.frame)
            else:
                pass
            key = cv2.waitKey(1)
            # Press Q to exit camera
            if key == ord("q"):
                self.started = False
                break
            # Press S to save a frame as image
            elif key == ord("s"):
                cv2.imwrite("test.jpg", self.frame)
            # Press R to start recording
            elif key == ord("r"):
                self.recording = not self.recording
                print(f"Recording" + self.name)
            # press T to stop recording
            elif key == ord("t"):
                print("Stopped recording" + self.name)
                self.videoresult.release()
            elif key == ord("1"):
                print("Switching to Transect")
                if self.mode == "Transect":
                    self.mode = None
                else:
                    self.mode = "Transect"
                
    
# function to send other functions as parameters for processes
def fmap(func):
    return func()

def run_processes(cpu_count, *args):
    # unpacks the processes into a list
    processes = []
    for arg in args:
        processes.append(arg)
        
    # runs the processes with the cpu count as the number of processes
    with mp.Pool(cpu_count) as p:
        p.map(fmap, processes)
        
if __name__ == "__main__":
    # cam = CameraFeed("Cam1", gstreamer=True, port=5000)
    cam = CameraFeed("Cam1", gstreamer=False)
    # cam2 = CameraFeed("Cam2", gstreamer=True, port=5001)

    # put more processes here, 5 is the cpu count, everything after will be a process
    run_processes(5, cam.start)

