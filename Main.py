from VisualDetection import VisualDetection
from AudioHandler import AudioHandler
from TypingHandler import TypingHandler


if __name__ == '__main__':
    audioHandler = AudioHandler()
    visualDetector = VisualDetection()
    typingHandler = TypingHandler()

    # Wait for a Roblox window to open
    while not visualDetector.checkIfRobloxIsOpen():
        pass
    
    print("Starting script... \nLooking for roblox charatcer")
    foundMatches = 0
    imagesSaved = 62
    while True:
        match = visualDetector.checkIfTurn(imagesSaved)
        if match:
            foundMatches +=1
        else:
            foundMatches = 0
        if foundMatches >= 3:
            found = True
            audioHandler.createAudioFile(imagesSaved, 'word.wav', visualDetector.waitForRepeatButton)
            sentence = audioHandler.transcribeAudio('word.wav')
            word = audioHandler.getWordFromSentence(sentence)
            typingHandler.writeWord(word,0.1)

            foundMatches = 0
            imagesSaved += 1
            visualDetector.waitForRepeatButton(3)
            visualDetector.handleDeath()
            
            
