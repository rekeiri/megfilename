#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import os


class GUI:
    def __init__(self, master, dpbox1, dpbox2, dpbox3, pat):

        self.master = master
        master.title("String Generator")
        # self.default_font = font.nametofont("TkDefaultFont")
        # self.default_font.configure(family = "Times New Roman", size = 12)

        # define all objects and variables
        self.mainframe = ttk.Frame(master, padding=(20, 20, 20, 20))
        # remove line below and uncomment the multiline comment
        # self.name = " ".join(self.read_file(pat))
        self.name = self.read_file2(pat).split("/")[1]
        # to remove spaces in front of name, and potential multiple spaces in name
        self.name = self.name.strip()  # .lstrip() removes whitespace from beginning only

        self.initials = self.name.split()
        try:
            self.initials = self.initials[0][0] + self.initials[len(self.initials) - 1][0]
            self.initials = self.initials.lower()
        except:
            print("Name does not have at least 2 words")
            self.initials = self.initials[0][0]
            self.initials = self.initials.lower()
        self.name_label = ttk.Label(self.mainframe, text="Patient Name: " + self.name)
        self.num_menu_var = StringVar()
        self.num_menu_var2 = StringVar()
        self.current_index = [0]
        self.num_menu_var.set("Current Index: 0")
        self.num_label = ttk.Label(self.mainframe, textvariable=self.num_menu_var)
        self.loc_label = ttk.Label(self.mainframe, text="Location: ")
        self.eeg_meg_label = ttk.Label(self.mainframe, text="No_EEG/MEG")
        self.first_menu_var = StringVar()
        self.first_menu_list = self.read_file(dpbox1)
        self.first_menu_var.set(self.first_menu_list[0])
        self.first_menu = OptionMenu(self.mainframe, self.first_menu_var, *self.first_menu_list)
        ''' Replace env_var_name with environment variable name
        Also, this makes the list go from 0 to env_var_name -1.
        So, to go from 1 to env_var_name, change 0 to one, and do self.num_limit + 1
 	'''
        try:
            self.num_limit = int(os.environ['MEGFILENAME_MAX_INDEX'])
            self.num_menu_list = list(range(1, self.num_limit + 1))
        except:
            # comment this bottom line out when the above lines are finished.
            self.num_menu_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.num_menu_list = ['Autopick'] + self.num_menu_list
        self.num_menu_var2.set(self.num_menu_list[0])
        self.num_menu = OptionMenu(self.mainframe, self.num_menu_var2, *self.num_menu_list)
        self.user_text = StringVar()
        self.user_text.set(self.initials)
        self.user_entry = ttk.Entry(self.mainframe, textvariable=self.user_text)
        self.loc_menu_var = StringVar()
        self.loc_menu_list = self.read_file(dpbox2)
        self.loc_menu_var.set(self.loc_menu_list[0])
        self.loc_menu = OptionMenu(self.mainframe, self.loc_menu_var, *self.loc_menu_list)
        self.eeg_meg_var = StringVar()
        self.eeg_meg_list = self.read_file(dpbox3)
        self.eeg_meg_var.set(self.eeg_meg_list[0])
        self.eeg_meg_menu = OptionMenu(self.mainframe, self.eeg_meg_var, *self.eeg_meg_list)
        self.reset_button = ttk.Button(self.mainframe, text='reset',
                                       command=lambda: self.reset(self.first_menu_var, self.num_menu_var2,
                                                                  self.user_text, self.loc_menu_var,
                                                                  self.eeg_meg_var, self.output1_text,
                                                                  self.output2_text, self.first_menu_list,
                                                                  self.num_menu_list, self.loc_menu_list,
                                                                  self.eeg_meg_list))
        self.combine_button = ttk.Button(self.mainframe, text='New String',
                                         command=lambda: self.combine(self.first_menu_var, self.num_menu_var,
                                                                      self.num_menu_var2, self.user_text,
                                                                      self.loc_menu_var,
                                                                      self.eeg_meg_var, self.output1_text,
                                                                      self.output2_text, self.current_index))
        self.exit_button = ttk.Button(self.mainframe, text='exit', command=lambda: self.exit_func(master))
        self.output1_label = ttk.Label(self.mainframe, text='SEF/MEF File String: ')
        self.output1_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))
        self.output2_label = ttk.Label(self.mainframe, text='RAW File String: ')
        self.output2_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))

        # is there a cleaner way instead of wrapping update_label inside of callback?
        self.combine_button.bind("<Button-1>", self.callback)

        # layout
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.mainframe.grid(row=1, column=1, sticky=(N, E, S, W))
        self.mainframe.columnconfigure(1, weight=1, minsize=80)  # code for each column and row of mainframe to expand
        self.mainframe.columnconfigure(2, weight=1, minsize=80)
        self.mainframe.columnconfigure(3, weight=1, minsize=80)
        self.mainframe.columnconfigure(4, weight=1, minsize=80)
        self.mainframe.columnconfigure(5, weight=1, minsize=80)
        self.mainframe.rowconfigure(1, weight=1, minsize=25)
        self.mainframe.rowconfigure(2, weight=1, minsize=25)
        self.mainframe.rowconfigure(3, weight=1, minsize=25)
        self.mainframe.rowconfigure(4, weight=1, minsize=25)
        self.mainframe.rowconfigure(5, weight=1, minsize=25)
        self.mainframe.rowconfigure(6, weight=1, minsize=25)
        self.name_label.grid(row=1, column=1, sticky=(N, E, S, W), padx=10, pady=5)
        self.num_label.grid(row=2, column=2, sticky=(N, S), padx=10, pady=5)
        self.loc_label.grid(row=2, column=4, sticky=(N, S))
        self.eeg_meg_label.grid(row=2, column=5, sticky=(N, S), padx=10, pady=5)
        self.first_menu.grid(row=3, column=1, sticky=(N, E, S, W), padx=10, pady=15)
        self.num_menu.grid(row=3, column=2, sticky=(N, E, S, W), padx=10, pady=15)
        self.user_entry.grid(row=3, column=3, sticky=(N, E, S, W), padx=10, pady=15)
        self.loc_menu.grid(row=3, column=4, sticky=(N, E, S, W), padx=10, pady=15)
        self.eeg_meg_menu.grid(row=3, column=5, sticky=(N, E, S, W), padx=10, pady=15)
        self.reset_button.grid(row=4, column=1, sticky=(N, E, S, W), padx=10, pady=15)
        self.combine_button.grid(row=4, column=2, sticky=(N, E, S, W), padx=10, pady=15)
        self.exit_button.grid(row=4, column=3, sticky=(N, E, S, W), padx=10, pady=15)
        self.output1_label.grid(row=5, column=1, sticky=(N, W, S), padx=10, pady=15)
        self.output1_text.grid(row=5, column=2, columnspan=4, sticky=(N, E, S, W), pady=15)
        self.output2_label.grid(row=6, column=1, sticky=(N, W, S), padx=10, pady=15)
        self.output2_text.grid(row=6, column=2, columnspan=4, sticky=(N, E, S, W), pady=15)

    # functions/methods

    def callback(self, event):
        self.update_label(self.num_menu_var, self.num_menu_var2, self.current_index)

        # returns a list of the words in the text file

    def read_file(self, path):
        f = open(path, "r")
        return f.read().split()

    def read_file2(self, path):
        f = open(path, "r")
        return f.read()

    def exit_func(self, root):
        root.destroy()

        # executes before combine

    def update_label(self, tkvar, tkvar2, current_index):
        prefix = "Current Index: "
        if tkvar2.get() != "Autopick":
            if (current_index[0] == int(tkvar2.get())):
                current_index[0] = current_index[0] + 1
                tkvar2.set(current_index[0])
            else:
                current_index[0] = int(tkvar2.get())
        else:
            current_index[0] = current_index[0] + 1
        tkvar.set(prefix + str(current_index[0]))

    def combine(self, dbv1, dbv2_1, dbv2, entryvar, dbv3, dbv4, text1, text2, current_index):
        text1.delete(1.0, END)  # since text is multi-line, 1.0 means line 1, char 0
        text2.delete(1.0, END)
        list_strings = [dbv1.get(), dbv2.get(), entryvar.get(), dbv3.get(), dbv4.get()]
        for i in range(len(list_strings) - 1, -1, -1):
            if list_strings[i] in ["NULL", ""]:
                del list_strings[i]
        for j in range(len(list_strings)):
            if list_strings[j] in ['Autopick']:
                list_strings[j] = str(current_index[0])
        if (dbv1.get() in ["SEF", "MEF"]):
            text1.insert(1.0, "_".join(list_strings) + "_avg")
        text2.insert(1.0, "_".join(list_strings) + "_raw")

    def reset(self, dbv1, dbv2, entryv, dbv3, dbv4, text1, text2, dbv1_list, dbv2_list, dbv3_list, dbv4_list):
        dbv1.set(dbv1_list[0])
        dbv2.set(dbv2_list[0])
        dbv3.set(dbv3_list[0])
        dbv4.set(dbv4_list[0])
        entryv.set(self.initials)
        text1.delete(1.0, END)
        text2.delete(1.0, END)
        self.current_index = [0]
        self.num_menu_var.set("Current Index: 0")


dpbox1_fname = "mfn-dropdownbox1.txt"
dpbox2_fname = "mfn-dropdownbox2.txt"
dpbox3_fname = "mfn-dropdownbox3.txt"
pat_fname = "mfn-myNames.txt"
root = Tk()
my_gui = GUI(root, dpbox1_fname, dpbox2_fname, dpbox3_fname, pat_fname)
root.mainloop()