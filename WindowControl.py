from subprocess import Popen
from pywinauto import Application
from PIL import Image
import pyautogui
import ctypes

#ctypes.windll.user32.SetProcessDPIAware()

app = Application(backend="uia")
app.connect(title="Roblox")
dlg_spec = app.window(title='Roblox')
rectangle = dlg_spec.wrapper_object().rectangle()
left, top, right, bottom = rectangle.left, rectangle.top, rectangle.right, rectangle.bottom
width, height = rectangle.width(), rectangle.height()
center = rectangle.mid_point()
centerWidth, centerHeight = center.x, center.y
print(f'left: {rectangle.left}, top: {rectangle.top}, right: {rectangle.right}, bottom: {rectangle.bottom}')
print(f"width: {rectangle.width()}, height: {rectangle.height()}")

pyautogui.screenshot(imageFilename="test.png", region=(centerWidth - int(centerWidth / 8), centerHeight + int(centerHeight / 8), int(centerWidth / 8) * 2, int(centerWidth / 8) * 2))