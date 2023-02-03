import unittest
from find_center_of_red import find_center_of_red

class Test_find_center_of_red(unittest.TestCase):
    def find_center_1(self):
        center, radius = find_center_of_red("autonomous_docking/images/dockingstation_stop.png")
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)

    def find_center_2(self):
        center, radius = find_center_of_red("autonomous_docking/images/dockingstation_stop2.png")
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)

    def find_center_3(self):
        center, radius = find_center_of_red("autonomous_docking/images/dockingstation_stop3.png")
        self.assertEqual(center, (954, 536))
        self.assertEqual(radius, 586)



if __name__ == "__main__":
    t = Test_find_center_of_red()
    unittest.main() #runs the test


    