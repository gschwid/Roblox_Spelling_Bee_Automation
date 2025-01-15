from SpeakerAudio import createAudioFile, releaseAudioResources
from DetectTurn import checkIfTurn, checkButton, checkIfRobloxIsOpen, checkIfDead
from InterpretAudio import transcribeAudio, getWordFromSentence
import pyautogui
from Typing import writeWord


if __name__ == '__main__':
    while not checkIfRobloxIsOpen():
        pass
    foundMatches = 0
    found = False
    imagesSaved = 62
    print("Starting script... \nLooking for roblox charatcer")
    while True:
        match = checkIfTurn(imagesSaved)
        if match:
            foundMatches +=1
        else:
            found = False
            foundMatches = 0
        if foundMatches >= 1:
            found = True
            createAudioFile(imagesSaved)
            sentence = transcribeAudio('word.wav')
            word = getWordFromSentence(sentence)
            writeWord(word,0.05)
            foundMatches = 0
            imagesSaved += 1
            checkButton(1)
            if checkIfDead():
                print("you died!")
                nextGame = False
                while not nextGame:
                    try:
                        pyautogui.locateOnScreen("Intermission.png")
                        nextGame = True
                        print("New game starting...")
                    except:
                        print("waiting for next game...")
            
            
