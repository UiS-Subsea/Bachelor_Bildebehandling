import unittest
from autonomus_transect_manuver import *

class Test_autonomus_transect_manuver(unittest.TestCase):
    def test_go_forward(self):
        manuver_command = autonomus_transect_manuver("autonomus_handling/transect_straight.png")
        self.assertEqual(manuver_command[0], "GO FORWARD")
        self.assertLess(manuver_command[1], 1)
        self.assertGreater(manuver_command[1], -1)

    def test_go_left(self):
        manuver_command = autonomus_transect_manuver("autonomus_handling/transect_to_left.png")
        self.assertEqual(manuver_command[0], "SWING LEFT")
        self.assertLessEqual(manuver_command[1], -1)

    def test_go_right(self):
        manuver_command = autonomus_transect_manuver("autonomus_handling/transect_to_right.png")
        self.assertEqual(manuver_command[0], "SWING RIGHT")
        self.assertGreaterEqual(manuver_command[1], 1)



if __name__ == "__main__":
    t = Test_autonomus_transect_manuver()
    unittest.main()


