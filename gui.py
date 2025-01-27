from tkinter import *
from tkinter import ttk
from Script import Script
import threading
import time
import sv_ttk

# Initialize the script and global variables
script = Script()
scriptThread = threading.Thread(target=script.startScript, daemon=True)
checkStatusRunning = True
checkWordRunning = True
scriptStarted = False

def threadStart():
    """Start the script in a new thread."""
    global scriptThread
    global scriptStarted
    if not scriptStarted:
        scriptThread = threading.Thread(target=script.startScript, daemon=True)
        scriptThread.start()
        scriptStarted = True

def killThread():
    """Stop the script and gracefully handle the thread."""
    global scriptStarted
    try:
        script.stopScript()
        scriptStarted = False
    except:
        print("Thread not running")

def checkStatus():
    """Update the status of the script periodically."""
    while checkStatusRunning:
        statusVar.set(script.getStatusOfScript())
        time.sleep(0.1)

def checkWord():
    """Update the detected word periodically."""
    while checkWordRunning:
        wordVar.set(script.getDetectedWord())
        time.sleep(0.1)

def onClosing():
    """Handle application closing and cleanup resources."""
    global threadStatus
    global threadWord
    global checkWordRunning
    global checkStatusRunning
    checkWordRunning = False
    checkStatusRunning = False
    killThread()
    threadStatus.join()
    threadWord.join()
    Script._audioHandler.releaseAudioResources()
    root.destroy()
    print("Shutting down...")

# Initialize the root window
root = Tk()
root.title("Roblox Script Controller")
root.geometry("600x400")

# Main container frame
mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Define variables for dynamic updates
statusVar = StringVar(value="Script is off.")
wordVar = StringVar(value="")

# Title Label
title_label = Label(mainframe, text="Roblox Script Controller", font=("Arial", 16, "bold"))
title_label.grid(column=0, row=0, columnspan=2, pady=(0, 20))

# Status Frame
status_frame = ttk.Frame(mainframe, padding="5 5 5 5")
status_frame.grid(column=0, row=1, columnspan=2, sticky=(W, E))

status_label = Label(status_frame, text="Status of Script:", anchor="w", font=("Arial", 12, "bold"))
status_label.grid(column=0, row=0, sticky="w", padx=(5, 10))
status_value = Label(status_frame, textvariable=statusVar, anchor="w", font=("Arial", 12))
status_value.grid(column=1, row=0, sticky="w")

word_label = Label(status_frame, text="Detected Word:", anchor="w", font=("Arial", 12, "bold"))
word_label.grid(column=0, row=1, sticky="w", padx=(5, 10), pady=(10, 0))
word_value = Label(status_frame, textvariable=wordVar, anchor="w", font=("Arial", 12))
word_value.grid(column=1, row=1, sticky="w", pady=(10, 0))

# Button Frame
button_frame = ttk.Frame(mainframe, padding="5 5 5 5")
button_frame.grid(column=0, row=2, columnspan=2, pady=(20, 0))

start_button = Button(button_frame, text="Start Script", command=threadStart, font=("Arial", 12))
start_button.grid(column=0, row=0, padx=(0, 10))

stop_button = Button(button_frame, text="Stop Script", command=killThread, font=("Arial", 12))
stop_button.grid(column=1, row=0)

# Configure weights for responsiveness
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)

status_frame.columnconfigure(0, weight=1)
status_frame.columnconfigure(1, weight=2)

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Threads for background tasks
threadStatus = threading.Thread(target=checkStatus, daemon=True)
threadWord = threading.Thread(target=checkWord, daemon=True)
threadStatus.start()
threadWord.start()

# Handle window close event
root.protocol("WM_DELETE_WINDOW", onClosing)

# Apply dark theme
sv_ttk.set_theme("dark")

root.mainloop()
