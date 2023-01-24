import cv2  #### pip install opencv-python

class CameraFeed:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id) # Choose which camera to use

    def get_frame(self):
        ret, frame = self.camera.read() # Ret is a boolean value that returns true if the frame is available, frame is the image
        return frame

    def is_on(self):
        return self.camera.isOpened() # Returns a boolean is true if the camera is available

    def save_frame(self, frame, filename):
        cv2.imwrite(filename, frame)

    def show_frame(self, frame, window_name="frame"): # Shows the frame in a window
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Runs the destructor method if q or 1 is pressed
            self.__del__()
            return False

    def __del__(self): # Destructor
        self.camera.release() # Exits camera
        cv2.destroyAllWindows() # Exits all cv2 windows


def frame_to_gray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Turns frame to grayscale

if __name__ == "__main__":
    cam = CameraFeed()                                      # Creates a camera object
    while cam.is_on():                                      # Only run if a camera is available
        while(True):                                        # Run until q or 1 is pressed
            frame = cam.get_frame()                         # Gets the frame
            gray_frame = frame_to_gray(frame)               # Turns the frame to grayscale
            cam.show_frame(frame, "Normal")                 # Shows the frame
            cam.show_frame(gray_frame, "Gray")              # Shows the grayscale frame
    else:
        print("Camera is not available")                    # Prints if no camera is available



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

