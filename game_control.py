# -*- coding:utf-8 -*-
import win32api
import win32con
from game_helper import *


def click(hwnd, pos, pos_end=None):
    """
    :param hwnd: 窗口句柄
    :param pos: (x, y) 鼠标点击的坐标
    :param pos_end: (x, y) 如果不为空，则点击坐标区域 pos 到 pos_end 内的随机点
    """
    x = pos[0] if pos_end is None else random.randint(pos[0], pos_end[0])
    y = pos[1] if pos_end is None else random.randint(pos[1], pos_end[1])
    long_position = win32api.MAKELONG(x, y)
    logger.debug("click in position (%d, %d)" % (x, y))
    # win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, long_position)   # 模拟鼠标移动
    # win32api.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, long_position)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
    random_sleep(100, 100)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)  # 模拟鼠标弹起


