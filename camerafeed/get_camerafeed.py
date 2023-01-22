import cv2  #### pip install opencv-python


class CameraFeed:
    def __init__(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id) # Choose which camera to use

    def get_frame(self):
        ret, frame = self.camera.read() # Ret is a boolean value that returns true if the frame is available, frame is the image
        return frame

    def isOn(self):
        return self.camera.isOpened() # Returns a boolean is true if the camera is available

    def get_frame_gray(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def show_frame(self, frame, window_name="frame"):
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.__del__()
            return False


    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = CameraFeed()
    while cam.isOn():
        while(True):
            frame = cam.get_frame()
            gray_frame = cam.get_frame_gray(frame)
            cam.show_frame(frame, "Normal")
            cam.show_frame(gray_frame, "Gray")
    else:
        print("Camera is not available")



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

