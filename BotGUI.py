
# EyeAligningBot

# Done by Balloon_356
# Bilibili: https://space.bilibili.com/244384103



import cv2
import time
import pyautogui as pg 
import pydirectinput as pd

import win32gui, win32api
import win32com.client
import pythoncom
import json

import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import *



from PIL import Image, ImageTk

import utils.cursor_matching as cm
import utils.template_matching  as tm
import utils.mouse_control as M
from utils.grabscreen import grab_screen



pg.PAUSE=0.001
pd.PAUSE=0.001


def SetForeground(hWnd):
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hWnd) 


def select_windows():
    winName = Combo_winName.get()
    global mc_hWnd
    mc_hWnd = win32gui.FindWindow(None, winName)
    word['text'] = '窗口句柄：' + str(mc_hWnd)
    word['bootstyle'] = 'info'


def detect_eyes():

    try:
        SetForeground(mc_hWnd)
    except:
        word['text'] = 'ERROR 1'
        word['bootstyle'] = 'danger'
        return
    
    # template matching
    _, destX, _, img_show = tm.temp_match(
        template_eye, mask, region=(0, 0, width-1, height-1))

    if destX != None:
        # interpolation
        img_show = cv2.resize(
            img_show, (0, 0), fx=7, fy=3, interpolation=cv2.INTER_NEAREST)

        # image show
        global imgTK
        current_image = Image.fromarray(img_show)
        imgTK = ImageTk.PhotoImage(image=current_image)
        canvas_im.itemconfig(image_container, image=imgTK)

        SetForeground(win32gui.FindWindow(None, 'EyeAligningBot'))
        word['text'] = '检测结果如上'
        word['bootstyle'] = 'info'

    else:
        SetForeground(win32gui.FindWindow(None, 'EyeAligningBot'))
        word['text'] = '未检测到末影之眼'
        word['bootstyle'] = 'danger'


def align():

    while True:
        # matching
        SetForeground(mc_hWnd)
        for _ in range(5):
            _, destX, destY, img_show = tm.temp_match(template_eye, mask)
            startX, startY = cm.cursor_match(template_cursor)
            # robust
            if destX != None:
                break
            else:
                M.mc_mouse_move(0, 0, paused=True)


        if destX != None:
            # interpolation
            img_show = cv2.resize(
                img_show, (0, 0), fx=7, fy=3, interpolation=cv2.INTER_NEAREST)

            # image show
            global imgTK
            current_image = Image.fromarray(img_show)
            imgTK = ImageTk.PhotoImage(image=current_image)
            canvas_im.itemconfig(image_container, image=imgTK)

            # aligning
            SetForeground(mc_hWnd)
            flag = M.EyeAlign(startX, startY, destX, destY)
            if  flag == True:
                SetForeground(win32gui.FindWindow(None, 'EyeAligningBot'))
                word['text'] = '已对准！'
                word['bootstyle'] = 'success'
                break

        else:
            SetForeground(win32gui.FindWindow(None, 'EyeAligningBot'))
            word['text'] = '未检测到末影之眼'
            word['bootstyle'] = 'danger'
            break


if __name__ == '__main__':

    with open('settings.json') as file:
        settings = json.load(file, )
        template_eye_filename = settings['eye_path']
        mask_filename = settings['mask_path']
        template_cursor_filename = settings['cursor_path']
        minecraft_windows_filter = settings['minecraft_windows_filter']
        bot_theme = settings['bot_theme']

    # theme: "cosmo", "flatly", "litera", "minty", "yeti", "pulse", "united",
    #        "morph",  "journal",  "darkly",  "superhero", "solar", "cyborg",
    #        "vapor", "simplex",  "cerculean", 

    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)

    # template
    template_eye = cv2.imread(template_eye_filename)
    mask = cv2.imread(mask_filename)
    template_cursor = cv2.imread(template_cursor_filename)
    eyeHW = template_eye.shape

    # GUI
    win = ttkb.Window(
        title='EyeAligningBot',
        themename=bot_theme, 
        iconphoto='./imgs/icon.png',
        resizable=(False, False),
        size=(240, 505))

    title = ttkb.Label(win, text='EyeAligningBot', font=('GeForce', 20), bootstyle='primary')
    title.pack(side='top', padx=10, pady=5)

    # enum windows
    windows_list = []
    win32gui.EnumWindows(
        lambda hWnd, param: param.append(win32gui.GetWindowText(hWnd)),
        windows_list)
    windows_list = [name for name in windows_list if minecraft_windows_filter in name]

    # combobox
    frame = ttkb.Frame(win)
    frame.pack(side='top', padx=10, pady=(5, 0), fill=X)
    Combo_winName = ttkb.Combobox(frame, value=windows_list)
    Combo_winName.set("选择窗口")
    Combo_winName.pack(side='left', padx=(0, 5), anchor='w')

    # buttons
    button_selectWindows = ttkb.Button(
                        frame, text='确定', 
                        command=select_windows,
                        bootstyle='primary outline'
                        )
    button_selectWindows.pack(side='left', ipadx=5, fill=X)

    button_det = ttkb.Button(
                        win, text='检测末影之眼', 
                        command=detect_eyes,
                        bootstyle='primary outline'
                        )
    button_det.pack(side='top', padx=10, pady=(5, 0), fill=X)

    button_align = ttkb.Button(win, text='对准',
                        command=align,
                        bootstyle='primary outline'
                        )
    button_align.pack(side='top', padx=10, pady=(5, 0), fill=X)

    # canvas
    canvas_im = ttkb.Canvas(win, width=216, height=308)
    canvas_im.pack(side='top', padx=10, pady=(10, 0))
    img1 = PhotoImage(file="imgs/default.png")
    image_container = canvas_im.create_image(0, 0, anchor="nw", image=img1)

    # labels
    frame_bottom = ttkb.Frame(win)
    frame_bottom.pack(side='top', padx=10, pady=(5, 0), fill=X)

    word = ttkb.Label(frame_bottom, text='未启动', bootstyle='danger')
    word.pack(side='left', anchor='w')

    sign = ttkb.Label(frame_bottom, text='by Balloon_356', bootstyle='secondary')
    sign.pack(side='right', anchor='e')


    win.mainloop()
