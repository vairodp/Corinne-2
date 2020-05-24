from gui import MyGui
from controller import Controller
from tkinter import Tk, messagebox
import tkinter as tkinter
from PIL import ImageTk, Image

import os.path

def main():
    root = Tk()
    icon = ImageTk.PhotoImage(Image.open("icons/logo-ico.ico"))
    root.tk.call("wm","iconphoto",root._w,icon)
    c = Controller()
    MyGui(root, c)
    root.mainloop()


if __name__ == '__main__':
    main()