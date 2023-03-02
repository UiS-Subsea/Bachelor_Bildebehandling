import cv2  ####  need to download OpenCV from source with GSTREAMER on, and install it, find tutorial on official opencv website
class CameraFeed:
    def __init__(self, gstreamer= True, multicast_grp=f"244.1.1.1", port=5000):
        if gstreamer:
            # Use GSTREAMER multicast to get the camera feed
            gst_feed = f"-v udpsrc multicast-group={multicast_grp} auto-multicast=true multicast-iface=eth0 port={port} ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"
            self.camera = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER) 
        else:
            # Use the default camera
            self.camera = cv2.VideoCapture(0)

    def start_camera(self):
        # Starts the camera
        print("Hello")
        while self.is_on():
            print("Hmm")
            while(True):
                ret, frame = self.get_frame()
                print("Test")
                if ret:
                    print("Looping")
                    if self.show_frame(frame):
                        self.show_frame(frame)
                    # yield frame
                print("L")
        else:
            print("Alert! Camera not found")
            return 0
                  

    def get_frame(self):
        # Ret is a boolean value that returns true if the frame is available, frame is the image
        ret, frame = self.camera.read() 
        return ret, frame

    def is_on(self):
        # Returns a boolean is true if the camera is available
        return self.camera.isOpened() 

    def save_frame(self, frame, filename):
        cv2.imwrite("camerafeed//Saved_Images//" + filename, frame)

    def show_frame(self, frame, window_name="frame"): 
        # Shows the frame in a window
        # Runs the destructor method if q or 1 is pressed
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            self.__del__()
            return False
        return True

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
    
    cam = CameraFeed(gstreamer = False)      
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

