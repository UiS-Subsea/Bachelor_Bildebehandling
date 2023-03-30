from PIL import ImageTk, Image # DO PIP INSTALL PILLOW
import tkinter as tk
from opencv_img_test import img, gray

root = tk.Tk()

image1 = Image.open("chess.png") # PIL image from PATH

image2 = Image.fromarray(gray) # PIL image from OPENCV

ptImage = ImageTk.PhotoImage(image1)
ptImage2 = ImageTk.PhotoImage(image2)

label1 = tk.Label(image=ptImage)
label2 = tk.Label(image=ptImage2)
label1.image = ptImage
label2.image = ptImage2

label1.pack()
label2.pack()
root.mainloop()