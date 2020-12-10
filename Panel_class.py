import tkinter as tk
import tkinter.filedialog as fd
from functools import partial

class panel:

    def __init__(self):
        
        self.window = None

        # This attributes determine widget and frame styling.
        self.title = ""
        self.widget_pad = 4
        self.frame_pad = 0
        self.sticky = "nsew"
        self.bg = "RosyBrown1"
        self.col_a_width = 150  #
        self.col_b_width = 200
        self.text_wrap = 300
        self.borderwidth = 0
        self.relief = "sunk"
        self.text_justify = tk.CENTER
        self.column_weight = 1
        self.row_weight = 1

        # Each of these containers is a list
        self.legend = ""
        self.entries = {}       
        self.file_prompts = {}
        self.dir_prompts = []
        self.buttons = {}
        
        # Data collected through widgets is put here.
        self.variables = {}

    def overtake_window(self, window):
        window.title(self.title)
        self.as_frames_in(window)

    def as_frames_in(self, parent):
        
        self.window = parent
        widget_frames = []
        
        if self.legend:
            widget_frames.append(self.frame_legend(parent))
        if self.entries:
            widget_frames.append(self.frame_entries(parent))
        if self.file_prompts:
            widget_frames.append(self.frame_file_prompts(parent))
        if self.dir_prompts:
            widget_frames.append(self.frame_dir_prompts(parent))
        
        row_cnt = 0
        for x in widget_frames:
            self.format(x)
            x.grid(
                row = row_cnt, 
                column = 0, 
                sticky = self.sticky,
                padx = self.frame_pad,
                pady = self.frame_pad
            )
            row_cnt = row_cnt + 1
        
        self.format(parent)

    def as_popup_from(self, parent):
        pop_up = tk.Toplevel(parent)
        self.window = pop_up
        
        pop_up.title(self.title)
        pop_up.lift()
        self.as_frames_in(pop_up)
        self.format(pop_up)
        pop_up.focus()

    def frame_legend(self,parent_frame):

        frame_legend = tk.Frame(parent_frame)
        
        lbl_legend = tk.Label(
            frame_legend, 
            text = self.legend,
            bg = self.bg,
            wraplength = self.text_wrap,
            justify = self.text_justify
        )
        
        lbl_legend.grid(
            row = 0,
            sticky = self.sticky,
            pady = self.widget_pad,
            padx = self.widget_pad,
        )

        return frame_legend
    
    def frame_entries(self, parent_frame):
        
        frame_entries = tk.Frame(parent_frame)
        frame_entries.columnconfigure(0, weight = 1, minsize = self.col_a_width)
        frame_entries.columnconfigure(1, weight = 1, minsize = self.col_b_width)
        row_cnt = 0
            
        for x in self.entries:
            
            label = tk.Label(
                frame_entries, 
                text = x, 
                anchor = "e",
                bg = self.bg
            )

            entry = tk.Entry(
                frame_entries
            )

            label.grid(
                row = row_cnt, 
                column = 0, 
                sticky = self.sticky, 
                padx = self.widget_pad, 
                pady = self.widget_pad
            )

            entry.grid(
                row = row_cnt,
                column = 1,
                sticky = self.sticky,
                padx = self.widget_pad,
                pady = self.widget_pad
            )
            
            row_cnt = row_cnt + 1
        
        return frame_entries
    
    def frame_file_prompts(self, parent_frame):
        
        frame_file_prompts = tk.Frame(parent_frame)
        frame_file_prompts.columnconfigure(0, minsize = self.col_a_width)
        frame_file_prompts.columnconfigure(1, minsize = self.col_b_width)
        row_cnt = 0
    
        for x in self.file_prompts.keys():

            self.variables[x] = tk.StringVar()
            
            button = tk.Button(
                frame_file_prompts, 
                text = x,
                command = partial(self.get_file_location, x),
                bg = self.bg
            )
            button.grid(
                row = row_cnt, 
                column = 0, 
                sticky = self.sticky, 
                padx = self.widget_pad, 
                pady = self.widget_pad
            )
            label = tk.Label(
                frame_file_prompts, 
                textvariable = self.variables[x],
                wraplength = self.col_b_width,
                relief = tk.SUNKEN,
                anchor = "nw",
                justify = tk.LEFT
            )
            label.grid(
                row = row_cnt, 
                column = 1, 
                sticky = self.sticky, 
                padx = self.widget_pad, 
                pady = self.widget_pad,
            )
            

            row_cnt = row_cnt + 1
        
        return frame_file_prompts

    def frame_dir_prompts(self, parent_frame):
        frame_dir_prompts = tk.Frame(parent_frame)
        frame_dir_prompts.columnconfigure(0, minsize = self.col_a_width)
        frame_dir_prompts.columnconfigure(1, minsize = self.col_b_width)
        row_cnt = 0

        for x in self.dir_prompts:

            self.variables[x] = tk.StringVar()
            
            button = tk.Button(
                frame_dir_prompts, 
                text = x,
                command = partial(self.get_dir_location, x),
                bg = self.bg
            )
            button.grid(
                row = row_cnt, 
                column = 0, 
                sticky = self.sticky, 
                padx = self.widget_pad, 
                pady = self.widget_pad
            )
            label = tk.Label(
                frame_dir_prompts, 
                textvariable = self.variables[x],
                relief = tk.SUNKEN,
                anchor="nw",
                justify = tk.LEFT
            )
            label.grid(
                row = row_cnt, 
                column = 1, 
                sticky = self.sticky, 
                padx = self.widget_pad, 
                pady = self.widget_pad,
            )
            

            row_cnt = row_cnt + 1
        
        return frame_dir_prompts

    def format(self, frame):
        
        frame.configure(
            padx = self.frame_pad,
            pady = self.frame_pad,
            bg = self.bg,
            borderwidth = self.borderwidth,
            relief = self.relief,
        )

        numcols, numrows = frame.grid_size()

        for i in range(numcols):
            frame.columnconfigure(i, weight = self.column_weight)
                    
        for i in range(numrows):
            frame.rowconfigure(i, weight = self.row_weight)

    def get_file_location(self, widget_name):
        if self.file_prompts[widget_name] == None:
            self.file_prompts[widget_name] = (("all files", ".*"))
        file = fd.askopenfilename(
            title = widget_name,
            filetypes = self.file_prompts[widget_name])
        self.variables[widget_name].set(file)
    
    def get_dir_location(self, widget_name):
        
        directory = fd.askdirectory(
            title = widget_name
        )
        self.variables[widget_name].set(directory)
        

if __name__ == "__main__":
    
    window = tk.Tk()
    window.lift()

    
    window_widgets = panel()
    window_widgets.title = "Main Window"
    window_widgets.legend = (
        "this is the root frame. it should be all one colour, resizable in both directions,"
        " and have no visual problems"
    ) 
    window_widgets.entries =[
        "Entry"
    ]
    window_widgets.file_prompts = {
        "File Prompt": (("jpeg files","*.jpg"),("all files","*.*"))
    }
    window_widgets.dir_prompts = [
        "Directory Prompt"
    ]

    
    
    # red_popup = panel()
    # red_popup.title = "frame in red"
    # red_popup.bg = "red"
    # red_popup.legend = "This pop up tests how things look on the pop up"
    # red_popup.entries = {"Entry"}

    # red_popup.as_popup_from(window)

    # actual_app = panel()
    # actual_app.entries = {
    #         "Title": None,
    #         "Author": None,
    #         "Author's Gender": None,
    #         "Date": None,
    #     }
        
    # actual_app.file_prompts ={
    #         "File Location": None,
    #         "Database Location" : None
    #     }
        
    # actual_app.buttons = {
    #         "About": None,
    #         "Wiki": None,
    #         "Submit": None
    #     }

    # actual_app.as_popup_from(window)  
    
    window_widgets.overtake_window(window)
    window.mainloop()