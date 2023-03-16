import cv2  ####  need to download OpenCV from source with GSTREAMER on, and install it, find tutorial on official opencv website
import time


class CameraFeed:
    def __init__(self, gstreamer= True, multicast_grp=f"244.1.1.1", port=5000):
        if gstreamer:
            # Use GSTREAMER multicast to get the camera feed
            gst_feed= f"-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port={port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.camera = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER) 
        else:
            # Use the default camera
            self.camera = cv2.VideoCapture(0)
        self.prev_time = 0

    def start_camera(self):
        # Starts the camera
        while(True):
            self.update_frame()
            if self.ret:
                cv2.putText(self.frame, str(int(self.fps)), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                cv2.imshow("Frame", self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):  
                    del self
                    break
            
                  

    def update_frame(self):
        # Ret is a boolean value that returns true if the frame is available, frame is the image
        self.ret, self.frame = self.camera.read() 
        self.new_time = time.time()
        self.fps = 1 / (self.new_time - self.prev_time)
        self.prev_time = self.new_time

    def is_on(self):
        # Returns a boolean is true if the camera is available
        return self.camera.isOpened() 

    def save_frame(self, frame, filename):
        cv2.imwrite("camerafeed//Saved_Images//" + filename, frame)


    def __del__(self): 
        # Destructor
        # Exits camera and all cv2 windows
        self.camera.release() 
        cv2.destroyAllWindows() 


def frame_to_gray(frame):
    # Turns frame to grayscale
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

if __name__ == "__main__":
    # Creates a camera object
    
    cam = CameraFeed(gstreamer = True)      
    cam.start_camera()           
    print("Break Point")
              



# vid = cv2.VideoCapture(0)

# while(vid.isOpened()):
#     while(True):
#         ret, frame = vid.read()

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         cv2.imshow('frame', frame)
#         cv2.imshow('gray', gray)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     vid.release()
#     cv2.destroyAllWindows()
# else:
#     print("Alert! Camera not found")

