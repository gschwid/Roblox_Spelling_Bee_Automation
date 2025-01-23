from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

root = Tk()
root.title("Roblox Script")

# Create a frame with padding
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

# Create the Start and Stop buttons
start_button = Button(mainframe, text="Start Script")
stop_button = Button(mainframe, text="Stop Script")

# Place the buttons in the grid and make them stretch horizontally
start_button.grid(column=0, row=0, sticky="ew", padx=5)
stop_button.grid(column=1, row=0, sticky="ew", padx=5)

# Configure the columns to expand and take equal space
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Configure the row to expand as well
mainframe.rowconfigure(0, weight=1)

# Set an initial size for the window
root.geometry("400x100")  # You can adjust the size to your liking

root.mainloop()
