from PIL import Image


#takes in an image, finds the red dot, finds displacement form center, returns what movement to do, forward, stop, move to side
#må lage test filer for denne funksjonen!
def docking_red_center_allign(img_path):
    first_red_px = 0
    last_red_px = 0
    red_px_counter = 0

    with Image.open(img_path) as img:
        new_img = img.convert("RGB") #convert to RGB for more efficiency, stores 3 bytes instead of 4, 25% boost in performance
        size_x, size_y = new_img.size #size of img
        center = (size_x // 2, size_y // 2) #exact pixel center as tuple

        print(new_img)
        px = new_img.load() #load pixel-matrix from image

        for x in range(size_x): #loop through axes
            for y in range(size_y):
                if px[x, y][0] > 180 and px[x, y][1] < 80 and px[x, y][2] < 80: #checks for red color
                    # print(px[x, y])
                    red_px_counter += 1
                    last_red_px = (x, y)

                    if first_red_px == 0:
                        first_red_px = (x, y)

        center_of_red = (round((first_red_px[0] + last_red_px[0]) / 2), round((first_red_px[1] + last_red_px[1]) / 2)) #calculate dead center of red spot
        # print(f"center: [{center}]")
        # print(f"center_of_red koord: [{center_of_red}]")

        diff_x = abs(center[0] - center_of_red[0]) #difference between center of image and center of red dot
        diff_y = abs(center[1] - center_of_red[1])

        print(diff_x, diff_y)
        print(red_px_counter)

        if red_px_counter > 400: #closing in on the dot, has to stop after certain pixels, not sure how many yet
            print("Here code for stop needs to be executed.")
            return "STOP ROV"

        if -10 < diff_x < 10 and -10 < diff_y < 10: #we have found center and can now move forward
            print("Here code for move forward needs to be executed.")
            return "MOVE FORWARD"

        print("This is the amount of pixels the ROV is displaced, and needs to be moved")
        return diff_x, diff_y #returns displacement if nothing else is returned first



if __name__ == "__main__":
    dock = docking_red_center_allign("images\dockingstation720.png")
    print(dock)


