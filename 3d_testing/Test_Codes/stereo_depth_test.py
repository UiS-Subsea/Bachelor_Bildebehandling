import numpy as np
import cv2
from matplotlib import pyplot as plt
import scipy

imgL = cv2.imread('3d_testing//Test_Images//left_cup.jpg',1)
imgR = cv2.imread('3d_testing//Test_Images//right_cup.jpg', 1)

imgL_tranformed = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgR_tranformed = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)


stereo = cv2.StereoBM_create(numDisparities=0, blockSize=5)
disparity = stereo.compute(imgL_tranformed,imgR_tranformed)
plt.imshow(disparity,'gray')
plt.show()

