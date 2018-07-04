#!/usr/bin/env python2
from Tkinter import *
import ttk


class ProgressWindow:

    def __init__(self, master):
        self.tlw = Toplevel(master)


class MainApp:

    def __init__(self, master):
        """Create widgets to be placed on root window"""
        # master setup
        master.title("Re-namer")

        # top frame
        self.cwd_lb = ttk.Label(master, text="Current Directory:")


def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()