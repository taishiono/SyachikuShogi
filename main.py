import tkinter as tk
from PIL import Image, ImageTk
from classes import Bann

bann = Bann(masu_size=80, line_size=5)
bann_img = bann.get_current_bann_img()
root = tk.Tk()
imgTk = ImageTk.PhotoImage(image=Image.fromarray(bann_img))
canvas = tk.Canvas(root, width=bann_img.shape[0], height=bann_img.shape[1])
canvas.pack()
img_on_campus = canvas.create_image(0, 0, anchor="nw", image=imgTk)
wait_finish = True


def clk():
    root.destroy()


def ButtonPress1(event):
    global bann
    global img_new
    global canvas
    global wait_finish

    a = bann.key_event_handler(event)
    if a[0] == 2:
        img_new = ImageTk.PhotoImage(image=Image.fromarray(a[1]))
        canvas.itemconfig(img_on_campus, image=img_new)
    elif a[0] == 1 or a[0] == -1:
        img_new = ImageTk.PhotoImage(image=Image.fromarray(a[1]))
        canvas.itemconfig(img_on_campus, image=img_new)

        label = tk.Label(root, text="Player {} Win!".format(a[0]))
        label.pack()
        button = tk.Button(root, text="Finish Game?", command=clk)
        button.pack()
    else:
        pass


if __name__ == "__main__":
    canvas.bind("<ButtonPress-1>", ButtonPress1)
    root.mainloop()
