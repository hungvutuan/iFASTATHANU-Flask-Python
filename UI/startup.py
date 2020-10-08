import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from AI.logistic_model import *

# define the logo's dimensions
logo_w = 200
logo_h = int(logo_w / 5)
# define buttons sizes
btn_w, btn_h = 12, 2
windows_size = '300x130'


def handle_start(event):
    # exec(open("../iFASTATHANU.cmd").read())
    print("start pressed")


def handle_retrain(event):
    train(False)
    print("retrain pressed")


root = tk.Tk()
root.wm_iconbitmap('fire.ico')
root.geometry(windows_size)
root.title("iFASTATHANU v" + VAR.get_current_version())  # title of the program

# insert the program's logo in a Canvas
canvas = tk.Canvas(root, width=logo_w, height=logo_h)
canvas.pack()

image_logo = Image.open("Logo_thumbnail_gray.png")
resized_image_logo = image_logo.resize((logo_w, logo_h), Image.ANTIALIAS)

logo = ImageTk.PhotoImage(resized_image_logo)
canvas.create_image(logo_w / 2, logo_h / 2, image=logo)

btn_start = tk.Button(text="START", width=btn_w, height=btn_h)
btn_start.bind("<Button-1>", handle_start)
btn_start.pack()

btn_retrain = tk.Button(text="RETRAIN", width=btn_w, height=btn_h)
btn_retrain.bind("<Button-1>", handle_retrain)
btn_retrain.pack(pady=10)
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
progress.pack()

root.resizable(True, True)
root.mainloop()
