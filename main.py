# This file contains all information needed to describe the GUI
# input checking etc is in input_checks

# Text analysis 

import tkinter as tk
from functools import partial 

from Panel_class import Panel

root = tk.Tk()

def launch_gui():
    panels = make_gui_panels()
    panels["input_panel"].overtake_window(root)
    root.mainloop()

def make_gui_panels():
    panels = [
        "input_panel",      #this is the main window
        "about",            #general information about the program/company
        "incomplete_warning"    #warns there are empty inputs
    ]
    panels = dict.fromkeys(panels, Panel())
    
    # format pop ups before the window that calls them, else you call a blank window
    panels["incomplete_warning"] = make_incomplete_warning()
    panels["about"] = make_about()
    panels["input_panel"] = make_input_panel(panels)


    return panels

def make_input_panel(panels): 
    panel = Panel()
    panel.title = "Genital Counter"
    panel.entries = [
        "Title",
        "Author",
        "Author's Gender",
        "Date",
    ]
    panel.file_prompts = {
        "Text location": (("text file","*.txt"),("all files","*.*")),
        "Database location": (("database file", "*db"),)
    }
    panel.buttons = {
        "About": partial(panels["about"].as_popup_from, root),
        "Wiki": partial(panels["incomplete_warning"].as_popup_from,root),
        "Submit": partial(submit_input, panel)
    }
    return panel

def make_about():
    about = Panel()
    about.title = "About"
    about.legend = ("This is some gumph about the program"
                "and all the things it is etc etc")
    about.buttons = {
        "close program test": about.destroy
    }
    return about

def make_incomplete_warning():
    incomplete_warning = Panel()
    incomplete_warning.legend = "There are empty fields. Do you want to continue"
    incomplete_warning.buttons = {
        "Yes": incomplete_warning.destroy, 
        "No": incomplete_warning.destroy
    }
    return incomplete_warning

def submit_input(input_panel):
    
    user_input = [
        "Title",
        "Author",
        "Author's Gender",
        "Date",
        "Text location",
        "Database location"   
    ]
    user_input = dict.fromkeys(user_input)
    
    for x in user_input:
        user_input[x] = input_panel.variables[x].get()


launch_gui()