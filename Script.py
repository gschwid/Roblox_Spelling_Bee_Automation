from VisualDetection import VisualDetection
from AudioHandler import AudioHandler
from TypingHandler import TypingHandler

class Script:
    """
    Class that handles running the Roblox Spelling Bee script. 

    Attributes:
        _audioHandler (AudioHandler): An instance of the AudioHandler class for managing audio processing.
        _visualDetector (VisualDetection): An instance of the VisualDetection class for handling visual detection.
        _typingHandler (TypingHandler): An instance of the TypingHandler class for managing typing-related actions.
        _running (bool): A flag indicating whether the script is currently running.
        _status (str): The current status of the script.
        _word (str): The most recently detected word by the script.
    """
    _audioHandler = AudioHandler()
    _visualDetector = VisualDetection()
    _typingHandler = TypingHandler()
    _running = False
    _status = "Script is off."
    _word = ""

    def startScript(self):
        """
        Starts the Roblox Spellig Bee script. 
        """
        self._running = True
        foundMatches = 0
        while self._running:
            # Check if Roblox window is open
            if self._visualDetector.checkIfRobloxIsOpen():
                self.setStatusOfScript("Searching for character...")
                match = self._visualDetector.checkIfTurn()
                if match:
                    foundMatches +=1
                else:
                    foundMatches = 0
                if foundMatches >= 3:
                    self.setStatusOfScript("Found character.")
                    validDetection = self._audioHandler.createAudioFile('_internal/generated-content/word.wav', self._visualDetector.waitForRepeatButton)
                    if validDetection: # This makes sure time out did not happen
                        sentence = self._audioHandler.transcribeAudio('_internal/generated-content/word.wav')
                        word = self._audioHandler.getWordFromSentence(sentence)
                        self.setDetectedWord(word)
                        self.setStatusOfScript("Typing word.")
                        self._typingHandler.writeWord(word,0.1)
                        foundMatches = 0
                        self._visualDetector.handleDeath(3)
                    else:
                        print ("Looks like the button was not found before timed out, must have been a false character detection.")
            else:
                self.setStatusOfScript("Waiting for Roblox window...")
        self.setStatusOfScript("Script is off.")

    def stopScript(self):
        """
        Stops the Roblox spelling bee script. 
        """
        self._running = False

    def getStatusOfScript(self):
        return self._status
        
    def setStatusOfScript(self, newStatus):
        self._status = newStatus

    def getDetectedWord(self):
        return self._word

    def setDetectedWord(self, word):
        self._word = word
                
            
