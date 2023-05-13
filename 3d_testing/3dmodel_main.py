import numpy as np
from Stereo_Calibration import stereo_calibration
from Camera_Calibration import calibrate_camera
from Triangulate import triangulate



if __name__ == "__main__":
    # mtx1, dist1 = calibrate_camera("3d_testing/Stereo1_Pics/*")
    # mtx2, dist2 = calibrate_camera("3d_testing/Stereo2_Pics/*")qq
    # np.savez("3d_testing//cam1_calibration.npz", mtx=mtx1, dist=dist1)
    # np.savez("3d_testing//cam2_calibration.npz", mtx=mtx2, dist=dist2)

    
    # R, T = stereo_calibration(mtx1, dist1, mtx2, dist2, "3d_testing/Stereo1_Pics/*", "3d_testing/Stereo2_Pics/*")
    # np.savez("3d_testing//stereo_calibration.npz", R=R, T=T)
    mtx1 = np.load("3d_testing//cam1_calibration.npz")['mtx']
    mtx2 = np.load("3d_testing//cam2_calibration.npz")['mtx']
    R = np.load("3d_testing//stereo_calibration.npz")['R']
    T = np.load("3d_testing//stereo_calibration.npz")['T']
    
    triangulate(mtx1, mtx2, R, T)
    