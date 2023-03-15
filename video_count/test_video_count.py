import unittest
from frog_count_main import count_frogs_main
import cv2

class TestFrogCount(unittest.TestCase):

    def test_video_count_1(self):
        camera_feed = cv2.VideoCapture("video_count/Media/TestVideo1.mp4")
        c = count_frogs_main(camera_feed)
        self.assertEqual(c, 4)

    def test_video_count_2(self):
        camera_feed = cv2.VideoCapture("video_count/Media/TestVideo2.mp4")
        c = count_frogs_main(camera_feed)
        self.assertEqual(c, 7)
    


if __name__ == "__main__":
    unittest.main()