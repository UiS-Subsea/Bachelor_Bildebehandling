import cv2
import numpy as np
from matplotlib import pyplot as plt


def color_correct(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def process(img):
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    plt.imshow(thresh)
    plt.show()
    
def triangulate(mtx1,mtx2,R,T):
    img1 = cv2.imread("3d_testing/Target_Images/Cam1_2.jpg")
    img2 = cv2.imread("3d_testing/Target_Images/Cam2_2.jpg")
   
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    gray1 = cv2.equalizeHist(gray1)
    gray2 = cv2.equalizeHist(gray2)
    
    # cv2.imshow("After hist equalize", gray1)
    # cv2.imshow("After hist equalize 2", gray2)
    # cv2.waitKey(0)
    
    gray1 = cv2.GaussianBlur(gray1, (5, 5), 0)
    gray2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    
    process(color_correct(gray1))
    plt.imshow(color_correct(gray1))
    plt.show()
    
    # cv2.imshow("After Gaussian Blur", gray1)
    # cv2.imshow("After Gaussian Blur 2", gray2)
    # cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    sift = cv2.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # print("No of keypoints on img1: ", len(kp1))
    # print("No of keypoints on img2: ", len(kp2))
    # print("kp1 type:", type(kp1), "values: ", kp1)
    # print("BIG TEST VALUE: ", kp1[0].pt)
    bf = cv2.BFMatcher()
    
    matches = bf.knnMatch(des1, des2, k=3)
    print("Matches: ", len(matches))
    good_matches = []
    for m,n, _ in matches:
        if m.distance < 0.85*n.distance:
            # print("This is m: ", m," This is n: ", n)
            # print("The query index is: ", m.queryIdx)
            good_matches.append(m)
    img_matches = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches[:], None)
    resized = cv2.resize(img_matches, (1280, 480))
    plt.imshow(resized)
    plt.show()
    
    # cv2.destroyAllWindows()
    print("Good matches: ", len(good_matches))
    # test = [print("This is m in good matches type: ", type(m), "and the idx is: ", m.queryIdx) for m in good_matches]
    key_points_query = [kp1[m.queryIdx].pt for m in good_matches]
    key_points_train = [kp2[m.trainIdx].pt for m in good_matches]
    
    # print("Query mtx1: ", mtx1.shape)
    # print("Train mtx2: ", mtx2.shape)
    # print(mtx1)
    # print(mtx2)
    pts1_2 = np.float32(key_points_query).reshape(-1, 1, 2)
    pts2_2 = np.float32(key_points_train).reshape(-1, 1, 2)
    # print(key_points1)
    # pts1_2 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    # pts2_2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    mtx1_extrinsic = np.hstack((mtx1, T)) # Adds the translation vector to the camera matrix
    mtx2_extrinsic = np.hstack((mtx2, T)) # Adds the translation vector to the camera matrix
    points_3d = cv2.triangulatePoints(mtx1_extrinsic, mtx2_extrinsic, pts1_2, pts2_2)
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
