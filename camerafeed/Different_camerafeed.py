from Other_Classes.autonomous_transect_main import AutonomousTransect
from Other_Classes.grass_monitor_main import SeagrassMonitor
import cv2
import multiprocessing as mp
class Camera:
    def __init__(self) -> None:
        self.cam = cv2.VideoCapture(0)
        self.frame = None
        
    def get_frame(self):
        while True:
            print("Getting frame")
            cv2.waitKey(20)

            # success, self.frame = self.cam.read()
        # return self.frame
    
    
class ExecutionClass:
    def __init__(self):
        self.AutonomousTransect = AutonomousTransect()
        
    def run(self, frame):
        while True:
            print("Running execution class")
            cv2.waitKey(20)
            self.frame = frame
            


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
    cam = Camera()
    Executor = ExecutionClass()
    
    run_processes(5, cam.get_frame, Executor.run(cam.frame))
    