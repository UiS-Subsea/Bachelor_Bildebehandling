import bpy
import os
import matplotlib.pyplot as plt

image_dir = 'Modeling/Images/'
images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]


img = plt.imread("Modeling/Images/Glass1.jpg")
print(os.getcwd())
plt.imshow(img)
plt.show()