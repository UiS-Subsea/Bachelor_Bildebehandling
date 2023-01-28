# Import libraries
import cv2


def count_frogs(image_path):
    image = cv2.imread(image_path)
    test = cv2.cvtColor(image, cv2.COLOR_RGB2HLS_FULL)
    blur = cv2.GaussianBlur(test, (11, 13), 0)
    canny = cv2.Canny(blur, 50, 120, 13)
    blur2 = cv2.GaussianBlur(canny, (11, 13), 0)
    (cnt, hierarchy) = cv2.findContours(blur2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #cnt is an array of conoures
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, cnt, -1, (255, 0, 0), 5)

    # print(len(cnt))
    # cv2.imshow("Image", test)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow("Blur", blur)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow("Canny", canny)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow("Blur2", blur2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow("Contours", rgb)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return len(cnt) #return the amount of contoures


if __name__ == "__main__":
    c = count_frogs('froggos/froggos9.png')
    print(f"There are {c} frogs")
