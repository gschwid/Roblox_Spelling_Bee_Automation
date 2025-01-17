from pyautogui import keyDown, keyUp, KEYBOARD_KEYS, KEY_NAMES, press
from random import uniform, choice, random
from time import sleep
import keyboard
import string

class TypingHandler:
    """
    A class to handle all the typing done by the Roblox spelling bee bot.
    """

    def writeWord(self, word, errorProbability):
        """
        Types out a specified word.

        Attributes:
            word (str): Word to type.
            errorProbability (float): probability that a misinput happens when typing. 
        """
        for chr in word:
            randomSleepTime = uniform(0, 0.005)
            randomPercentage = random()
            if randomPercentage < errorProbability:
                mistakeChr = self.generateRandomChar()
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

    def generateRandomChar(self):
        """
        Generates a random characer.
        """
        letters = string.ascii_letters
        chr = choice(letters).lower()
        return chr
        
