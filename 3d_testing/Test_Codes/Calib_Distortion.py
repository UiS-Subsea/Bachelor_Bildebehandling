import numpy as np
import cv2
import glob

chessBoardSize = (7,7)
frameSize = (640,480)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

object_points =  np.zeros((chessBoardSize[0]*chessBoardSize[1],3), np.float32)
object_points[:,:2] = np.mgrid[0:chessBoardSize[0],0:chessBoardSize[1]].T.reshape(-1,2)

new_object_points = []
imgage_points = []

images = glob.glob("3d_testing//Chess_images//*.jpg")

for image in images:
    img = cv2.imread(image)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessBoardSize,None)
    
    if ret:
        new_object_points.append(object_points)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgage_points.append(corners2) 
        
        cv2.drawChessboardCorners(img, chessBoardSize, corners2, ret)
        cv2.imshow('img',img)
        cv2.waitKey(0)
        
cv2.destroyAllWindows()

ret, camera_matrix, distortion_coeffs, rotation_vector, transformation_vector = cv2.calibrateCamera(new_object_points, imgage_points, gray.shape[::-1],None,None)

np.savez("3d_testing//calibration.npz", mtx=camera_matrix, dist=distortion_coeffs, rvecs=rotation_vector, tvecs=transformation_vector)




# To undistort images

image = cv2.imread("TestImage.jpg")
height, width = image.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (width,height), 1, (width,height))

undistorted = cv2.undistort(image, camera_matrix, distortion_coeffs, None, newCameraMatrix)

x, y, width, height = roi

undistorted = undistorted[y:y+height, x:x+width]

cv2.imwrite("Undistorted.jpg", undistorted)


# undistort with remapping

mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, distortion_coeffs, None, newCameraMatrix, (width,height), 5)
undistorted = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)

x, y, width, height = roi

undistorted = undistorted[y:y+height, x:x+width]
cv2.imwrite("Undistorted2.jpg", undistorted)




# Reprojection error

mean_error = 0

for i in range(len(new_object_points)):
    imgage_points2, _ = cv2.projectPoints(new_object_points[i], rotation_vector[i], transformation_vector[i], camera_matrix, distortion_coeffs)
    error = cv2.norm(imgage_points[i],imgage_points2, cv2.NORM_L2)/len(imgage_points2)
    mean_error += error
    
print("total error: {}".format(mean_error/len(new_object_points)))
