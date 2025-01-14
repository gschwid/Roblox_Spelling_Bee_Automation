from pyautogui import keyDown, keyUp, KEYBOARD_KEYS, KEY_NAMES, press
from random import uniform, choice, random
from time import sleep
import keyboard
import string

def writeWord(word, errorProbability):
    for chr in word:
        randomSleepTime = uniform(0, 0.005)
        randomPercentage = random()
        if randomPercentage < errorProbability:
            mistakeChr = generateRandomChar()
            keyDown(mistakeChr)
            keyUp(mistakeChr)
            sleep(randomSleepTime)
            sleep(0.001)
            keyboard.press_and_release('backspace')
        keyDown(chr)
        sleep(randomSleepTime)
        keyUp(chr)
        print(chr)
    sleep(0.05)
    keyboard.press_and_release('enter')

def generateRandomChar():
    letters = string.ascii_letters
    chr = choice(letters).lower()
    return chr

if __name__ == '__main__':
    sleep(4)
    writeWord("hello there planet earth", 0.1)
        
