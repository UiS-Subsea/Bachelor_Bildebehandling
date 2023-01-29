from PIL import Image
import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt


def convert_color(img_path):
    with Image.open(img_path) as img:
        
        size_x, size_y = img.size
        px = img.load()

        for x in range(size_x):
            for y in range(size_y):
                if is_black(px[x, y]):
                    img.putpixel((x, y), (154,217,234)) # Blue pixel
        return img
                    
def is_black(px):
    if px[0] < 50 and px[1] < 50 and px[2] < 50:
        return True
    return False


if __name__ == "__main__":
    picture = convert_color("output.jpg")
    picture.show()