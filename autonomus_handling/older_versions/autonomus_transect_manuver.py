from PIL import Image
import math

def is_dark_blue(px):
    if px[0] > 40 and px[1] > 40 and px[2] > 180:
        return True
    return False


#returns the angle of displacement relative to the blue lines in degrees as the avg
def angle_of_displacement(topleft, bottomleft, topright, bottomright):
    line1 = math.degrees(math.atan((bottomleft[0] - topleft[0]) / (topleft[1] - bottomleft[1])))
    line2 = math.degrees(math.atan((bottomright[0] - topright[0]) / (topright[1] - bottomright[1])))

    return round((line1 + line2), 3) / 2 #average of the displacement between the two lines


def autonomus_transect_manuver(imagepath): 
    with Image.open(imagepath) as img:
        new_img = img.convert("RGB")
        size_x, size_y = new_img.size #size of img
        px = new_img.load() #load pixel-matrix from image

        r1_first_dark = 0
        r1_last_dark = 0

        r2_first_dark = 0
        r2_last_dark = 0

        for x1 in range(size_x):
            pixel = px[x1, 0]
            if is_dark_blue(pixel):
                r1_first_dark = (x1, 0)
                break

        for x2 in range(size_x - 1, 0, -1):
            pixel = px[x2, 0]
            if is_dark_blue(pixel):
                r1_last_dark = (x2, 0)
                break

        for x3 in range(size_x):
            pixel = px[x3, size_y - 1]
            if is_dark_blue(pixel):
                r2_first_dark = (x3, size_y)
                break

        for x4 in range(size_x - 1, 0, -1):
            pixel = px[x4, size_y - 1]
            if is_dark_blue(pixel):
                r2_last_dark = (x4, size_y)
                break

        displacement_angle = angle_of_displacement(r1_first_dark, r2_first_dark, r1_last_dark, r2_last_dark)

        if -1 < displacement_angle < 1:
            return "GO FORWARD", displacement_angle

        if displacement_angle >= 1:
            return "SWING RIGHT", displacement_angle

        return "SWING LEFT", displacement_angle
        

        

if __name__ == "__main__":
    a = autonomus_transect_manuver("autonomus_handling/older_versions/transect_straight.png")
    print(a)
    





