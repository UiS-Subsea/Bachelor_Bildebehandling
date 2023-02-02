import unittest
from Monitor_seagrass import *

class test_detect_squares(unittest.TestCase):
    def test_squares(self):
        
        squares1 = detect_squares("monitor_seagrass\images\Example1.png")
        squares2 = detect_squares("monitor_seagrass\images\Example2.png")
        self.assertEqual(squares1, 41)
        self.assertEqual(squares2, 37)
    


if __name__ == "__main__":
    t = test_detect_squares()
    unittest.main()
        