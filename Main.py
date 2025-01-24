from VisualDetection import VisualDetection
from AudioHandler import AudioHandler
from TypingHandler import TypingHandler
import time

if __name__ == '__main__':
    audioHandler = AudioHandler()
    visualDetector = VisualDetection()
    typingHandler = TypingHandler()

    # Wait for a Roblox window to open
    while not visualDetector.checkIfRobloxIsOpen():
        time.sleep(1)
        pass
    
    print("Starting script... \nLooking for roblox charatcer")
    foundMatches = 0
    loop = 0

    while True:
        if loop % 100 == 0:
            print("searching for character..")
        match = visualDetector.checkIfTurn()
        if match:
            foundMatches +=1
        else:
            foundMatches = 0 # Resets if randomly got a good detection.
        if foundMatches >= 2:
            found = True
            validDetection = audioHandler.createAudioFile('word.wav', visualDetector.waitForRepeatButton) 
            if validDetection: # This makes sure time out did not happen
                sentence = audioHandler.transcribeAudio('word.wav')
                word = audioHandler.getWordFromSentence(sentence)
                typingHandler.writeWord(word,0.1)
                foundMatches = 0
                visualDetector.waitForRepeatButton(3, 7)
                visualDetector.handleDeath()
        loop += 1
            
            
            
