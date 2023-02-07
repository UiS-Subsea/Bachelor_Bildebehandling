import unittest
import cv2
from find_center_of_red import find_center_of_red

class Test_find_center_of_red(unittest.TestCase):
    def test_find_center_1(self):
        img = cv2.imread("autonomous_docking/images/dockingstation_stop.png")
        center, radius = find_center_of_red(img)
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)

    def test_find_center_2(self):
        img = cv2.imread("autonomous_docking/images/dockingstation_stop2.png")
        center, radius = find_center_of_red(img)
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)

    def test_find_center_3(self):
        img = cv2.imread("autonomous_docking/images/dockingstation_stop3.png")
        center, radius = find_center_of_red(img)
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)

    def test_find_center_3(self):
        img = cv2.imread("autonomous_docking/images/dockingstation_stop3.png")
        center, radius = find_center_of_red(img)
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)



if __name__ == "__main__":
    t = Test_find_center_of_red()
    unittest.main() #runs the test


    