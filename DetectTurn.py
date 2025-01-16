import pyautogui
import time
import cv2 as cv
import pytesseract
from pywinauto import Application

orb = cv.ORB_create()
app = Application()
windowInfo = {}

def updateWindowInfo():
    global windowInfo
    rectangle = dlg_spec.wrapper_object().rectangle()
    center = rectangle.mid_point()
    width, height = rectangle.width(), rectangle.height()
    centerWidth, centerHeight = center.x, center.y
    left, top, right, bottom = rectangle.left, rectangle.top, rectangle.right, rectangle.bottom
    windowInfo = {
        'width' : width,
        'height' : height,
        'centerWidth' : centerWidth,
        'centerHeight' : centerHeight,
        'left' : left,
        'top' : top,
        'right' : right,
        'bottom' : bottom
    }

def checkIfTurn(picturesSaved):
        updateWindowInfo()
        widthRatio = int(windowInfo['width'] / 8) # 8 is a hyperparameter that seemed to work well
        heightRatio = int(windowInfo['height'] / 12)
        squareSize = max(widthRatio, heightRatio)
        pyautogui.screenshot(imageFilename="check.png", region=(windowInfo['centerWidth'] - widthRatio, windowInfo['centerHeight'] + heightRatio, squareSize * 2, squareSize * 2))
        if featureMatch('reference.png', 'check.png', 20):
            return True
        else:
            return False
        
def featureMatch(referencePicture, screenshot, minGoodMatches):
    try:
        reference_picture = cv.imread(referencePicture, cv.IMREAD_GRAYSCALE)
        screenshot_picture = cv.imread(screenshot, cv.IMREAD_GRAYSCALE)
    
        # Get descriptors
        kp1, des1 = orb.detectAndCompute(reference_picture,None)
        kp2, des2 = orb.detectAndCompute(screenshot_picture,None)

        # Use brute force matching to find 2 best matches between images
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1,des2,k=2)

        # Ratio test, if one match is significantly better than other add it to the good list
        good = []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        print(len(good))
        if len(good) >= minGoodMatches:            #filename = "Detected_Images/match" + str(picturesSaved) + ".jpg"
            #cv.imwrite(filename, screenshot_picture)
            return True
        else:
            return False
    except cv.error:
        print("screen has no features! Likely only one color.")
    except ValueError:
        print("Something broke lol")

def checkButton(sleep):
    updateWindowInfo()
    waitForPixelChange(windowInfo['right'] - 30, windowInfo['centerHeight'], 0, sleep)

def waitForPixelChange(x, y, threshold, sleep):
    newPixel = pyautogui.pixel(x, y)
    print(newPixel)
    while abs(newPixel[0] - newPixel[1]) > threshold or abs(newPixel[1] - newPixel[2]) > threshold or abs(newPixel[2] - newPixel[0]) > threshold:
        newPixel = pyautogui.pixel(x, y)
    if sleep > 0:
        time.sleep(sleep)
    print("Pixel change detected!")
    return

# THIS NEEDS TO BE REFACTORED
def detectPixelChange(x, y, threshold, sleep):
    newPixel = pyautogui.pixel(x, y)
    print(newPixel)
    if abs(newPixel[0] - newPixel[1]) > threshold or abs(newPixel[1] - newPixel[2]) > threshold or abs(newPixel[2] - newPixel[0]) > threshold:
        return False
    else:
        return True

def checkIfRobloxIsOpen():
    global app
    global dlg_spec
    try:
        app.connect(title="Roblox")
        dlg_spec = app.window(title='Roblox')
        return True
    except:
        print('Roblox window not open...')
        return False
    
def handleDeath():
    updateWindowInfo()
    pyautogui.click(windowInfo['centerWidth'], windowInfo['centerHeight'])
    
def detectNewGame():
    updateWindowInfo()
    pyautogui.screenshot("screen.png", region=(windowInfo['left'], windowInfo['top'], windowInfo['width'], windowInfo['height']))
    time.sleep(0.1)
    if featureMatch('reference.png', 'screen.png', 7):
        return True
    else:
        return False
    
if __name__ == '__main__':
    checkIfRobloxIsOpen()
    checkIfDead()

