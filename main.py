# This file contains all information needed to describe the GUI
# input checking etc is in input_checks

# Text analysis 

import tkinter as tk
from functools import partial 

from Panel_class import Panel

"""
how about:
initialise list of GUI panels
turn list into dict, value = Panel()
send dict to a module function that formats everything
"""
def make_input_panel():

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
        "About": partial(make_about().as_popup_from, root),
        "Wiki": None,
        "Submit": None
    }
    return input_panel

def make_about():
    about = Panel()
    about.title = "About"
    about.legend = ("This is some gumph about the program"
                "and all the things it is etc etc")
    # about.buttons = {
    #     "close program test": input_panel.destroy
    # }

    #this blanked out till dictionarising is done
    return about

root = tk.Tk()
input_panel = make_input_panel()
input_panel.overtake_window(root)
root.mainloop()
