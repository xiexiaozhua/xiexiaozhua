import os
import pyautogui
import time
os.startfile("cmd")
time.sleep(1)
pyautogui.write("shutdown -s -t 5")
pyautogui.press('enter')
