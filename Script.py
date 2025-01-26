from VisualDetection import VisualDetection
from AudioHandler import AudioHandler
from TypingHandler import TypingHandler
import time


class Script:
    _audioHandler = AudioHandler()
    _visualDetector = VisualDetection()
    _typingHandler = TypingHandler()
    _running = False

    def startScript(self):
        print("hi")
        imagesSaved = 0
        self._running = True
        while self._running:
            print("waaaaaa")
            # Wait for a Roblox window to open
            while not self._visualDetector.checkIfRobloxIsOpen():
                time.sleep(1)
                pass
            
            print("Starting script... \nLooking for roblox charatcer")
            foundMatches = 0
            match = self._visualDetector.checkIfTurn(imagesSaved)
            if match:
                foundMatches +=1
            else:
                foundMatches = 0
            if foundMatches >= 3:
                found = True
                validDetection = self._audioHandler.createAudioFile(imagesSaved, 'word.wav', self._visualDetector.waitForRepeatButton) 
                if validDetection: # This makes sure time out did not happen
                    sentence = self._audioHandler.transcribeAudio('word.wav')
                    word = self._audioHandler.getWordFromSentence(sentence)
                    self._typingHandler.writeWord(word,0.1)
                    foundMatches = 0
                    imagesSaved += 1
                    self._visualDetector.waitForRepeatButton(3, 7)
                    self._visualDetector.handleDeath()
                else:
                    print ("Looks like the button was not found before timed out, must have been a false character detection.")

    def stopScript(self):
        print("bye")
        self._running = False
                
            
