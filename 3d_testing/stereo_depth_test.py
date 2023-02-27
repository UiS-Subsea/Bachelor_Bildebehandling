import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('3d_testing//Test_Images//left_cup.jpg',1)
imgR = cv2.imread('3d_testing//Test_Images//right_cup.jpg', 1)

imgL_tranformed = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
imgR_tranformed = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

imgL_tranformed = cv2.Canny(imgL_tranformed, 70, 270, 13)
imgR_tranformed = cv2.Canny(imgR_tranformed, 70, 270, 13)
plt.imshow(imgL_tranformed,'gray')
plt.show()
plt.imshow(imgR_tranformed,'gray')
plt.show()

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL_tranformed,imgR_tranformed)
plt.imshow(disparity,'gray')
plt.show()