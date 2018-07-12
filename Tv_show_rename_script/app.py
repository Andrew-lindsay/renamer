#!/usr/bin/env python2
from Tkinter import *
import ttk
import tkFileDialog as filedialog
import tkMessageBox
import tkColorChooser
import re_namer as rn
import os
import thread
import sys

# TODO: scale textbox
# TODO: directly edit the text in new names array in other tab
# TODO: make background colour percistant
# TODO: add icon to window
# TODO: add option to save the conversion between file names
# TODO: fix geometry of popup windows


class EntryBoxWindow:

    def __init__(self, master, label="Value:"):
        self.val = 0

        self.tlw = Toplevel(master, padx=5, pady=5, bg=MainApp.bg, takefocus=True)
        self.tlw.geometry("+550+250")
        self.tlw.resizable(False, False)
        self.val_entry = ttk.Entry(self.tlw, width=6)
        self.butt = ttk.Button(self.tlw, text="Enter", command=self.ret_val)
        ttk.Label(self.tlw, text=label).grid(row=0, column=0, padx=5)
        self.val_entry.grid(row=0, column=1)
        self.butt.grid(row=0, column=2, padx=5)

        self.val_entry.bind('<Return>', lambda x: self.ret_val())

    def ret_val(self):
        try:
            self.val = int(self.val_entry.get())
            self.tlw.destroy()
        except ValueError:
            tkMessageBox.showwarning(title='Value entry error', message='Please entry only interger values')


class ProgressWindow:

    def __init__(self, master, num_files=0):
        self.master = master

        self.tlw = Toplevel(master, padx=5, pady=5, bg=MainApp.bg)
        self.tlw.resizable(False, False)
        self.tlw.geometry("+550+250")

        self.val = DoubleVar()
        self.val.set(0.0)

        ttk.Label(self.tlw, text="Committing..", background=MainApp.bg).pack(anchor=W)
        self.prog_bar = ttk.Progressbar(self.tlw, mode='determinate', maximum=float(num_files), length=200, variable=self.val)
        self.prog_bar.pack()
        self.tlw.withdraw()

    def set_num_files(self, num_files):
        self.prog_bar['maximum'] = float(num_files)
        self.prog_bar['value'] = 0.0

    def destroy(self):
        self.tlw.destroy()

    def withdraw(self):
        self.tlw.withdraw()

    def show(self):
        self.tlw.deiconify()
        self.tlw.lift(self.master)
        self.tlw.configure(takefocus=True)


class MainApp:
    # class variables
    bg = '#e0dbdd'

    def __init__(self, master):
        """Create widgets to be placed on root window"""
        # vars
        self.bg = '#e0dbdd'
        self.dir_str = StringVar()
        self.fl_list = []
        self.fl_new_names = []
        self.count_val = 1
        # directory that commit command uses so that value cannot be changed between apply and commit
        self.dire_commit = ""
        self.master_ref = master

        # master setup
        master.title("Re-namer")
        master.geometry("520x510+400+100")
        master.configure(background=self.bg)
        master.option_add('*tearOff', False)

        # menu bar
        menubar = Menu(master, background=self.bg)
        menubar.config(bg=self.bg)
        master.config(menu=menubar, bg=self.bg)
        file = Menu(menubar, background=self.bg)
        options = Menu(menubar, background=self.bg)
        menubar.add_cascade(menu=file, label="File")
        menubar.add_cascade(menu=options, label="Options")
        file.add_command(label="Save")
        file.add_command(label="Exit", command=lambda: sys.exit(0))
        options.add_command(label="Select Background", command=lambda: self.color_picker(master))
        options.add_command(label="Set Count", command=self.count_function)

        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.bg)
        self.style.configure('TButton', background=self.bg)
        self.style.configure('TLabel', background=self.bg)

        self.prog_win = ProgressWindow(master)

        self.top_frame(master)

        self.bottom_frame(master)

    def top_frame(self, master):
        """Defines top panel frame of app"""

        # top frame
        self.top_fr = ttk.Frame(master, padding=(10, 10))
        self.top_fr.grid(row=0, column=0, sticky=NW)

        # directory stuff
        self.cwd_lb = ttk.Label(self.top_fr, text="Current Directory:")
        self.cwd_entry = ttk.Entry(self.top_fr, width=60, textvariable=self.dir_str)
        self.cwd_button = ttk.Button(self.top_fr, text='Select', command=self.select_dir)
        self.cwd_lb.grid(row=0, column=0, sticky=NW, columnspan=2)
        self.cwd_entry.grid(row=1, column=0, columnspan=4, pady=(0, 10))
        self.cwd_button.grid(row=1, column=4, padx=(5, 0), pady=(0, 10))

        # file type
        self.file_type_lb = ttk.Label(self.top_fr, text="File Type:")
        self.file_type_entry = ttk.Entry(self.top_fr, width=10)
        self.file_type_lb.grid(row=2, column=0, sticky=NW)
        self.file_type_entry.grid(row=3, column=0, sticky=NW)
        self.file_type_entry.bind('<Return>', lambda x: self.apply())

        # Season
        self.season_lb = ttk.Label(self.top_fr, text="Season:")
        self.season_entry = ttk.Entry(self.top_fr, width=10)
        self.season_lb.grid(row=2, column=1, sticky=NW)
        self.season_entry.grid(row=3, column=1, sticky=NW)
        self.season_entry.bind('<Return>', lambda x: self.apply())

        # left
        self.left_lb = ttk.Label(self.top_fr, text="Left:")
        self.left_entry = ttk.Entry(self.top_fr, width=10)
        self.left_lb.grid(row=2, column=2, sticky=NW)
        self.left_entry.grid(row=3, column=2, sticky=NW)
        self.left_entry.bind('<Return>', lambda x: self.apply())

        # file type
        self.right_lb = ttk.Label(self.top_fr, text="Right:")
        self.right_entry = ttk.Entry(self.top_fr, width=10)
        self.right_lb.grid(row=2, column=3, sticky=NW)
        self.right_entry.grid(row=3, column=3, sticky=NW)
        self.right_entry.bind('<Return>', lambda x: self.apply())

    def bottom_frame(self, master):
        """defines bottom frame"""

        # Bottom frame
        self.bottom_fr = ttk.Frame(master, padding=(10, 0))
        self.bottom_fr.grid(row=1, column=0, sticky=NW)
        self.bottom_fr.rowconfigure(1, weight=1)
        #self.bottom_fr.columnconfigure()

        # scroll bars
        self.x_txt_scr = ttk.Scrollbar(self.bottom_fr, orient=HORIZONTAL)
        self.y_txt_scr = ttk.Scrollbar(self.bottom_fr, orient=VERTICAL)

        # text box stuff
        self.tb_lb = ttk.Label(self.bottom_fr, text="File name changes:")
        self.tb = Text(self.bottom_fr, height=20, width=69, font=('Arial', 10), wrap=NONE)
        self.tb_lb.grid(row=0, column=0, columnspan=2, sticky=NW)
        self.tb.grid(row=1, column=0, columnspan=5, sticky=NW)

        # binding scroll bars
        self.x_txt_scr.configure(command=self.tb.xview)
        self.y_txt_scr.configure(command=self.tb.yview)
        self.x_txt_scr.grid(row=2, column=0, columnspan=6, sticky=EW, pady=(0, 10))
        self.y_txt_scr.grid(row=1, column=5, sticky=NS)
        self.tb.configure(xscrollcommand=self.x_txt_scr.set, yscrollcommand=self.y_txt_scr.set)

        # buttons
        self.commit_bt = ttk.Button(self.bottom_fr, text="Commit", state='disabled', command=self.commit)
        self.apply_bt = ttk.Button(self.bottom_fr, text="Apply", command=self.apply)
        self.commit_bt.grid(row=3, column=1, sticky=SE)
        self.apply_bt.grid(row=3, column=2, sticky=NE)

    def select_dir(self):
        """Opens file selection dir"""
        dir_name = filedialog.askdirectory()
        if dir_name is not "":
            print("name: " + dir_name)
            self.tb.delete("1.0", 'end')
            self.dir_str.set(dir_name)

    def commit(self):
        """Commit and alters files names"""
        # Create progress window
        self.prog_win.set_num_files(len(self.fl_list)+1)
        self.prog_win.show()
        # start thread that handles commit so gui thread can update
        thread.start_new_thread(rn.commit_name_change, (self.fl_list, self.fl_new_names, self.dire_commit, self.prog_win.prog_bar))
        print("Completed commit")
        self.commit_bt.configure(state='disabled')
        self.master_ref.after(100, self.check_prog)

    def check_prog(self):
        # keep checking the progress bar if it has finished then hid the window
        if self.prog_win.val.get() == len(self.fl_list):
            self.prog_win.withdraw()
            self.count_val = 1
        else:
            self.master_ref.after(100, self.check_prog)

    def apply(self):
        """Shows changes to files in textbox"""
        # TODO: save last operation so it can be reverted (maybe save all of them)

        # check directory is not empty and is a vaild dirctory
        if self.dir_str.get() is "" or not os.path.isdir(self.dir_str.get()):
            tkMessageBox.showwarning(title="Invalid Directory", message="Please enter a valid Directory")
            return

        # check entry boxes for valid entry data
        try:
            left_off = int(self.left_entry.get())
            right_off = int(self.right_entry.get())
            season = str(int(self.season_entry.get()))
        except ValueError:
            tkMessageBox.showwarning(title="Invalid data entered",
                                     message="One or more of the entry fields has invalid data\nEnsure that left, "
                                             "right and season are integers.")
            # exit function if invalid parameter
            return

        self.fl_list = self.file_list_sort(dire=self.dir_str.get(), file_type=self.file_type_entry.get())
        # print to terminal
        for fl in self.fl_list:
            print(fl)

        self.fl_new_names = rn.change_file_names(left_offset=left_off,
                                                 right_offset=right_off,
                                                 file_ending=self.file_type_entry.get(),
                                                 season=season,
                                                 file_list=self.fl_list,
                                                 counter=self.count_val)

        # alter text box
        self.tb.delete("1.0", 'end')
        for x in range(0, len(self.fl_list)):
            self.tb.insert(str(x+1)+".0", self.fl_list[x] + " --> " + self.fl_new_names[x] + "\n")

        # allow user to now commit changes to file names
        self.commit_bt.configure(state='!disabled')
        self.dire_commit = self.dir_str.get()

    def color_picker(self, master):
        colour_selected = tkColorChooser.askcolor()
        print(colour_selected)
        self.style.configure('TFrame', background=colour_selected[1])
        self.style.configure('TButton', background=colour_selected[1])
        self.style.configure('TLabel', background=colour_selected[1])
        master.configure(background=colour_selected[1])
        self.bg = colour_selected[1]
        MainApp.bg = colour_selected[1]

    @staticmethod
    def file_list_sort(dire, file_type):
        """takes directory and file ending and returns list of files in directory that end with that file ending"""
        filelist = []
        for _file in os.listdir(dire):
            if _file.endswith(file_type):
                filelist.append(_file)
        filelist.sort()
        return filelist

    def load_preferences(self):
        pass

    # menu functions
    def count_function(self):
        ent = EntryBoxWindow(self.master_ref, label="Count value:")
        self.master_ref.wait_window(ent.tlw)
        self.count_val = ent.val
        print('values returned', self.count_val)


def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()