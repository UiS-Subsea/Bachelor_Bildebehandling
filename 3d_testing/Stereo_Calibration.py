import cv2
import numpy as np
import glob

def calibrate_camera(image_folder):
    image_names = glob.glob("3d_testing//Real_Images")
    image_list = []
    
    for img_name in image_names:
        img = cv2.imread(img_name)
        image_list.append(img)
        
    criteria = (cv2.TERM_CRITERIA_EPS, + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    rows = 8
    cols = 8
    
    objp = np.zeros((rows*cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)
    
    height, width = image_list[0]
    
    imgpoints = []
    objpoints = []
    
    for frame in image_list:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        ret, corners = cv2.findChessboardCorners(gray, (rows,cols), None)
        
        if ret:
            conv_size = (11,11)
            corners = cv2.cornerSubPix(gray, corners, conv_size, (-1,-1), criteria)
            cv2.drawChessboardCorners(frame, (rows, cols), corners, ret)
            cv2.imshow(frame)
            cv2.waitKey(0)
            
            objpoints.append(objp)
            imgpoints.append(corners)
            
    ret, cam_matrix, distortion, rota_vector, transform_vector = cv2.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
    print("Worked: ", ret)
    print("Camera matrix: ", cam_matrix)
    print("Distortion: ", distortion)
    print("Rotation: ", rota_vector)
    print("Transformation: ", transform_vector)
    
    return cam_matrix, distortion


def stereo_calibration(mtx1, dist1, mtx2, dist2, folder1, folder2):
    images_names1 = glob.glob(folder1)
    images_names2 = glob.glob(folder2)
    
    c1_images = []
    c2_images = []
    
    for img1, img2 in zip(images_names1, images_names2):
        _img1 = cv2.imread(img1)
        _img2 = cv2.imread(img2)

        c1_images.append(_img1)
        c2_images.append(_img2)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    rows = 8
    cols = 8
    
    world_scaling = 1.
    
    objp = np.zeros((rows*cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)
    objp = objp * world_scaling
    
    height, width = c1_images[0].shape
    
    
    imgpoints1 = []
    imgpoints2 = []
    objpoints = []
    
    for frame1, frame2 in zip(c1_images, c2_images):
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        ret1, corners1 = cv2.findChessboardCorners(gray1, (rows,cols), None)
        ret2, corners2 = cv2.findChessboardCorners(gray2, (rows,cols), None)
        
        if ret1 and ret2:
            conv_size = (11,11)
            corners1 = cv2.cornerSubPix(gray1, corners1, conv_size, (-1,-1), criteria)
            corners2 = cv2.cornerSubPix(gray2, corners2, conv_size, (-1,-1), criteria)
            
            cv2.drawChessboardCorners(frame1, (rows, cols), corners1, ret1)
            cv2.drawChessboardCorners(frame2, (rows, cols), corners2, ret2)
            
            cv2.imshow(frame1)
            cv2.imshow(frame2)
            cv2.waitKey(0)
            
            objpoints.append(objp)
            imgpoints1.append(corners1)
            imgpoints2.append(corners2)
    
    stereo_calib_flags = cv2.CALIB_FIX_INTRINSIC
    ret, cam_matrix, dist, rota, transform, ematrix, fmatrix = cv2.stereoCalibrate(objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, (width, height), flags=stereo_calib_flags)
    
    return rota, transform


    
    
    
    
    
if __name__ == "__main__":
    mtx1, dist1 = calibrate_camera("3d_testing//Stereo1_Pics")
    mtx2, dist2 = calibrate_camera("3d_testing//Stereo2_Pics")
    