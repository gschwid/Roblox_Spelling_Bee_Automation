import pyautogui
import time
import cv2 as cv
from pywinauto import Application
import func_timeout
import pydirectinput

class VisualDetection:
    """
    A class to handle all the visual detection and reaction of the Roblox Spelling Bee Bot.

    Attributes:
        _orb: The ORB object used for image processing (private).
        _app: An instance of the Application class for interacting with the GUI (private).
        _windowInfo: A dictionary storing information about the window (private).
        _dlg_spec: The dialog specification for the application (private).
    """

    def __init__(self):
        """
        Initializes the VisualDetection class with private attributes.
        """
        self._orb = cv.ORB_create()
        self._app = Application()
        self._windowInfo = {}
        self._dlg_spec = None

    def updateWindowInfo(self):
        """
        Updates the window dimension attribute.
        """
        rectangle = self._dlg_spec.wrapper_object().rectangle()
        center = rectangle.mid_point()
        width, height = rectangle.width(), rectangle.height()
        centerWidth, centerHeight = center.x, center.y
        left, top, right, bottom = rectangle.left, rectangle.top, rectangle.right, rectangle.bottom
        self._windowInfo = {
            'width' : width,
            'height' : height,
            'centerWidth' : centerWidth,
            'centerHeight' : centerHeight,
            'left' : left,
            'top' : top,
            'right' : right,
            'bottom' : bottom
        }

    def checkIfTurn(self):
        """
        Checks if its your characters turn in the spelling bee.
        """
        self.updateWindowInfo()
        widthRatio = int(self._windowInfo['width'] / 8) # 8 is a hyperparameter that seemed to work well
        heightRatio = int(self._windowInfo['height'] / 12)
        squareSize = max(widthRatio, heightRatio)
        pyautogui.screenshot(imageFilename="_internal/generated-content/check.png", region=(self._windowInfo['centerWidth'] - widthRatio, self._windowInfo['centerHeight'] + heightRatio, squareSize * 2, squareSize * 2))
        if self.featureMatch('reference.png', '_internal/generated-content/check.png', 15):
            return True
        else:
            return False
        
    def featureMatch(self, referencePicture, screenshot, minGoodMatches):
        """
        Preforms ORB feature matching on 2 images.

        Attributes:
            referencePicture (str): Picture used as reference for matching.
            screenshot (str): screenshot being matched with the reference.
            minGoodMatches (int): Minimum number of good matches found to find match.

        """
        try:
            referencePicture = cv.imread(referencePicture, cv.IMREAD_GRAYSCALE)
            screenshotPicture = cv.imread(screenshot, cv.IMREAD_GRAYSCALE)
        
            # Get descriptors
            kp1, des1 = self._orb.detectAndCompute(referencePicture,None)
            kp2, des2 = self._orb.detectAndCompute(screenshotPicture,None)

            # Use brute force matching to find 2 best matches between images
            bf = cv.BFMatcher()
            matches = bf.knnMatch(des1,des2,k=2)

            # Ratio test, if one match is significantly better than other add it to the good list
            good = []
            for m,n in matches:
                if m.distance < 0.75*n.distance:
                    good.append([m])
            print(len(good))
            if len(good) >= minGoodMatches:      
                return True
            else:
                return False
            
        except cv.error:
            print("screen has no features! Likely only one color.")
        except ValueError:
            print("Something broke lol")

    def waitForRepeatButton(self, sleep, timeout):
        """
        Checks if the repeat button has appeared in the Roblox Spelling Bee.

        Attributes:
            sleep (int): How long the script will sleep after button is found.
            timeout (int): How long the function will wait for the button.
        """
        self.updateWindowInfo()
        try:
            func_timeout.func_timeout(timeout, self.waitForPixelChangeNuetralColor, args=(self._windowInfo['right'] - 30, self._windowInfo['centerHeight'], 0, sleep))
            print("Button found!")
            return True
        except func_timeout.FunctionTimedOut:
            print("Button took too long to find, timing out..")
            return False
            
    def waitForPixelChangeNuetralColor(self, x, y, threshold, sleep):
        """
        Waits for a pixel change on specified pixel to a nuetral color.

        Attributes:
            x (int): x cordinate of pixel.
            y (int): y coordinate of pixel.
            threshold (int): allowed difference between the R, G, B values.
            sleep: time to sleep once detected. 
        """
        pyautogui.screenshot("_internal/generated-content/button_check.png")
        buttonImage = cv.imread("_internal/generated-content/button_check.png")
        try:
            newPixel = buttonImage[y, x]
            while abs(int(newPixel[0]) - int(newPixel[1])) > threshold or abs(int(newPixel[1]) - int(newPixel[2])) > threshold or abs(int(newPixel[2]) - int(newPixel[0])) > threshold:
                pyautogui.screenshot("_internal/generated-content/button_check.png")
                buttonImage = cv.imread("_internal/generated-content/button_check.png")
                newPixel = buttonImage[y, x]
            if sleep > 0:
                time.sleep(sleep)
            return
        except:
            raise IndexError("Move the Roblox screen.")

    def checkIfRobloxIsOpen(self):
        """
        Checks if a Roblox window is open.
        """
        try:
            self._app.connect(title="Roblox")
            self._dlg_spec = self._app.window(title='Roblox')
            return True
        except:
            print('Roblox window not open...')
            return False
        
    def handleDeath(self, scrollTime):
        """
        Clicks the screen to handle death pop up.

        Attributes:
            scrollTime (int): time it takes to move cursor to middle of screen.
        """
        self.updateWindowInfo()
        time.sleep(scrollTime)
        pydirectinput.moveTo(self._windowInfo['centerWidth'], self._windowInfo['centerHeight'] - 30, duration=scrollTime)
        pydirectinput.moveTo(self._windowInfo['centerWidth'], self._windowInfo['centerHeight'], duration=scrollTime)
        pydirectinput.click(self._windowInfo['centerWidth'], self._windowInfo['centerHeight'])

if __name__ == '__main__':
    visualDetector = VisualDetection()
    visualDetector.checkIfRobloxIsOpen()
    visualDetector.handleDeath(6)