import cv2
import numpy as np
import matplotlib as plt

#takes in two images and combines them into one panoramic image, it saves the output as output.jpg
#NEEDS A RETURN
def stich_images(image1, image2): 
    img_1 = cv2.imread(image1)
    img1 = cv2.imread(image1)

    cv2.imshow("img1", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img_2 = cv2.imread(image2)
    img2 = cv2.imread(image2)

    cv2.imshow("img2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray2", gray1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray2", gray2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    img1 = cv2.drawKeypoints(gray1, kp1, img1)
    img2 = cv2.drawKeypoints(gray2, kp2, img2)

    cv2.imshow("keypoints img1", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow("keypoints img2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m in matches:
        if (m[0].distance < 0.5*m[1].distance):
            good.append(m)

    matches = np.asarray(good)

    if (len(matches[0:,0]) >= 4):
        src = np.float32([kp1[m.queryIdx].pt for m in matches[:,0]]).reshape(-1, 1, 2)
        dst = np.float32([kp2[m.trainIdx].pt for m in matches[:,0]]).reshape(-1, 1, 2)

        H, masked = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)

    else:
        raise AssertionError("Cant find enought keypoints.")


    dst = cv2.warpPerspective(img_1, H, ((img_1.shape[1] + img_2.shape[1]), img_2.shape[0])) #wraped image
    dst[0:img_2.shape[0], 0:img_2.shape[1]] = img_2 #stitched image
    cv2.imwrite("output.jpg", dst)
    cv2.imshow("output", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    se = stich_images("output.jpg", "panoramic_froggos/froggos10_slice3.png")


