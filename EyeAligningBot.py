
import cv2
import time
import pyautogui as pg 
import pydirectinput as pd


import utils.cursor_matching as cm
import utils.template_matching  as tm
import utils.mouse_control as M
import win32gui, win32com.client
import pythoncom


pg.PAUSE=0.01
pd.PAUSE=0.01


# template
template_eye = cv2.imread('./img/eye_cropped_fov30.png')
template_eye_precise = cv2.imread('./img/eye_precise.png')
template_cursor = cv2.imread('./img/cursor.png')

# set foreground
def SetForeground(winName):
    mc_hWnd = win32gui.FindWindow(None, winName)
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(mc_hWnd) 

warmup = True

while True:

    # matching
    destX, destY = tm.temp_match(template_eye, template_eye_precise)
    startX, startY = cm.cursor_match(template_cursor)

    if warmup:
        warmup = False
        cv2.waitKey()

    # display
    if cv2.waitKey(25) & 0xFF == ord('Q'):
        cv2.destroyAllWindows()
        break

    print('dest: ', destX, destY)
    print('start: ', startX, startY)

    # aligning
    if destX != None:
        SetForeground('Minecraft* 1.16.1 - 单人游戏')
        flag = M.EyeAlign(startX, startY, destX, destY)
        if  flag == True:
            break
        SetForeground('screen_pixel')

    