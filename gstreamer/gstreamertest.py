import cv2


gst_feed = "-v udpsrc multicast-group=224.1.1.1 auto-multicast=true port=5000 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96 ! rtph264depay ! h264parse ! decodebin ! videoconvert ! appsink sync=false"

cap = cv2.VideoCapture(gst_feed, cv2.CAP_GSTREAMER)
# cap = cv2.VideoCapture(0)
while cap.isOpened():
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                cv2.imwrite("gstreamer//test1.jpg", frame)
                cv2.destroyAllWindows()
                cap.release()
                break
        else:
            break
else:
    print("Unable to open camera") 


# 5001 port is left camera
# 5000 port is right camera