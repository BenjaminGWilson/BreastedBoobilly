# This file contains all information needed for launching the interface.
# SQL and line splitting functions are in ________________

import tkinter as tk
from functools import partial 

from Panel_class import Panel


def input_panel():

    input_panel = Panel()
    input_panel.title = "Genital Counter"
    input_panel.entries = [
        "Title",
        "Author",
        "Author's Gender",
        "Date",
    ]
    input_panel.file_prompts = {
        "Text location": (("text file","*.txt"),("all files","*.*")),
        "Database location": (("database file", "*db"),)
    }
    input_panel.buttons = {
        "About": partial(about().as_popup_from, root),
        "Wiki": None,
        "Submit": None
    }
    return input_panel

def about():
    about = Panel()
    about.title = "About"
    about.legend = ("This is some gumph about the program"
                "and all the things it is etc etc")
    return about

root = tk.Tk()
main_input_window = input_panel()
main_input_window.overtake_window(root)
root.mainloop()
