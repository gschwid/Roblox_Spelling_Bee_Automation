from tkinter import *
from tkinter import ttk
from Script import Script
import threading
import time

script = Script()
thread = None

def threadStart():
    global thread
    thread = threading.Thread(target=script.startScript)
    thread.start()

def killThread():
    global thread
    script.stopScript()
    thread.join()

root = Tk()
root.title("Roblox Script")
root.geometry("500x500")

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
textVar1 = StringVar()
textVar2 = StringVar()

def checkStatus():
    global textVar1
    while True:
        textVar1.set(script.getStatusOfScript())
        time.sleep(0.5)

def checkWord():
    while True:
        textVar2.set(script.getDetectedWord())

threadStatus = threading.Thread(target=checkStatus)
threadWord = threading.Thread(target=checkWord)

threadStatus.start()

start_button = Button(mainframe, text="Start Script", command=threadStart)
stop_button = Button(mainframe, text="Stop Script", command=killThread)
label = Label(mainframe, text=f"Status of Script: ")
status = Label(mainframe, textvariable=textVar1)

label.grid(column=0, row=0, sticky="we", padx=5, pady=5)
status.grid(column=1, row=0, sticky="we", padx=5, pady=5)
start_button.grid(column=0, row=1, sticky="wens", padx=5, pady=5)
stop_button.grid(column=0, row=2, sticky="wens", padx=5, pady=5)

# Configure the mainframe columns and rows to expand
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)

# Configure the root window to allow the mainframe to expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.mainloop()
