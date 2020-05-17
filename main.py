from gui import MyGui
from controller import Controller
from tkinter import Tk, messagebox

import os.path

def main():
    root = Tk()
    root.iconbitmap("icons/logo-ico.ico")
    c = Controller()
    MyGui(root, c)
    root.mainloop()


if __name__ == '__main__':
    main()