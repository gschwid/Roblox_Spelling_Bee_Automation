from tkinter import *
from tkinter import ttk
from Script import Script

script = Script()

root = Tk()
root.title("Roblox Script")
root.geometry("500x500")

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

start_button = Button(mainframe, text="Start Script", command=script.startScript)
stop_button = Button(mainframe, text="Stop Script", command=script.stopScript)

start_button.grid(column=0, row=0, sticky="wens", padx=5, pady=5)
stop_button.grid(column=0, row=1, sticky="wens", padx=5, pady=5)

# Configure the mainframe columns and rows to expand
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)

# Configure the root window to allow the mainframe to expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
