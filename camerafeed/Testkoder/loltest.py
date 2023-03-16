import cv2



cam = cv2.VideoCapture("filename.avi")


while True:
    frame = cam.read()[1]
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break