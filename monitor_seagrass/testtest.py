import cv2

img = cv2.imread("monitor_seagrass\images\Example1.png")
imggg = img.copy()
# green = cv2.inRange(img, (30, 80, 0), (100, 255, 100))
# true_green = cv2.bitwise_and(img, img, mask=green)
canny = cv2.Canny(img, 100, 200)


# cv2.imshow("green", green)
# cv2.imshow("true green", true_green)
cv2.imshow("original", imggg)
cv2.imshow("Canny", canny)
cv2.waitKey(0)