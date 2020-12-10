import tkinter as tk

from Panel_class import Panel
import panels as p

root = tk.Tk()

main = p.main_input()
main.overtake_window(root)

root.mainloop()
