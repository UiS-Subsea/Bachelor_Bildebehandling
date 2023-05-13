import cv2
import numpy as np
import glob

def calibrate_camera(image_folder):
    image_names = glob.glob(image_folder)
    image_names = sorted(image_names)
    image_list = []
    
    for img_name in image_names:
        img = cv2.imread(img_name, 1)
        image_list.append(img)
        
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    rows = 5
    cols = 5
    world_scaling = 1.
    
    objp = np.zeros((rows*cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)
    objp = world_scaling* objp
    
    width = image_list[0].shape[1]
    height = image_list[0].shape[0]
    
    imgpoints = []
    objpoints = []
    
    for frame in image_list:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Gray", gray)
        # cv2.waitKey(0)
        ret, corners = cv2.findChessboardCorners(gray, (rows,cols), None)
        # print(corners)
        if ret:
            conv_size = (5,5)
            corners = cv2.cornerSubPix(gray, corners, conv_size, (-1,-1), criteria)
            # cv2.drawChessboardCorners(frame, (rows, cols), corners, ret)
            # cv2.imshow("name", frame)
            # cv2.imwrite("3d_testing\Stereo1_Pics\chessboard_1.png", frame)
            # cv2.waitKey(0)
            
            objpoints.append(objp)
            imgpoints.append(corners)
            
    ret, cam_matrix, distortion, rota_vector, translation = cv2.calibrateCamera(objpoints, imgpoints, (width, height), None, None)
    # print("Worked: ", ret)
    # print("Camera matrix: ", cam_matrix)
    # print("Distortion: ", distortion)
    # print("Rotation: ", rota_vector)
    # print("Translation: ", translation)
    return cam_matrix, distortion
