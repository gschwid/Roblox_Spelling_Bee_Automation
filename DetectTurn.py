import pyautogui
import time
import cv2 as cv
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
    if left < 0:
        left = 0
    elif right < 0:
        right = 0
    elif top < 0:
        top = 0
    elif bottom < 0:
        bottom = 0
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
        featureMatch('reference.png', 'check.png', 15)

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
    print(f"{windowInfo['right']} {windowInfo['centerHeight']}")
    waitForPixelChange(windowInfo['right'] - 30, windowInfo['centerHeight'], sleep)

def waitForPixelChange(x, y, sleep):
    newPixel = pyautogui.pixel(x, y)
    print(newPixel)
    while newPixel[0] != newPixel[1] or newPixel[1] != newPixel[2] or newPixel[2] != newPixel[0]:
        newPixel = pyautogui.pixel(x, y)
    if sleep > 0:
        time.sleep(sleep)
    print("Pixel change detected!")
    return

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
    
def checkIfDead():
    time.sleep(2)
    try:
        location = pyautogui.locateOnScreen('died.png')
        pyautogui.click(location)
        return True
    except:
        print("not dead!")
        return False
    

if __name__ == '__main__':
    checkIfRobloxIsOpen()
    while True:
        checkButton(0)
