from Other_Classes.autonomous_transect_main import AutonomousTransect
from Other_Classes.grass_monitor_main import SeagrassMonitor

class ExecutionClass:
    def __init__(self):
        self.AutonomousTransect = AutonomousTransect()
        
    def run(self, frame):
        while True:
            print("Running execution class")
            self.frame = frame