import cv2
import numpy as np
from matplotlib import pyplot as plt
import pyvista as pv


img1 = cv2.imread('3d_testing//Test_Images//cup3_1.jpg')
img2 = cv2.imread('3d_testing//Test_Images//cup3_2.jpg')
img3 = cv2.imread('3d_testing//Test_Images//cup3_3.jpg')

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
kp3, des3 = sift.detectAndCompute(img3,None)

# Match the keypoints between images 1 and 2
bf = cv2.BFMatcher()
matches12 = bf.knnMatch(des1, des2, k=2)

# Apply Lowe's ratio test to filter the matches
good_matches12 = []
for m, n in matches12:
    if m.distance < 0.75 * n.distance:
        good_matches12.append(m)

# Convert the matched keypoints to numpy arrays
pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches12]).reshape(-1, 1, 2)
pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches12]).reshape(-1, 1, 2)

# Estimate the essential matrix using RANSAC
E, mask12 = cv2.findEssentialMat(pts1, pts2, method=cv2.RANSAC, prob=0.999, threshold=1.0)

# Recover the relative pose between images 1 and 2
_, R12, t12, mask12 = cv2.recoverPose(E, pts1, pts2)

# Match the keypoints between images 2 and 3
matches23 = bf.knnMatch(des2, des3, k=2)

# Apply Lowe's ratio test to filter the matches
good_matches23 = []
for m, n in matches23:
    if m.distance < 0.75 * n.distance:
        good_matches23.append(m)

# Convert the matched keypoints to numpy arrays
pts2 = np.float32([kp2[m.queryIdx].pt for m in good_matches23]).reshape(-1, 1, 2)
pts3 = np.float32([kp3[m.trainIdx].pt for m in good_matches23]).reshape(-1, 1, 2)

# Estimate the essential matrix using RANSAC
E, mask23 = cv2.findEssentialMat(pts2, pts3, method=cv2.RANSAC, prob=0.999, threshold=1.0)

# Recover the relative pose between images 2 and 3
_, R23, t23, mask23 = cv2.recoverPose(E, pts2, pts3)

# Compute the projection matrix for image 1
K = np.array([[5, 0, 5], [0, 5, 5], [0, 0, 1]])
P1 = K.dot(np.hstack((np.eye(3), np.zeros((3, 1)))))
R1 = np.eye(3)
t1 = np.zeros((3, 1))
P2 = K.dot(np.hstack((R12, t12)))

points4D = cv2.triangulatePoints(P1, P2, pts1, pts2)
points3D = cv2.convertPointsFromHomogeneous(points4D.T).reshape(-1, 3)

# Step 5: Create a 3D mesh or point cloud from the triangulated points.
# Convert the 3D points to a numpy array

points = np.squeeze(points3D)
# Save the points to a file

np.savetxt('points.txt', points)
# Alternatively, create a point cloud visualization using a library such as PyVista

# Create a PyVista point cloud from the 3D points

cloud = pv.PolyData(points)
# Visualize the point cloud

cloud.plot()