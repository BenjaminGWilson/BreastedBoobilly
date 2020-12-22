"""
This program searches through long form text (ie novels) for use of
possesive pronouns (ie his, her, their). When it finds one it tries
to work out whether it's a body part that's being owned. If it is
a body part then the program records that against the pronoun.

Once a full count is complete the program does some basic analysis
of the numbers and then presents graphed summaries of it's findings.

The user has the option to export all data to a database, allowing
in depth and intertextual analysis via SQL.

If you use this program in your research, please let me know!
Information about correct referencing can be found in the 'About'
panel.

If you want to edit the code, and anything isn't clear here, there's a
map of the code in the documentation.

Programmed by Rhetorical Figures (Benjamin G. Wilson)

This file mostly contains instructions for the GUI and input checks.
The Panel module realises these instructions as tkinter widgets.
Text processing and SQL commands live in the text_analysis module.

"""

# standard modules
import tkinter as tk
from functools import partial

# local modules
from Panel_class import Panel
import text_analysis as text

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
        "missing_db_prompt",    # if user doesn't suggest a db, this prompts them to make a new one
        "new_database",  # prompts for location and title of new database
        "processing"    # screen to look at as data is processed

    ]
    panels = dict.fromkeys(panels, Panel())

    # format pop ups before the window that calls them, else you call a blank window
    panels["processing"] = make_processing()
    panels["new_database"] = make_new_database()
    panels["missing_db_prompt"] = make_missing_db_prompt()
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
        "Text location": (("text file", "*.txt"), ("all files", "*.*")),
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
    def next_window(this_panel):
        this_panel.destroy()
        if database_field_empty() == True:
            panels["missing_db_prompt"].as_popup_from(root)
        else:
            process()

    incomplete_warning = Panel()
    incomplete_warning.legend = "There are empty fields. Do you want to continue"
    incomplete_warning.buttons = {
        "Yes": partial(next_window, incomplete_warning),
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


def make_missing_db_prompt():
    def yes_button(this_window):
        this_window.destroy()
        panels["new_database"].as_popup_from(root)

    def no_button(this_window):
        this_window.destroy()
        process()

    missing_db_prompt = Panel()
    missing_db_prompt.legend = ("You haven't named a database to store your results in."
                                " Would you like to make a new one?")
    missing_db_prompt.buttons = {
            "Yes": partial(yes_button, missing_db_prompt),
            "No, I'll link to an existing database": missing_db_prompt.destroy,
            "No, I don't want to export to a database": partial(no_button, missing_db_prompt)
        }
    missing_db_prompt.sticky = ""
    return missing_db_prompt


def make_new_database():
    def next_window(this_panel):
        new_db_location = (this_panel.variables["Choose directory"].get()
                            + "/"
                            + this_panel.variables["New database name"].get())
        panels["input_panel"].variables["Database location"].set(
            new_db_location)
        this_panel.destroy()

    new_database = Panel()
    new_database.dir_prompts = ("Choose directory",)
    new_database.entries = ("New database name",)
    new_database.buttons = {
        "Create new database": partial(next_window, new_database),
        "Cancel": new_database.destroy
    }
    return new_database


def make_processing():
    processing = Panel()

    processing.changing_text_display = [
        "Length of text:",
        "Words processed:",
        "Current word:",
    ]

    return processing

def submit_input(input_panel):
    global user_input
    user_input= dict.fromkeys(input_panel.variables)
    for x in user_input:
        user_input[x]= input_panel.variables[x].get()
        if len(user_input[x]) < 1:
            user_input[x]= None

    check_essential_fields()

def check_essential_fields():
    essential_fields= ("Title", "Text location")
    for x in essential_fields:
        if user_input[x] == None:
            panels["missing_essential"].as_popup_from(root)
            return
    check_optional_fields()

def check_optional_fields():
    optional_fields= ("Author", "Author's gender", "Date")
    for x in optional_fields:
        if user_input[x] == None:
            panels["incomplete_warning"].as_popup_from(root)
            return
    if database_field_empty() == True:
        panels["missing_db_prompt"].as_popup_from(root)
    else:
        process()

def database_field_empty():
    if user_input["Database location"] == None:
        return True
    else:
        return False

def process():
    panels["processing"].as_popup_from(root)
    text.read(user_input, panels["processing"].variables)


launch_gui()
