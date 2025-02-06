import time
from pynput.mouse import Controller as MouseController, Button

mouse = MouseController()

time.sleep(3)

mouse.press(Button.left)
mouse.release(Button.left)
time.sleep(.05)
mouse.press(Button.left)
mouse.release(Button.left)
time.sleep(.1)