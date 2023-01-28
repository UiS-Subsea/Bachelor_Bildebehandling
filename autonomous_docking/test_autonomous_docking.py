import unittest
from autonomous_docking import autonomous_docking

class Test_docking_red_center_allign(unittest.TestCase):
    def test_move_forward(self):
        dock_command = autonomous_docking("autonomous_docking\images\move_forward_480.png")
        self.assertEqual(dock_command, "MOVE FORWARD")

    def test_auto_stop_rov(self):
        dock_command = autonomous_docking("autonomous_docking\images\dockingstation480_close.png")
        self.assertEqual(dock_command, "STOP ROV")

    def test_allign_centers(self):
        dock_command = autonomous_docking("autonomous_docking\images\dockingstation480.png")
        self.assertEqual((-105, -36), dock_command)



if __name__ == "__main__":
    t = Test_docking_red_center_allign()
    unittest.main() #runs the test


    