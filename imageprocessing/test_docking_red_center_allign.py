import unittest
from docking_red_center_allign import docking_red_center_allign

class Test_docking_red_center_allign(unittest.TestCase):
    def test_move_forward(self):
        dock_command = docking_red_center_allign("imageprocessing\images\move_forward_720.png")
        self.assertEqual(dock_command, "MOVE FORWARD")

    def test_auto_stop_rov(self):
        dock_command = docking_red_center_allign("imageprocessing\images\dockingstation720_close.png")
        self.assertEqual(dock_command, "STOP ROV")

    def test_allign_centers(self):
        dock_command = docking_red_center_allign("imageprocessing\images\dockingstation720.png")
        self.assertEqual((-105, -36), dock_command)



if __name__ == "__main__":
    t = Test_docking_red_center_allign()
    unittest.main() #runs the test