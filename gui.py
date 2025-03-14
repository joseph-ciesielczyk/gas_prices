from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Gas Prices")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

hello = 'hello'

for i in range(5):
    for j in range(10):
        ttk.Label(mainframe, text=hello).grid(column=i, row=j, sticky=(W, E))

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
