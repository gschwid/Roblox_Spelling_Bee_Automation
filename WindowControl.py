from subprocess import Popen
from pywinauto import Application

app = Application()
app.connect(title="Roblox")
print(app.top_window().wrapper_object().rectangle())