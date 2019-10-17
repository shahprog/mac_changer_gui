#!/usr/bin/env python

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import subprocess
import os
import re


class App:
    def __init__(self, master):
        self.master = master
        self.create_frame()
        self.labels()
        self.entries()
        self.buttons()
        self.set_values()

    def create_frame(self):
        self.mac_frame = LabelFrame(self.master, text='Mac Changer')
        self.mac_frame.grid(column=0, row=1, sticky='ew', padx=10, pady=5)
        self.mac_frame.columnconfigure(0, weight=1)

        self.interface_frame = LabelFrame(self.master, text='Interface')
        self.interface_frame.grid(column=0, row=0, sticky='ew', padx=10, pady=5)
        self.interface_frame.columnconfigure(0, weight=1)


        self.labelentryframe = Frame(self.mac_frame)
        self.labelentryframe.grid(column=0,row=1, sticky='ew')
        self.labelentryframe.columnconfigure(0, weight=1)

        self.button_frame = Frame(self.mac_frame)
        self.button_frame.grid(row=2, column=0, sticky='ew')
        self.button_frame.columnconfigure(1, weight=1)


    def labels(self):
        self.current_mac_label = Label(self.labelentryframe, text='Current MAC')
        self.new_mac_label = Label(self.labelentryframe, text='New Mac')

        self.current_mac_label.grid(column=0, row=0, sticky='E', padx=5, pady=3)
        self.current_mac_label.columnconfigure(0, weight=1)

        self.new_mac_label.grid(column=0, row=1, sticky='E', padx=5, pady=3)
        self.new_mac_label.columnconfigure(1, weight=1)

        self.interface_lebel = Label(self.interface_frame, text='Interface')
        self.interface_lebel.grid(column=0, row=0, sticky='E')

        # make combobox for interface
        self.all_interfaces = os.listdir('/sys/class/net/')
        self.interface_combo = ttk.Combobox(self.interface_frame, values=self.all_interfaces)
        self.interface_combo.grid(column=1, row=0, padx=5, pady=3)
        self.interface_combo.current(1)

        self.get_button = Button(self.interface_frame, text='Get', command=self.set_values)
        self.get_button.grid(column=2, row=0, padx=3, pady=3)

    def set_values(self):
        if self.interface_combo.get() not in self.all_interfaces:
            messagebox.showerror('Interface Error', 'This interface is invalid')
            self.interface_combo.current(1)

        self.current_mac = StringVar()
        self.current_mac.set(self.get_current_mac())
        self.current_mac_entry.config(textvariable=self.current_mac)

        if self.current_mac.get() == 'None':
            self.new_mac_entry.config(state='disabled')
            self.new_mac_entry2.config(state='disabled')
            self.new_mac_entry3.config(state='disabled')
            self.new_mac_entry4.config(state='disabled')
            self.new_mac_entry5.config(state='disabled')
            self.new_mac_entry6.config(state='disabled')
            self.clear_all()
            self.change_button.config(state='disabled')
        else:
            self.new_mac_entry.config(state='normal')
            self.new_mac_entry2.config(state='normal')
            self.new_mac_entry3.config(state='normal')
            self.new_mac_entry4.config(state='normal')
            self.new_mac_entry5.config(state='normal')
            self.new_mac_entry6.config(state='normal')
            self.change_button.config(state='normal')


    def entries(self):
        self.current_mac_entry = Entry(self.labelentryframe, state='readonly')

        self.fp = StringVar()
        self.sp = StringVar()
        self.tp = StringVar()
        self.frp = StringVar()
        self.fvp = StringVar()
        self.sxp = StringVar()

        self.new_mac_entry =  Entry(self.labelentryframe, width=3, textvariable=self.fp)
        self.new_mac_entry2 = Entry(self.labelentryframe, width=3, textvariable=self.sp)
        self.new_mac_entry3 = Entry(self.labelentryframe, width=3, textvariable=self.tp)
        self.new_mac_entry4 = Entry(self.labelentryframe, width=3, textvariable=self.frp)
        self.new_mac_entry5 = Entry(self.labelentryframe, width=3, textvariable=self.fvp)
        self.new_mac_entry6 = Entry(self.labelentryframe, width=3, textvariable=self.sxp)

        self.current_mac_entry.grid(column=1, row=0, sticky='EW',columnspan=6, padx=5, pady=3)
        self.current_mac_entry.columnconfigure(2, weight=6)

        self.new_mac_entry.grid(column=1, row=1, sticky='EW', padx=5, pady=3)
        self.new_mac_entry.columnconfigure(3, weight=1)

        self.new_mac_entry2.grid(column=2, row=1, sticky='EW', padx=5, pady=3)
        self.new_mac_entry2.columnconfigure(4, weight=1)

        self.new_mac_entry3.grid(column=3, row=1, sticky='EW', padx=5, pady=3)
        self.new_mac_entry3.columnconfigure(5, weight=1)

        self.new_mac_entry4.grid(column=4, row=1, sticky='EW', padx=5, pady=3)
        self.new_mac_entry4.columnconfigure(6, weight=1)

        self.new_mac_entry5.grid(column=5, row=1, sticky='EW', padx=5, pady=3)
        self.new_mac_entry5.columnconfigure(7, weight=1)

        self.new_mac_entry6.grid(column=6, row=1, sticky='EW', padx=5, pady=3)
        self.new_mac_entry6.columnconfigure(8, weight=1)

    def buttons(self):
        self.change_button = Button(self.button_frame, text='Change', command=self.set_new_mac)
        self.clear_button = Button(self.button_frame, text='Clear', command=self.clear_all)
        self.exit_button = Button(self.button_frame, text='Exit', command=self._exit)

        self.change_button.grid(column=0, row=0, padx=2, pady=2)

        self.clear_button.grid(column=1, row=0, padx=0, pady=2)

        self.exit_button.grid(column=2, row=0, padx=2, pady=2)

    def get_current_mac(self):
        try:
            ifconfig_result = subprocess.check_output(["ifconfig", self.interface_combo.get()])
            get_mac_by_search = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result.decode('utf-8'))
            return get_mac_by_search.group()
        except:
            return None

    def set_new_mac(self):
        if self.fp.get() == '' or self.sp.get() == '' or self.tp.get() == '' or self.frp.get() == '' or self.fvp.get() == '' or self.sxp.get() == '':
            messagebox.showwarning('Empty', 'Please fill al the input Boxes')
        else:
            if len(self.fp.get()) == 2 and len(self.sp.get()) == 2 and len(self.tp.get()) == 2 and len(self.frp.get()) == 2 and len(self.fvp.get()) == 2 and len(self.sxp.get()) == 2:
                self.new_mac = ':'.join([self.fp.get(), self.sp.get(), self.tp.get(), self.frp.get(), self.fvp.get(), self.sxp.get()])

                self.validate_mac()
            else:
                messagebox.showinfo('Invalid', 'Please fill each input box with valid input')

    def clear_all(self):
        self.fp.set('')
        self.sp.set('')
        self.tp.set('')
        self.frp.set('')
        self.fvp.set('')
        self.sxp.set('')

    def validate_mac(self):
        # Use regex to search a string
        self.is_any_mac = re.search(r'((([a-fA-F0-9][a-fA-F0-9]+[-]){5}|([a-fA-F0-9][a-fA-F0-9]+[:]){5})([a-fA-F0-9][a-fA-F0-9])$)|(^([a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]+[.]){2}([a-fA-F0-9][a-fA-F0-9][a-fA-F0-9][a-fA-F0-9]))', self.new_mac)
        if self.is_any_mac.group() is not None:
            self.new_mac = self.is_any_mac.group()
            self.change_mac()
        else:
            messagebox.showerror('Error', 'Please enter a valid mac')

    def change_mac(self):
        subprocess.call(["ifconfig", self.interface_combo.get(), "down"])
        subprocess.call(["ifconfig", self.interface_combo.get(), "hw", "ether", self.new_mac])
        subprocess.call(["ifconfig", self.interface_combo.get(), "up"])
        if self.get_current_mac() == self.new_mac:
            self.current_mac.set(self.new_mac)
            self.clear_all()
            messagebox.showinfo('Changed', 'MAC Address changed successfully')

    def _exit(self):
        self.ans = messagebox.askquestion('Exit', 'Exit this program?')
        if self.ans == 'yes':
            self.master.quit()
            self.master.destroy()
            exit()

root = Tk()
root.title('Mac Changer')
root.resizable(0,0)
root.columnconfigure(0, weight=7)
app = App(root)
root.mainloop()
