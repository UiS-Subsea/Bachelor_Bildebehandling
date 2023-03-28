from Other_Classes.autonomous_transect_main import AutonomousTransect
from Other_Classes.grass_monitor_main import SeagrassMonitor
from Other_Classes.autonomous_docking_main import find_center_of_red
import cv2
import multiprocessing as mp

class Camera:
    def __init__(self) -> None:
        self.cam = cv2.VideoCapture(0)
        
    def get_frame(self):
        success, frame = self.cam.read()
        return frame
    
    
class ExecutionClass:
    def __init__(self):
        self.AutonomousTransect = AutonomousTransect()
        
    def show(self, frame, name = "frame"):
        cv2.imshow(name, frame)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            exit()
            
    def transect(self, frame):
        transect_frame, driving_data_packet = self.AutonomousTransect.run(frame.copy())
        self.show(transect_frame, "Transect")
        return driving_data_packet
            
    def seagrass(self, frame):
        seagrass_frame = self.seagrass.run(frame.copy())
        self.show(seagrass_frame, "Seagrass")

if __name__ == "__main__":
    cam = Camera()
    execution = ExecutionClass()
    
    while True:
        frame = cam.get_frame()
        execution.show(frame)
        execution.transect(frame)