import unittest
import cv2
from supporting_functions import *

class Test_get_center_of_frame(unittest.TestCase):
    def test_get_center720p(self):
        img720p = cv2.imread("autonomous_docking/images/docking_720p.png")
        center_coord = get_center_of_frame(img720p)
        self.assertEqual(center_coord, (640, 360))

    def test_get_center1080p(self):
        img1080p = cv2.imread("autonomous_docking/images/docking_1080p.png")
        center_coord = get_center_of_frame(img1080p)
        self.assertEqual(center_coord, (960, 540))



class Test_differance_between_centers(unittest.TestCase):
    def test_diff_centers_1(self):
        frame_center = (500, 500)
        red_center = (1000, 1000)
        diff_centers = differance_between_centers(frame_center, red_center)
        self.assertEqual(diff_centers, (500, -500))

    def test_diff_centers_2(self):
        frame_center = (500, 500)
        red_center = (100, 100)
        diff_centers = differance_between_centers(frame_center, red_center)
        self.assertEqual(diff_centers, (-400, 400))

    def test_diff_centers_3(self):
        frame_center = (500, 500)
        red_center = (100, 900)
        diff_centers = differance_between_centers(frame_center, red_center)
        self.assertEqual(diff_centers, (-400, -400))

    def test_diff_centers_4(self):
        frame_center = (500, 500)
        red_center = (900, 100)
        diff_centers = differance_between_centers(frame_center, red_center)
        self.assertEqual(diff_centers, (400, 400))



class Test_red_frame_area_percentage(unittest.TestCase):
    def test_red_frame_area_percent_1(self):
        frame_width = 10
        frame_height = 10
        radius = 5
        percent_diff = red_frame_area_percentage(radius, frame_width, frame_height)
        self.assertEqual(percent_diff, 78.54)

    def test_red_frame_area_percent_2(self):
        frame_width = 1920
        frame_height = 1080
        radius = 500
        percent_diff = red_frame_area_percentage(radius, frame_width, frame_height)
        self.assertEqual(percent_diff, 37.876)



class Test_regulate_position(unittest.TestCase):
    def test_go_left(self):
        drive_command = regulate_position(100, 0)
        self.assertAlmostEqual(drive_command, "GO LEFT")

    def test_go_right(self):
        drive_command = regulate_position(-100, 0)
        self.assertEqual(drive_command, "GO RIGHT")

    def test_go_down(self):
        drive_command = regulate_position(0, 100)
        self.assertEqual(drive_command, "GO DOWN")

    def test_go_up(self):
        drive_command = regulate_position(0, -100)
        self.assertEqual(drive_command, "GO UP")




if __name__ == "__main__":
    t = Test_get_center_of_frame()
    unittest.main()