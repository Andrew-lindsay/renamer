#!/usr/bin/env python2
from Tkinter import *
import ttk
import re_namer


class ProgressWindow:

    def __init__(self, master):
        self.tlw = Toplevel(master)


class MainApp:

    def __init__(self, master):
        """Create widgets to be placed on root window"""
        # master setup
        master.title("Re-namer")
        master.geometry("510x600+400+100")
        self.bg = '#e0dbdd'
        master.configure(background=self.bg)

        # style TODO: add style
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.bg)
        self.style.configure('TButton', background=self.bg)
        self.style.configure('TLabel', background=self.bg)

        self.top_frame(master)

        self.bootm_fram(master)

    def top_frame(self,master):
        # top frame
        self.top_fr = ttk.Frame(master, padding=(10, 10))
        self.top_fr.grid(row=0, column=0, sticky=NW)
        # directory stuff
        self.cwd_lb = ttk.Label(self.top_fr, text="Current Directory:")
        self.cwd_entry = ttk.Entry(self.top_fr, width=60)
        self.cwd_button = ttk.Button(self.top_fr, text='Select', command=self.select_dir)
        self.cwd_lb.grid(row=0, column=0, sticky=NW, columnspan=2)
        self.cwd_entry.grid(row=1, column=0, columnspan=4, pady=(0, 10))
        self.cwd_button.grid(row=1, column=4, padx=(5, 0), pady=(0, 10))
        # file type
        self.file_type_lb = ttk.Label(self.top_fr, text="File Type:")
        self.file_type_entry = ttk.Entry(self.top_fr, width=10)
        self.file_type_lb.grid(row=2, column=0, sticky=NW)
        self.file_type_entry.grid(row=3, column=0, sticky=NW)
        # Season
        self.season_lb = ttk.Label(self.top_fr, text="Season:")
        self.season_entry = ttk.Entry(self.top_fr, width=10)
        self.season_lb.grid(row=2, column=1, sticky=NW)
        self.season_entry.grid(row=3, column=1, sticky=NW)
        # left
        self.left_lb = ttk.Label(self.top_fr, text="Left:")
        self.left_entry = ttk.Entry(self.top_fr, width=10)
        self.left_lb.grid(row=2, column=2, sticky=NW)
        self.left_entry.grid(row=3, column=2, sticky=NW)
        # file type
        self.right_lb = ttk.Label(self.top_fr, text="Right:")
        self.right_entry = ttk.Entry(self.top_fr, width=10)
        self.right_lb.grid(row=2, column=3, sticky=NW)
        self.right_entry.grid(row=3, column=3, sticky=NW)

    def bottom_frame(self, master):
        """"""
        # Bottom frame
        self.bottom_fr = ttk.Frame(master, padding=(10, 0))
        self.bottom_fr.grid(row=1, column=0, sticky=NW)
        self.bottom_fr.rowconfigure(1, weight=1)
        #self.bottom_fr.columnconfigure()
        # text box stuff
        self.tb_lb = ttk.Label(self.bottom_fr, text="File name changes:")
        self.tb = Text(self.bottom_fr, height=20, width=69, font=('Arial', 10))
        self.tb_lb.grid(row=0, column=0, columnspan=2, sticky=NW)
        self.tb.grid(row=1, column=0, columnspan=5, sticky=NW)

    def select_dir(self):
        """Opens file selection dir"""


def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()