#!/usr/bin/env python2
from Tkinter import *
import ttk
import tkFileDialog as filedialog
import tkMessageBox
import tkColorChooser
import tkFont
import re_namer as rn
import os
import thread
import sys
import csv
import yaml

# TODO: fix geometry of popup windows
# TODO: fix color issue after color picker used but bo color selected
# TODO: get directory box to be scalable hoziontaly
# TODO: fix progress bar so spawned each time it is needed
# TODO: fix 


class EntryBoxWindow:

    def __init__(self, master, label="Value:"): 
        self.val = 0

        self.tlw = Toplevel(master, padx=5, pady=5, bg=MainApp.bg, takefocus=True)
        self.tlw.geometry("+550+250")
        self.tlw.resizable(False, False)

        img = PhotoImage(file=MainApp.icon)
        self.tlw.tk.call('wm', 'iconphoto', self.tlw._w, img)

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
        img = PhotoImage(file=MainApp.icon)
        self.tlw.tk.call('wm', 'iconphoto', self.tlw._w, img)

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
    icon = os.path.join(os.getcwd(), 'renamer.gif')

    def __init__(self, master):
        """Create widgets to be placed on root window"""
        # vars
        self.bg = '#e0dbdd'
        if os.name != "nt":
            self.app_font = tkFont.Font(family="DejaVu Sans", size=9)
        else:
            self.app_font = tkFont.Font(family='Segoe UI', size=9)  # use default for windwow
        self.dir_str = StringVar()
        self.auto_save = IntVar()
        self.fl_list = []
        self.fl_new_names = []
        self.count_val = 1
        # directory that commit command uses so that value cannot be changed between apply and commit
        self.dire_commit = ""
        self.master_ref = master

        # load preferences
        self.settings = self.load_preferences()

        # set settings
        self.auto_save.set(self.settings['auto_save'])
        self.bg = self.settings['colour']
        MainApp.bg = self.bg

        master.title("Re-namer")
        # master setup
        master.geometry("610x535+400+100")
        master.configure(background=self.bg)
        master.option_add('*tearOff', False)
        img = PhotoImage(file=MainApp.icon)
        master.call('wm', 'iconphoto', master._w, img)

        # menu bar
        menubar = Menu(master, font=self.app_font, bd=0)
        # menubar.configure(bg=self.bg)
        master.config(menu=menubar)
        self.file_m = Menu(menubar, font=self.app_font)
        self.options = Menu(menubar, font=self.app_font)    
        menubar.add_cascade(menu=self.file_m, label="File")
        menubar.add_cascade(menu=self.options, label="Options")
        self.file_m.add_command(label="Save", state='disabled', command=self.save_file_conver)
        self.file_m.add_command(label="Revert", state='disabled', command=self.revert_conver)
        self.file_m.add_command(label="Exit", command=lambda: sys.exit(0))
        self.options.add_command(label="Select Background", command=lambda: self.color_picker(master))
        self.options.add_command(label="Set Count", command=self.count_function)
        self.options.add_checkbutton(label='Auto Save', variable=self.auto_save)
        self.options.add_command(label="Save Settings", command=self.write_preferences)

        self.style = ttk.Style()
        if os.name != "nt":
            self.style.theme_use('alt')
        self.style.configure('TFrame', background=self.bg, font=self.app_font)
        self.style.configure('TButton', font=self.app_font)
        self.style.configure('TLabel', background=self.bg, font=self.app_font)

        self.prog_win = ProgressWindow(master)

        self.top_frame(master)

        self.bottom_frame(master)

    def top_frame(self, master):
        """Defines top panel frame of app"""
        # top frame
        master.columnconfigure(0, weight=1)

        self.top_fr = ttk.Frame(master, padding=(10, 10))
        self.top_fr.grid(row=0, column=0, sticky="ew")
        # self.top_fr.rowconfigure(1, weight=1)
        self.top_fr.columnconfigure(4, weight=1)


        # directory stuff
        self.cwd_lb = ttk.Label(self.top_fr, text="Current Directory:")
        self.cwd_entry = ttk.Entry(self.top_fr, width=60, textvariable=self.dir_str)
        self.cwd_button = ttk.Button(self.top_fr, text='Select', command=self.select_dir)
        self.cwd_lb.grid(row=0, column=0, sticky=NW, columnspan=4)
        self.cwd_entry.grid(row=1, column=0, columnspan=5, pady=(0, 10), sticky="ew")
        self.cwd_button.grid(row=1, column=6, padx=(5, 0), pady=(0, 10))
        self.cwd_entry.bind('<Return>', lambda x: self.is_backup())

        # file type
        self.file_type_lb = ttk.Label(self.top_fr, text="File Type:")
        self.file_type_entry = ttk.Entry(self.top_fr, width=10)
        self.file_type_lb.grid(row=2, column=0, sticky=NW)
        self.file_type_entry.grid(row=3, column=0, sticky=NW, padx=(0, 10))
        self.file_type_entry.bind('<Return>', lambda x: self.apply())

        # Season
        self.season_lb = ttk.Label(self.top_fr, text="Season:")
        self.season_entry = ttk.Entry(self.top_fr, width=10)
        self.season_lb.grid(row=2, column=1, sticky=NW)
        self.season_entry.grid(row=3, column=1, sticky=NW, padx=(0, 10))
        self.season_entry.bind('<Return>', lambda x: self.apply())

        # left
        self.left_lb = ttk.Label(self.top_fr, text="Left:")
        self.left_entry = ttk.Entry(self.top_fr, width=10)
        self.left_lb.grid(row=2, column=2, sticky=NW)
        self.left_entry.grid(row=3, column=2, sticky=NW, padx=(0, 10))
        self.left_entry.bind('<Return>', lambda x: self.apply())

        # file type
        self.right_lb = ttk.Label(self.top_fr, text="Right:")
        self.right_entry = ttk.Entry(self.top_fr, width=10)
        self.right_lb.grid(row=2, column=3, sticky=NW)
        self.right_entry.grid(row=3, column=3, sticky=NW, padx=(0, 10))
        self.right_entry.bind('<Return>', lambda x: self.apply())

    def bottom_frame(self, master):
        """defines bottom frame"""
        # Bottom frame
        self.bottom_fr = ttk.Frame(master, padding=(10, 0))
        master.rowconfigure(1, weight=1)
        master.columnconfigure(0, weight=1)

        self.bottom_fr.grid(row=1, column=0, sticky="nsew")
        self.bottom_fr.rowconfigure(1, weight=1)
        self.bottom_fr.columnconfigure(0, weight=1)

        # scroll bars
        self.x_txt_scr = ttk.Scrollbar(self.bottom_fr, orient=HORIZONTAL)
        self.y_txt_scr = ttk.Scrollbar(self.bottom_fr, orient=VERTICAL)

        # text box stuff
        self.tb_lb = ttk.Label(self.bottom_fr, text="File name changes:")
        self.tb = Text(self.bottom_fr, height=20, width=69, font=('DejaVu Sans Mono', 9), wrap=NONE)
        self.tb_lb.grid(row=0, column=0, columnspan=2, sticky=NW)
        self.tb.grid(row=1, column=0, columnspan=5, sticky="nsew")

        # binding scroll bars
        self.x_txt_scr.configure(command=self.tb.xview)
        self.y_txt_scr.configure(command=self.tb.yview)
        self.x_txt_scr.grid(row=2, column=0, columnspan=6, sticky=EW, pady=(0, 10))
        self.y_txt_scr.grid(row=1, column=5, sticky=NS)
        self.tb.configure(xscrollcommand=self.x_txt_scr.set, yscrollcommand=self.y_txt_scr.set)

        # buttons
        #self.buttFrame = ttk.Frame(self.bottom_fr, padding=(10, 0))
        #self.buttFrame.grid(row=3, column=0, sticky="nsew")
        self.commit_bt = ttk.Button(self.bottom_fr, text="Commit", state='disabled', command=self.commit)
        self.apply_bt = ttk.Button(self.bottom_fr, text="Apply", command=self.apply)
        self.commit_bt.grid(row=3, column=0, padx=(0, 110), pady=(0, 10))
        self.apply_bt.grid(row=3, column=0, padx=(110, 0), pady=(0, 10))

    def select_dir(self):
        """Opens file selection dir"""
        dir_name = filedialog.askdirectory()
        if dir_name is not "":
            print("name: " + dir_name)
            self.tb.delete("1.0", 'end')
            self.dir_str.set(dir_name)
            if os.path.isfile(os.path.join(dir_name, 'backup.csv')):
                self.file_m.entryconfigure('Revert', state='normal')
            self.file_m.entryconfigure('Save', state='disabled')
            self.commit_bt.configure(state='disabled')

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
            self.prog_win.val.set(0.0)
            # auto save check box checked then execute
            if self.auto_save.get():
                self.save_file_conver()
            # once commited can then write commit to file
            self.file_m.entryconfigure('Save', state='normal')
            # commited names for if save is used
        else:
            self.master_ref.after(100, self.check_prog)

    def apply(self):
        """Shows changes to files in textbox"""
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

        # call to external module
        self.fl_new_names = rn.change_file_names(left_offset=left_off,
                                                 right_offset=right_off,
                                                 file_ending=self.file_type_entry.get(),
                                                 season=season,
                                                 file_list=self.fl_list,
                                                 counter=self.count_val)

        # find max, try block in case list of files is empty
        try:
            # create list of file name lengths then find max
            max_name_len = max([len(name) for name in self.fl_list])
        except ValueError:
            max_name_len = 0

        # alter text box
        self.tb.delete("1.0", 'end')
        for x in range(0, len(self.fl_list)):
            self.tb.insert(str(x+1)+".0", self.fl_list[x] + " " + "-"*(max_name_len - len(self.fl_list[x])) + "--> " + self.fl_new_names[x] + "\n")

        # allow user to now commit changes to file names
        self.commit_bt.configure(state='!disabled')
        self.dire_commit = self.dir_str.get()

    def color_picker(self, master):
        colour_selected = tkColorChooser.askcolor()
        if colour_selected != (None, None):
            print("colour:" + str(colour_selected))
            self.style.configure('TFrame', background=colour_selected[1])
            self.style.configure('TLabel', background=colour_selected[1])
            master.configure(background=colour_selected[1])
            self.bg = colour_selected[1]
            MainApp.bg = colour_selected[1]
        else:
            print("No colour selected: " + str(colour_selected))

    @staticmethod
    def file_list_sort(dire, file_type):
        """takes directory and file ending and returns list of files in directory that end with that file ending"""
        file_list = []
        for _file in os.listdir(dire):
            if _file.endswith(file_type):
                file_list.append(_file)
        file_list.sort()
        return file_list

    def load_preferences(self):
        """Load setting from yaml file"""
        if os.path.isfile(os.path.join(os.getcwd(), 'properties.yaml')):
            with open('properties.yaml', 'r') as prop:
                obj = yaml.load(prop)
                return obj
        else:
            # create dictionary
            data = {"colour": '#e0dbdd', "auto_save": 0}
            # write to file
            with open('properties.yaml', 'w') as prop_new:
                yaml.dump(data, prop_new, default_flow_style=False)
            return data

    def write_preferences(self):
        """Write preferences back to the property yaml file"""
        self.settings['auto_save'] = self.auto_save.get()
        self.settings['colour'] = self.bg
        with open('properties.yaml', 'w') as prop_new:
            yaml.dump(self.settings, prop_new, default_flow_style=False)
        tkMessageBox.showinfo(title='Settings save', message='Your settings have been saved')

    def is_backup(self):
        """When hitting enter while tpying in directory entry box check if backup exists, enable option to revert"""
        if os.path.isfile(os.path.join(self.dir_str.get(), 'backup.csv')):
            self.file_m.entryconfigure('Revert', state='normal')
        else:
            self.file_m.entryconfigure('Revert', state='disabled')
        # check if directory has changed from the one used in during commit
        if self.dir_str.get() != self.dire_commit:
            self.file_m.entryconfigure('Save', state='disabled')
            self.tb.delete('1.0', 'end')

    def save_file_conver(self):
        """ Create csv file with mapping that was last commited """
        if os.path.isfile(os.path.join(self.dire_commit, 'backup.csv')):
            if not tkMessageBox.askyesno(title='Backup file exists', message='A back up file already exists in this '
                                                                             'directory, Do you want to replace it?'):
                return

        with open(os.path.join(self.dire_commit, 'backup.csv'), 'w') as file_s:
            csv_wr = csv.writer(file_s, delimiter=',')
            for name_pair in zip(self.fl_list, self.fl_new_names):
                csv_wr.writerow(name_pair)
        self.file_m.entryconfigure('Revert', state='normal')

    def revert_conver(self):
        """using backup file undo a file name conversion"""

        # check that dir string have not been changed manually if now not valid backup file disable the revert button
        if self.dir_str.get() is "" or not os.path.isdir(self.dir_str.get()) \
                or not os.path.isfile(os.path.join(self.dir_str.get(), 'backup.csv')):
            tkMessageBox.showwarning(title="Invalid Directory", message="Please enter a valid Directory")
            self.file_m.entryconfigure('Revert', state='disabled')
            return

        old_names = []
        new_names = []
        # read from csv file and populate lists
        with open(os.path.join(self.dir_str.get(), 'backup.csv'), 'r') as file_s:
            csv_re = csv.reader(file_s, delimiter=",")
            # unzip csv values
            old_names, new_names = zip(*csv_re)
            old_names = list(old_names)
            new_names = list(new_names)

        # check if new names still match the names of the files and ask if they want to force
        current_file_names = [s.encode('ascii') for s in MainApp.file_list_sort(self.dir_str.get(), old_names[0].split('.')[-1])]
        if new_names != current_file_names:
            if tkMessageBox.askyesno(title='File name mismatch',
                                     message='The file names do not match those that where present when conversion was '
                                             'made, do you want to force conversion anyway?'):
                rn.commit_name_change(file_list=current_file_names, new_names=old_names, cwd=self.dir_str.get())
                self.tb.delete("1.0", 'end')
                for x in range(0, len(old_names)):
                    self.tb.insert(str(x + 1) + ".0", current_file_names[x] + " --> " + old_names[x] + "\n")
        else:
            print('Match')
            rn.commit_name_change(file_list=new_names, new_names=old_names, cwd=self.dir_str.get())
            # write to textbox
            self.tb.delete("1.0", 'end')
            for x in range(0, len(old_names)):
                self.tb.insert(str(x + 1) + ".0", new_names[x] + " --> " + old_names[x] + "\n")

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
