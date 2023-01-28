import unittest
import sys
sys.path.append("..")
from frog_count.frog_count_func import *

class Test_count_frogs(unittest.TestCase):
    def test_froggos(self):
        c = count_frogs("froggos/froggos.jpg")
        self.assertEqual(c, 7)

    def test_froggos2(self):
        c = count_frogs("froggos/froggos2.jpg")
        self.assertEqual(c, 8)

    def test_froggos3(self):
        c = count_frogs("froggos/froggos3.jpg")
        self.assertEqual(c, 6)

    def test_froggos4(self): 
        c = count_frogs("froggos/froggos4.jpg")
        self.assertEqual(c, 8)

    def test_froggos5(self): 
        c = count_frogs("froggos/froggos5.png")
        self.assertEqual(c, 6)

    def test_froggos6(self):
        c = count_frogs("froggos/froggos6.png")
        self.assertEqual(c, 11)

    def test_froggos6(self): #den mest realistiske testen
        c = count_frogs("froggos/froggos7.png")
        self.assertEqual(c, 11)
    


if __name__ == "__main__":
    t = Test_count_frogs()
    unittest.main()
        