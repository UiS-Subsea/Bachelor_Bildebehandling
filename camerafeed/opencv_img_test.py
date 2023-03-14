import cv2 # DO PIP INSTALL OPENCV-PYTHON
from matplotlib import pyplot as plt

img = cv2.imread("chess.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# def show_img(img):
#     new_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     plt.imshow(new_img)
#     plt.show()
# cv2.resize(img, (0,0), fx=0.5, fy=0.5)
def show_img(img):
    cv2.imshow("Chess", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_blacked_img(img):
    new_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    plt.imshow(new_img, cmap="gray")
    plt.show()

def show_both(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow("Chess", img)
    cv2.imshow("Chess Gray", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_img(img)
    # show_blacked_img(img)
    # show_both(img)