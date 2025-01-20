from VisualDetection import VisualDetection
from AudioHandler import AudioHandler
from TypingHandler import TypingHandler
import time
import csv

if __name__ == '__main__':
    audioHandler = AudioHandler()
    visualDetector = VisualDetection()
    typingHandler = TypingHandler()
    rowCount = 0

    with open("spelling_dataset.csv", "r", newline="") as file:
        csvReader = csv.reader(file)
        for row in csvReader:
            rowCount += 1


    with open("spelling_dataset.csv", "a", newline="") as file:
        csvWriter = csv.writer(file)

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
            match = visualDetector.checkIfTurn(rowCount)
            if match:
                foundMatches +=1
            else:
                foundMatches = 0 # Resets if randomly got a good detection.
            if foundMatches >= 2:
                found = True
                validDetection = audioHandler.createAudioFile(rowCount, 'dataset/word' + str(rowCount) + '.wav', visualDetector.waitForRepeatButton) 
                if validDetection: # This makes sure time out did not happen
                    sentence = audioHandler.transcribeAudio('dataset/word' + str(rowCount) + '.wav')
                    word = audioHandler.getWordFromSentence(sentence)
                    typingHandler.writeWord(word,0.1)
                    foundMatches = 0
                    visualDetector.waitForRepeatButton(1, 7)
                    visualDetector.handleDeath()
                    csvWriter.writerow([('dataset/word' + str(rowCount) + '.wav'), str(sentence)])
                    rowCount += 1
            loop += 1
            
            
            
