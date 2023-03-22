import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the images
def triangulate_real(mtx1,mtx2,R,T):
    img1 = cv2.imread('3d_testing/Test_Images/Skull1.jpg')
    img2 = cv2.imread('3d_testing/Test_Images/Skull2.jpg')
    img3 = cv2.imread('3d_testing/Test_Images/Skull3.jpg')
    img4 = cv2.imread('3d_testing/Test_Images/Skull4.jpg')

    # Convert the images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    gray4 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)

    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors in each image
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    kp3, des3 = sift.detectAndCompute(gray3, None)
    kp4, des4 = sift.detectAndCompute(gray4, None)

    # Create a BFMatcher object
    bf = cv2.BFMatcher()

    # Match the descriptors between each pair of images
    matches12 = bf.knnMatch(des1, des2, k=2)
    matches13 = bf.knnMatch(des1, des3, k=2)
    matches14 = bf.knnMatch(des1, des4, k=2)

    # Apply Lowe's ratio test to filter out bad matches
    good_matches12 = []
    for m,n in matches12:
        if m.distance < 0.75*n.distance:
            good_matches12.append(m)

    good_matches13 = []
    for m,n in matches13:
        if m.distance < 0.75*n.distance:
            good_matches13.append(m)

    good_matches14 = []
    for m,n in matches14:
        if m.distance < 0.75*n.distance:
            good_matches14.append(m)

    # Extract the matched keypoints in each pair of images
    pts1_2 = np.float32([kp1[m.queryIdx].pt for m in good_matches12]).reshape(-1, 1, 2)
    pts2_2 = np.float32([kp2[m.trainIdx].pt for m in good_matches12]).reshape(-1, 1, 2)

    pts1_3 = np.float32([kp1[m.queryIdx].pt for m in good_matches13]).reshape(-1, 1, 2)
    pts3_3 = np.float32([kp3[m.trainIdx].pt for m in good_matches13]).reshape(-1, 1, 2)

    pts1_4 = np.float32([kp1[m.queryIdx].pt for m in good_matches14]).reshape(-1, 1, 2)
    pts4_4 = np.float32([kp4[m.trainIdx].pt for m in good_matches14]).reshape(-1, 1, 2)

    points_3d = cv2.triangulatePoints(mtx1, mtx2, pts1_2, pts2_2)

    points_3d_homogeneous = np.hstack((points_3d, np.ones((points_3d.shape[0], 1))))
    points_3d_normalized = cv2.convertPointsFromHomogeneous(points_3d_homogeneous.T).reshape(-1, 3)

    # Convert the 3D points to homogeneous coordinates and normalize
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.scatter3D(points_3d_normalized[:, 0], points_3d_normalized[:,1], points_3d_normalized[:, 2], cmap='Greens')
    plt.show()