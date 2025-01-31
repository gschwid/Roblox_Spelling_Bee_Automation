from tkinter import *
from tkinter import ttk
from Script import Script
import threading
import time
import sv_ttk

class Gui:
    
    _script = Script()
    _scriptThread = threading.Thread(target=_script.startScript, daemon=True)
    _checkStatusRunning = True
    _checkWordRunning = True
    _scriptStarted = False
    _root = Tk()
    _statusVar = StringVar(value="Script is off.")
    _wordVar = StringVar(value="")
    
    def __init__(self):
        self._threadStatus = threading.Thread(target=self.checkScriptStatus, daemon=True)
        self._threadWord = threading.Thread(target=self.checkDetectedWord, daemon=True)

    def startScriptThread(self):
        """Start the Roblox script in a new thread."""
        if not self._scriptStarted:
            scriptThread = threading.Thread(target=self._script.startScript, daemon=True)
            scriptThread.start()
            self._scriptStarted = True

    def killScriptThread(self):
        """Stop the script and handle the thread."""
        try:
            self._script.stopScript()
            self._scriptStarted = False
        except:
            print("Thread not running")

    def checkScriptStatus(self):
        """Update the status of the script to display on the Gui"""
        while self._checkStatusRunning:
            self._statusVar.set(self._script.getStatusOfScript())
            time.sleep(0.1)

    def checkDetectedWord(self):
        """Update the detected word periodically to display on the Gui"""
        while self._checkWordRunning:
            self._wordVar.set(self._script.getDetectedWord())
            time.sleep(0.1)

    def onClosing(self):
        """Handle application closing and cleanup resources."""
        self._checkWordRunning = False
        self._checkStatusRunning = False
        self.killScriptThread()
        self._threadStatus.join()
        self._threadWord.join()
        self._script._audioHandler.releaseAudioResources()
        self._root.destroy()
        print("Shutting down...")


    def initializeGui(self):
        """
        Initialize the Gui for the roblox spelling bee script.
        """
        self._root.title("Roblox Script Controller")
        self._root.geometry("600x400")

        # Main container frame
        mainframe = ttk.Frame(self._root, padding="10 10 10 10")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        # Title Label
        title_label = Label(mainframe, text="Roblox Script Controller", font=("Arial", 16, "bold"))
        title_label.grid(column=0, row=0, columnspan=2, pady=(0, 20))

        # Status Frame
        status_frame = ttk.Frame(mainframe, padding="5 5 5 5")
        status_frame.grid(column=0, row=1, columnspan=2, sticky=(W, E))

        status_label = Label(status_frame, text="Status of Script:", anchor="w", font=("Arial", 12, "bold"))
        status_label.grid(column=0, row=0, sticky="w", padx=(5, 10))
        status_value = Label(status_frame, textvariable=self._statusVar, anchor="w", font=("Arial", 12))
        status_value.grid(column=1, row=0, sticky="w")

        word_label = Label(status_frame, text="Detected Word:", anchor="w", font=("Arial", 12, "bold"))
        word_label.grid(column=0, row=1, sticky="w", padx=(5, 10), pady=(10, 0))
        word_value = Label(status_frame, textvariable=self._wordVar, anchor="w", font=("Arial", 12))
        word_value.grid(column=1, row=1, sticky="w", pady=(10, 0))

        # Button Frame
        button_frame = ttk.Frame(mainframe, padding="5 5 5 5")
        button_frame.grid(column=0, row=2, columnspan=2, pady=(20, 0))

        start_button = Button(button_frame, text="Start Script", command=self.startScriptThread, font=("Arial", 12))
        start_button.grid(column=0, row=0, padx=(0, 10))

        stop_button = Button(button_frame, text="Stop Script", command=self.killScriptThread, font=("Arial", 12))
        stop_button.grid(column=1, row=0)

        # Configure weights for responsiveness
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1)

        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=2)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Threads for background tasks
        self._threadStatus.start()
        self._threadWord.start()
        sv_ttk.set_theme("dark")
        self._root.protocol("WM_DELETE_WINDOW", self.onClosing)

    def startGui(self):
        """
        Run the Roblox spelling bee script.
        """
        self._root.mainloop()
