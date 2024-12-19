import time
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode

time.sleep(1)
keyboard = KeyboardController()
keyboard.press(Key.shift)
time.sleep(.1)
keyboard.press(KeyCode(vk=29))
time.sleep(.1)
keyboard.release(KeyCode(vk=29))
time.sleep(.1)
keyboard.release(Key.shift)