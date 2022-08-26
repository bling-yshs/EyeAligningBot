import pyautogui as pg 
import pydirectinput as pd
import time
import win32api, win32con

from pynput import keyboard
from pynput.mouse import Button, Controller


def mc_pause():
    pd.keyDown('f3')
    pd.keyDown('esc')
    pd.keyUp('esc')
    pd.keyUp('f3')

def mc_mouse_move(dx, dy, paused=False):  
    if paused:
        pd.keyDown('esc')
        pd.keyUp('esc')
    pd.moveRel(0, 1)  # to activate the cursor
    pd.moveRel(dy, dx)
    if paused:
        mc_pause()

def EyeAlign(startX, startY, destX, destY):
    time.sleep(0.1)
    dx = destX - startX
    dy = destY - startY
    print(dx, dy)
    if dy == 0:
        win32api.MessageBox(0, "已对准", "提醒", win32con.MB_OK)
        return True
    elif abs(dy) <= 10:
        mc_mouse_move(3*dx, 2*dy, paused=True)
    else:
        mc_mouse_move(3*dx, 3*dy, paused=True)
    time.sleep(0.1)
    return False


