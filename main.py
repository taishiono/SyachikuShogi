import tkinter as tk
from PIL import Image, ImageTk
from classes import Bann

bann = Bann(masu_size=80, line_size=5)
bann_img = bann.get_current_bann()
root = tk.Tk()
imgTk = ImageTk.PhotoImage(image=Image.fromarray(bann_img))
canvas = tk.Canvas(root, width=bann_img.shape[0], height=bann_img.shape[1])
canvas.pack()
img_on_campus = canvas.create_image(0, 0, anchor="nw", image=imgTk)


def ButtonPress1(event):
    global bann
    global img_new
    global canvas

    a = bann.search_koma_by_eventPosition(event)
    if a[0] == 1:
        img_new = ImageTk.PhotoImage(image=Image.fromarray(a[1]))
        canvas.itemconfig(img_on_campus, image=img_new)
    else:
        pass


if __name__ == "__main__":
    canvas.bind("<ButtonPress-1>", ButtonPress1)
    root.mainloop()
