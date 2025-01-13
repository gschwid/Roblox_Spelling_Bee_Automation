import pyautogui
import time
import cv2 as cv
from pywinauto import Application

orb = cv.ORB_create()
app = Application(backend="uia")
app.connect(title="Roblox")
dlg_spec = app.window(title='Roblox')

def checkIfTurn(picturesSaved):
    try:
        rectangle = dlg_spec.wrapper_object().rectangle()
        center = rectangle.mid_point()
        width, height = rectangle.width(), rectangle.height()
        centerWidth, centerHeight = center.x, center.y
        widthRatio = int(width / 8) # 8 is a hyperparameter that seemed to work well
        heightRatio = int(height / 12)
        squareSize = max(widthRatio, heightRatio)
        pyautogui.screenshot(imageFilename="check.png", region=(centerWidth - widthRatio, centerHeight + heightRatio, squareSize * 2, squareSize * 2))
        reference_picture = cv.imread('reference.png', cv.IMREAD_GRAYSCALE)
        screenshot_picture = cv.imread("check.png", cv.IMREAD_GRAYSCALE)
        screenshot_picture = cv.resize(screenshot_picture, reference_picture.shape)
    
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
        if len(good) >= 15:
            #filename = "Detected_Images/match" + str(picturesSaved) + ".jpg"
            #cv.imwrite(filename, screenshot_picture)
            return True
        else:
            return False
    except cv.error:
        print("screen has no features! Likely only one color.")
    except ValueError:
        print("idk man some shit happened")

def waitForPixelChange(x, y, sleep):
    initialPixel = pyautogui.pixel(x, y)
    newPixel = pyautogui.pixel(x, y)
    while newPixel == initialPixel:
        newPixel = pyautogui.pixel(x, y)
    if sleep > 0:
        time.sleep(sleep)
    print("Pixel change detected!")
    return
