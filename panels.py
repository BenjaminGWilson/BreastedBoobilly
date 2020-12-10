# This file contains all information about the interface.

from Panel_class import Panel

def main_input():
    main = Panel()
    main.title = "Genital Counter"
    main.entries = [
        "Title",
        "Author",
        "Author's Gender",
        "Date",
    ]
    main.file_prompts = {
        "File Location": (("text file","*.txt"),("all files","*.*"))
    }
    main.buttons = {
        "About": None,
        "Wiki": None,
        "Submit": None
    }
    return main

