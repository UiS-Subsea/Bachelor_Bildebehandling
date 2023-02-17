import cv2

gst_feed = "-v udpsrc port=5000 ! application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"

cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
print(cv2.getBuildInformation())
while cap.isOpened():
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
else:
    print("Unable to open camera") 


