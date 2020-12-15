# This file contains all information needed to describe the GUI
# input checking etc is in input_checks

# Text analysis 

import tkinter as tk
from functools import partial 

from Panel_class import Panel

# globals
root = tk.Tk()
user_input = {}
panels = {}

def launch_gui():
    global panels
    panels = make_gui_panels()
    panels["input_panel"].overtake_window(root)
    root.mainloop()

def make_gui_panels():
    panels = [
        "input_panel",      # this is the main window
        "about",            # general information about the program/company
        "incomplete_warning",    # warns there are empty inputs
        "missing_essential",     # warns essential information hasn't been input
        "new_db_prompt",    # if user doesn't suggest a db, this prompts them to make a new one      

    ]
    panels = dict.fromkeys(panels, Panel())
    
    # format pop ups before the window that calls them, else you call a blank window
    panels["new_db_prompt"] = make_new_db_prompt()
    panels["missing_essential"] = make_missing_essential()
    panels["incomplete_warning"] = make_incomplete_warning(panels)
    panels["about"] = make_about()
    panels["input_panel"] = make_input_panel(panels)


    return panels

def make_input_panel(panels): 
    panel = Panel()
    panel.title = "Genital Counter"
    panel.entries = [
        "Title",
        "Author",
        "Author's gender",
        "Date",
    ]
    panel.file_prompts = {
        "Text location": (("text file","*.txt"),("all files","*.*")),
        "Database location": (("database file", "*db"),)
    }
    panel.buttons = {
        "About": partial(panels["about"].as_popup_from, root),
        "Wiki": None,
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

def make_incomplete_warning(panels):
    def next_window(this_window):
        this_window.destroy()
        if database_field_empty() == True:
            panels["new_db_prompt"].as_popup_from(root)
        else:
            process_text
    
    incomplete_warning = Panel()
    incomplete_warning.legend = "There are empty fields. Do you want to continue"
    incomplete_warning.buttons = {
        "Yes": partial(next_window,incomplete_warning), 
        "No": incomplete_warning.destroy
    }
    return incomplete_warning

def make_missing_essential():
    missing_essential = Panel()
    missing_essential.legend = ("Please fill in the the title and location"
                                " of the text you want to analyse.")
    missing_essential.buttons = {
        "Ok": missing_essential.destroy, 
    }
    return missing_essential

def make_new_db_prompt():

    def next_window(this_window):
        new_db_location =   (this_window.variables["Choose directory"].get() 
                            + "/"
                            + this_window.variables["New database name"].get())
        panels["input_panel"].set(new_db_location)
        this_window.destroy()

    new_db_prompt = Panel()
    new_db_prompt.legend = ("You haven't named a database to store your results in."
                            " Would you like to make a new one?")
    new_db_prompt.entries = ("New database name",)
    new_db_prompt.dir_prompts = ("Choose directory",)
    new_db_prompt.buttons = {
        "Yes": partial(next_window, new_db_prompt),
        "No": new_db_prompt.destroy
    }
    return new_db_prompt

def submit_input(input_panel):
    global user_input
    user_input = dict.fromkeys(input_panel.variables)
    for x in user_input:
        user_input[x] = input_panel.variables[x].get()
        if len(user_input[x]) < 1:
            user_input[x] = None

    check_essential_fields()

def check_essential_fields():
    essential_fields = ("Title", "Text location")
    for x in essential_fields:
        if user_input[x] == None:
            panels["missing_essential"].as_popup_from(root)
            return
    check_optional_fields()

def check_optional_fields():
    optional_fields = ("Author", "Author's gender", "Date")
    for x in optional_fields:
        if user_input[x] == None:
            panels["incomplete_warning"].as_popup_from(root)
            return

def database_field_empty():
    if user_input["Database location"] == None:
        return True
    else:
        return False

def process():
    print(user_input)
        

launch_gui()