from PIL import ImageTk, Image # DO PIP INSTALL PILLOW
import tkinter as tk
from opencv_img_test import img, gray



window = tk.Tk()
window.title("Chess")

frame_a = tk.Frame(master=window, width=100, height=100, bg="red")
frame_b = tk.Frame(master=window, width=100, height=100, bg="blue")

#############################################

image1 = Image.open("chess.png") # PIL image from PATH
image2 = Image.fromarray(gray) # PIL image from OPENCV

ptImage = ImageTk.PhotoImage(image1)
ptImage2 = ImageTk.PhotoImage(image2)


label1 = tk.Label(master=frame_a, image=ptImage, text="I am frame A")
label2 = tk.Label(master=frame_b, image=ptImage2, text = "I am frame B")
label1.image = ptImage
label2.image = ptImage2

label1.pack()
label2.pack()

##############################################

frame_a.pack()
frame_b.pack()

window.mainloop()