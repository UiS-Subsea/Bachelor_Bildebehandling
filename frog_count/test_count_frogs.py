import unittest
from count_frogs import *

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

    def test_froggos4(self): #nest vanskeligste testen
        c = count_frogs("froggos/froggos4.jpg")
        self.assertEqual(c, 8)

    def test_froggos5(self): #vanskeligste testen
        c = count_frogs("froggos/froggos5.png")
        self.assertEqual(c, 6)
    




if __name__ == "__main__":
    t = Test_count_frogs()
    unittest.main()
        