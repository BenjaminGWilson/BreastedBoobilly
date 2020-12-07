# TODO

# check inputs
# 	do files exist? do they need making
# 	is it a duplicate entry?

# load dictionary
# load body_dictionary
# read text
# 	how to deal with punctuation?
# 	list of mystery words
# empty text to db
# output analysis
# 	how many possesive sentences per gender?
# 	how much of each gender was made up of body? (bodillyness rating)
# 	how was each body made up?
# 	how much more bodily was it than other things in the database?
# 	generate charts

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

"""

import tkinter as tk
import tkinter.filedialog as tkfile
from functools import partial
import sqlite3
from sqlite3 import Error
import os.path
from os import path

class Input_Window:
    def __init__(self):
        
        self.master = tk.Tk()
        self.master.title("Genital Counter")
        self.master.columnconfigure(0, weight = 1)
        
        self.internal_col_width = 130
        self.frame_padding = 3

        frame_text_inputs = tk.Frame()
        frame_buttons = tk.Frame()
        frame_file_prompts = tk.Frame()

        frame_text_inputs.columnconfigure((0,1), minsize = self.internal_col_width, weight = 1)
        frame_file_prompts.columnconfigure((0,1), minsize = self.internal_col_width, weight = 1)
        frame_buttons.columnconfigure((0,1,2), weight = 1)

        
        inputs = {
            "Title": None,
            "Author": None,
            "Author's Gender": None,
            "Date": None,
        }
        
        file_prompts ={
            "File Location": self.set_file_location,
            "Database Location" : self.set_database_location
        }
        
        buttons = {
            "About": None,
            "Wiki": None,
            "Submit": self.check_form_completion
        }
        
        self.file_prompt_variables_for_widgets = self.make_file_prompts(file_prompts, frame_file_prompts)
        self.inputs = self.make_submission_form(inputs, frame_text_inputs)
        self.buttons = self.make_button_panel(buttons, frame_buttons)

        frame_text_inputs.grid(row = 0, column = 0, sticky = "NESW", padx = self.frame_padding, pady = self.frame_padding)
        frame_file_prompts.grid(row = 1, column = 0, sticky = "NESW", padx = self.frame_padding, pady = self.frame_padding)
        frame_buttons.grid(row = 2, column = 0, padx = self.frame_padding, pady = self.frame_padding)
    
    def make_submission_form(self, inputs, frame): 
    # populates a frame with entry spaces, returns a list of those entry spaces
        
        row_cnt = 0
        for x in inputs.keys():
            tk.Label(frame, text = x, anchor = "e").grid(row = row_cnt, column = 0, sticky = "NESW", padx = self.frame_padding, pady = self.frame_padding)
            inputs[x] = tk.Entry(frame)
            inputs[x].grid(row = row_cnt, column = 1, sticky = "NESW", padx = self.frame_padding, pady = self.frame_padding)
            row_cnt = row_cnt + 1

        return inputs

    def make_file_prompts(self, file_prompts, frame): 
    #populates a frame with file prompts, returns list of their linked StringVar()
        
        row_cnt = 0
        for x in file_prompts.keys():
            tk.Button(
                frame, 
                text = x,
                command = file_prompts[x]
            ).grid(row = row_cnt, column = 0, sticky = "E", padx = self.frame_padding, pady = self.frame_padding)
            
            file_prompts[x] = tk.StringVar(value = "...select file...")
            
            tk.Label(
                frame, 
                textvariable = file_prompts[x],
                relief = tk.SUNKEN,
                bg = "white"
            ).grid(row = row_cnt, column = 1, sticky = "NESW", padx = self.frame_padding, pady = self.frame_padding)
            
            row_cnt = row_cnt + 1

        return file_prompts 
    
    def make_button_panel(self, buttons, frame): 
    # populates a frame with buttons, returns a list of those buttons
        
        col_cnt = 0
        for x in buttons.keys():
            buttons[x] = tk.Button(frame, text = x, command = buttons[x])
            buttons[x].grid(row = 0, column = col_cnt, padx = self.frame_padding, pady = self.frame_padding)
            col_cnt = col_cnt + 1

        return buttons

    def set_file_location(self):
        
        path = tkfile.askopenfilename(
            title = 'select', 
            filetypes =[("*.txt", ".txt")]
        )
       
        if len(path) > 0:
            self.file_location = path 
            self.file_prompt_variables_for_widgets["File Location"].set(path)
    
    def set_database_location(self):
        path = tkfile.askopenfilename(
            title = 'select', 
            filetypes =[("*.db", ".db")]
        )
       
        if len(path) > 0:
            self.database_location = path 
            self.file_prompt_variables_for_widgets["Database Location"].set(path)

    def check_form_completion(self):
    
        for x in self.inputs:
            if len(self.inputs[x].get()) < 1:
                pop_up = tk.Toplevel(self.master)
                pop_up.focus_force()
                buttons = {
                    "Yes": lambda:[pop_up.destroy(),self.does_file_exist()],
                    "No": pop_up.destroy
                    }
                self.fill_pop_up("There are empty fields; do you want to continue?", buttons, pop_up)
                break
            else: 
                self.does_file_exist
    
    def does_file_exist(self):
        
        if hasattr(self, "file_location") == False:
            pop_up = tk.Toplevel(self.master)
            pop_up.focus_force()
            buttons = {
                "Okay": pop_up.destroy
                }
            self.fill_pop_up("Please supply a file to analyse.", buttons, pop_up)
        
        elif hasattr(self, "database_location") == False:
            pop_up = tk.Toplevel(self.master)
            pop_up.focus_force()
            buttons = {
                "Add existing database": pop_up.destroy,
                "Create new database": lambda: [pop_up.destroy, self.new_database_dialog()], 
                "Skip database export": pop_up.destroy
            }
            self.fill_pop_up(
                "You haven't supplied a database, what would you like to do? ", 
                buttons, pop_up)            
            
    def fill_pop_up(self, text, buttons, window):
        frame_buttons_warning = tk.Frame(window)
        warning = tk.Label(window, text = text)
        self.make_button_panel(buttons, frame_buttons_warning)
        warning.grid(row = 0)
        frame_buttons_warning.grid(row = 1)

    def new_database_dialog(self):
        pop_up = tk.Toplevel(self.master)
        
        frame1 = tk.Frame(pop_up)
        frame2 = tk.Frame(pop_up)
        frame3 = tk.Frame(pop_up)
        
        directory_requests = {
            "Database Folder Location": self.ask_for_db_folder_dialog
        }
        inputs = {
            "New Database Name": None
        }
        buttons = {
            "Exit": pop_up.destroy,
            "Create new database":self.make_new_database
        }

        self.dir_prompt_variables_for_widgets = self.make_dir_prompts(directory_requests, frame1)
        self.inputs.update(self.make_submission_form(inputs, frame2))
        self.buttons.update(self.make_button_panel(buttons, frame3))

        frame1.grid(row = 0)
        frame2.grid(row = 1)
        frame3.grid(row = 2)

    def make_new_database(self):
        directory = self.dir_prompt_variables_for_widgets["Database Folder Location"].get()
        filename = self.inputs["New Database Name"].get()

        if path.isdir(directory) == False or len(filename) < 1:
            return
        
        new_db = directory + "/" + filename + ".db"
        
        try:
            db_obj = sqlite3.connect(new_db)
            self.database_location = new_db
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if db_obj:
                db_obj.close()
        

    def make_dir_prompts(self, dir_prompts, frame): 
    #populates a frame with dir prompts, returns list of their linked StringVar()
        
        row_cnt = 0
        for x in dir_prompts.keys():
            tk.Button(
                frame, 
                text = x,
                command = dir_prompts[x]
            ).grid(row = row_cnt, column = 0, sticky = "E", padx = self.frame_padding, pady = self.frame_padding)
            
            dir_prompts[x] = tk.StringVar(value = "...select directory...")
            
            tk.Label(
                frame, 
                textvariable = dir_prompts[x],
                relief = tk.SUNKEN,
                bg = "white"
            ).grid(row = row_cnt, column = 1, sticky = "NESW", padx = self.frame_padding, pady = self.frame_padding)
            
            row_cnt = row_cnt + 1

        return dir_prompts 
    
    def ask_for_db_folder_dialog(self):
        
        folder = tkfile.askdirectory(title = 'select')
        self.dir_prompt_variables_for_widgets["Database Folder Location"].set(folder)

def main():
    
    app = Input_Window()
    app.master.mainloop()

main()