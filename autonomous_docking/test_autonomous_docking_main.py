import unittest
import cv2
from autonomous_docking_main import *

class test_autonomous_docking(unittest.TestCase):
    def test_autonomous_docking_go_left(self):
        test_frame = cv2.imread("autonomous_docking/images/pool_test1.png")
        docking_command = autonomous_docking(test_frame)
        self.assertEqual(docking_command, "GO LEFT")

    def test_autonomous_docking_go_right(self):
        test_frame = cv2.imread("autonomous_docking/images/pool_test2.png")
        docking_command = autonomous_docking(test_frame)
        self.assertEqual(docking_command, "GO RIGHT")

    def test_autonomous_docking_go_down(self):
        test_frame = cv2.imread("autonomous_docking/images/pool_test3.png")
        docking_command = autonomous_docking(test_frame)
        self.assertEqual(docking_command, "GO DOWN")






if __name__ == "__main__":
    t = test_autonomous_docking()
    unittest.main()
