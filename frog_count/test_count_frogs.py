import unittest
from frog_count_func import *

class Test_count_frogs(unittest.TestCase):
    def test_froggos(self):
        c = count_frogs("frog_count/froggos/froggos.jpg")
        self.assertEqual(c, 7)

    def test_froggos2(self):
        c = count_frogs("frog_count/froggos/froggos2.jpg")
        self.assertEqual(c, 8)

    def test_froggos3(self):
        c = count_frogs("frog_count/froggos/froggos3.jpg")
        self.assertEqual(c, 6)

    def test_froggos4(self): 
        c = count_frogs("frog_count/froggos/froggos4.jpg")
        self.assertEqual(c, 8)

    def test_froggos5(self): 
        c = count_frogs("frog_count/froggos/froggos5.png")
        self.assertEqual(c, 6)

    def test_froggos6(self):
        c = count_frogs("frog_count/froggos/froggos6.png")
        self.assertEqual(c, 11)

    def test_froggos7(self): #den vanskeligste testen, grunnet veldig høy oppløsning
        c = count_frogs("frog_count/froggos/froggos7.png")
        self.assertEqual(c, 9)

    def test_froggos8(self): #den mest realistiske testen
        c = count_frogs("frog_count/froggos/froggos8.png")
        self.assertEqual(c, 9)

    def test_froggos9(self): #den mest realistiske testen
        c = count_frogs("frog_count/froggos/froggos9.png")
        self.assertEqual(c, 3)
    
    def test_froggos10(self): #den mest realistiske testen
        c = count_frogs("frog_count/froggos/vann1.jpg")
        print("Test 10: ", c)
        self.assertEqual(c, 2)
        
    def test_froggos11(self): #den mest realistiske testen
        c = count_frogs("frog_count/froggos/vann2.jpg")
        print("Test 11: ", c)
        self.assertEqual(c, 3)

    def test_froggos12(self): #den mest realistiske testen
        c = count_frogs("frog_count/froggos/vann3.jpg")
        print("Test 12: ", c)
        self.assertEqual(c, 3)

    def test_froggos13(self): #den mest realistiske testen
        c = count_frogs("frog_count/froggos/vann4.jpg")
        print("Test 13: ", c)
        self.assertEqual(c, 3)



if __name__ == "__main__":
    t = Test_count_frogs()
    unittest.main()
        