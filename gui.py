from tkinter import *
from tkinter import ttk
from Script import Script
import threading
import time

script = Script()
scriptThread = threading.Thread(target=script.startScript)
checkStatusRunning = True
checkWordRunning = True

def threadStart():
    global scriptThread
    scriptThread = threading.Thread(target=script.startScript)
    scriptThread.start()

def killThread():
    global scriptThread
    try:
        script.stopScript()
        scriptThread.join()
    except:
        print("Thread not running")

def checkStatus():
    global statusVar
    while checkStatusRunning:
        statusVar.set(script.getStatusOfScript())
        time.sleep(0.1)

def checkWord():
    while checkWordRunning:
        wordVar.set(script.getDetectedWord())
        time.sleep(0.1)

def onClosing():
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
    print("shutting down..")

root = Tk()
root.title("Roblox Script")
root.geometry("500x500")

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
statusVar = StringVar()
wordVar = StringVar()

threadStatus = threading.Thread(target=checkStatus)
threadWord = threading.Thread(target=checkWord)

start_button = Button(mainframe, text="Start Script", command=threadStart)
stop_button = Button(mainframe, text="Stop Script", command=killThread)
statusLabel = Label(mainframe, text=f"Status of Script: ")
status = Label(mainframe, textvariable=statusVar)
wordLabel = Label(mainframe, text=f"Detected word: ")
word = Label(mainframe, textvariable=wordVar)


statusLabel.grid(column=0, row=0, sticky="we", padx=5, pady=5)
status.grid(column=1, row=0, sticky="we", padx=5, pady=5)
start_button.grid(column=0, row=2, sticky="wens", padx=5, pady=5)
stop_button.grid(column=1, row=2, sticky="wens", padx=5, pady=5)
wordLabel.grid(column=0, row=1, sticky="we", padx=5, pady=5)
word.grid(column=1, row=1, sticky="we", padx=5, pady=5)

# Configure the mainframe columns and rows to expand
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)

# Configure the root window to allow the mainframe to expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

threadStatus.start()
threadWord.start()

root.protocol("WM_DELETE_WINDOW", onClosing)

root.mainloop()
