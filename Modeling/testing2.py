import os
import matplotlib.pyplot as plt
import cv2
from model_functions import *

image_dir = 'Modeling/Images/'
images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]


for image in images:
    image_path = image_dir + image
    the_image = cv2.imread(image_path)

    print(the_image.shape)
    resized_img = cv2.resize(the_image, (720, 960))
    
    

