from VisualDetection import VisualDetection
from AudioHandler import AudioHandler
from TypingHandler import TypingHandler
import time
import queue


class Script:
    _audioHandler = AudioHandler()
    _visualDetector = VisualDetection()
    _typingHandler = TypingHandler()
    _running = False
    _status = "Script is off."
    _word = ""
    _mainThreadQue = queue.Queue()

    def startScript(self):
        imagesSaved = 0
        self._running = True
        foundMatches = 0
        while self._running:
            # Check if Roblox window is open
            if self._visualDetector.checkIfRobloxIsOpen():
                self.setStatusOfScript("Searching for character...")
                match = self._visualDetector.checkIfTurn(imagesSaved)
                if match:
                    foundMatches +=1
                else:
                    foundMatches = 0
                if foundMatches >= 3:
                    self.setStatusOfScript("Found Character.")
                    found = True
                    validDetection = self._audioHandler.createAudioFile(imagesSaved, 'word.wav', self._visualDetector.waitForRepeatButton)
                    if validDetection: # This makes sure time out did not happen
                        sentence = self._audioHandler.transcribeAudio('word.wav')
                        word = self._audioHandler.getWordFromSentence(sentence)
                        self.setDetectedWord(word)
                        self._typingHandler.writeWord(word,0.1)
                        foundMatches = 0
                        imagesSaved += 1
                        self._visualDetector.waitForRepeatButton(3, 7)
                        self._visualDetector.handleDeath()
                    else:
                        print ("Looks like the button was not found before timed out, must have been a false character detection.")
            else:
                self.setStatusOfScript("Waiting for Roblox window...")
        self.setStatusOfScript("Script is off.")

    def stopScript(self):
        self._running = False

    def getStatusOfScript(self):
        return self._status
        
    def setStatusOfScript(self, newStatus):
        self._status = newStatus

    def getDetectedWord(self):
        return self._word

    def setDetectedWord(self, word):
        self._word = word

    def getMainThreadQue(self):
        return self._mainThreadQue
                
            
