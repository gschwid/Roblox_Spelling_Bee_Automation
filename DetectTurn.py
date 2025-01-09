import pyautogui
import time
import cv2 as cv

orb = cv.ORB_create()

def checkIfTurn(picturesSaved):
    try:
        pyautogui.screenshot(imageFilename="check.png", region=(800,550,300,300))
        reference_picture = cv.imread('reference.png', cv.IMREAD_GRAYSCALE)
        screenshot_picture = cv.imread("check.png", cv.IMREAD_GRAYSCALE)
    
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
