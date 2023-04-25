from PIL import Image
import time

def find_red(image_file):
    red_px_list = []
    # Open the image
    img = Image.open(image_file)

    # Get the size of the image
    width, height = img.size

    # Loop through each pixel of the image
    for x in range(width):
        for y in range(height):
            
            # Get the RGB values of the pixel
            r, g, b = img.getpixel((x, y))
            
            # Check if the pixel is within red range
            if r >= 200 and g <= 70 and b <= 0:
                red_px_list.append((x, y))


if __name__ == "__main__":
    # Get start time
    start = time.perf_counter()
    find_red("autonomous_docking\older_versions\docking_1080p.png")
    # Print runtime of the function
    print(round(time.perf_counter() - start, 4))

