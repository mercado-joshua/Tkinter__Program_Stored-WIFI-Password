#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd

import subprocess
import pyperclip as pc

#===========================
# Main App
#===========================

class App(tk.Tk):
    """Main Application."""

    #------------------------------------------
    # Initializer
    #------------------------------------------
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_vars()
        self.init_UI()
        self.init_events()

    #------------------------------------------
    # Instance Variables
    #------------------------------------------
    def init_vars(self):
        self.data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        self.profiles = [i.split(':')[1][1:-1] for i in self.data if 'All User Profile' in i]

    #-------------------------------------------
    # Window Settings
    #-------------------------------------------
    def init_config(self):
        self.resizable(False, False)
        self.geometry('500x500')
        self.title('Stored Wifi Password Finder Version 1.0')
        self.iconbitmap('python.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    #-------------------------------------------
    # Window Events / Keyboard Shorcuts
    #-------------------------------------------
    def init_events(self):
        self.tree.bind('<Button-3>', self.show_popupmenu)

    #-------------------------------------------
    # Widgets / Components
    #-------------------------------------------
    def init_UI(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        fieldset = ttk.LabelFrame(self.frame, text='Get Stored Wifi Password')
        fieldset.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=15)

        fields = ('Profile Name', 'Password')
        columns = [index for index, field in enumerate(fields)]

        self.tree = ttk.Treeview(fieldset, show='headings', columns=columns, selectmode='browse')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for index, field in enumerate(fields):
            self.tree.column(index, minwidth=25, width=120, anchor=tk.E)
            self.tree.heading(index, text=field)

        self.style.configure('Treeview', rowheight=35)
        self.style.map('Treeview', background=[('selected', '#000')])

        scrollbar = ttk.Scrollbar(fieldset, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        self.popupmenu = Menu(self.tree, tearoff=0)
        self.popupmenu.add_command(label='Copy Password', command=self.copy_password)

        self.ui_refresh()

    # UI ---------------------------------------
    def ui_refresh(self):
        self.tree.delete(*self.tree.get_children())
        for i in self.profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
            results = [b.split(':')[1][1:-1] for b in results if 'Key Content' in b]

            try:
                self.tree.insert(parent='', index=tk.END, text='', values=(i, results[0]))
            except IndexError:
                mb.showerror('Error', f'No password set for {i} profile!')

    # ------------------------------------------
    def show_popupmenu(self, event):
        self.popupmenu.post(event.x_root, event.y_root)

    def copy_password(self):
        selected_row = self.tree.item(self.tree.focus())
        pc.copy(selected_row['values'][1])

#===========================
# Start GUI
#===========================

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()