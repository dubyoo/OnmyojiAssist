# -*- coding:utf-8 -*-
import win32gui
import win32ui
import win32con
import numpy
import cv2
import traceback
from game_helper import *


def get_window_handlers():
    hwnd_list = list()
    win32gui.EnumWindows(_enum_window_callback, hwnd_list)
    return hwnd_list


def _enum_window_callback(hwnd, hwnd_list):
    if win32gui.IsWindow(hwnd) \
            and win32gui.IsWindowEnabled(hwnd) \
            and win32gui.IsWindowVisible(hwnd) \
            and win32gui.GetWindowText(hwnd) == '阴阳师-网易游戏':
        hwnd_list.append(hwnd)


def dump_windows_information(hwnd_list):
    info_dict = dict()
    for hwnd in hwnd_list:
        title = win32gui.GetWindowText(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
        client_rect = (x, y, rect[2], rect[3])
        info_dict[hwnd] = (title, client_rect)
    for k, v in info_dict.items():
        print('hwnd:', k, 'info:', str(v))


def shake_window(hwnd):
    x, y, w, h = win32gui.GetWindowRect(hwnd)
    for i in range(3):
        win32gui.SetWindowPos(
            hwnd, None, x + random.randint(-5, 5), y - random.randint(-5, 5), 0, 0,
            win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)  # 实现更改当前窗口位置
        time.sleep(0.1)
        win32gui.SetWindowPos(
            hwnd, None, x, y, 0, 0,
            win32con.SWP_NOSENDCHANGING | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)  # 将窗口恢复至初始位置
        time.sleep(0.1)


def screen_shot(hwnd, pos_lt=None, pos_rb=None, file_name=None):
    """
    窗口区域截图
        :param hwnd: 窗口句柄
        :param pos_lt: (x,y) 截图区域的左上角坐标, 若为 None 则截取整个窗口
        :param pos_rb: (x,y) 截图区域的右下角坐标, 若为 None 则截取整个窗口
        :param file_name: 截图文件的保存路径
        :return: 若 file_name 为空则返回 RGB 数据
    """
    window_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    client_pos = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
    client_to_window_x = client_pos[0] - window_rect[0]
    client_to_window_y = client_pos[1] - window_rect[1]
    if pos_lt is None or pos_rb is None:
        pos_lt = (0, 0)
        pos_rb = (client_rect[2], client_rect[3])
    w = pos_rb[0] - pos_lt[0]
    h = pos_rb[1] - pos_lt[1]
    hwindc = win32gui.GetWindowDC(hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, w, h)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (w, h), srcdc,
                 (pos_lt[0] + client_to_window_x, pos_lt[1] + client_to_window_y),
                 win32con.SRCCOPY)
    if file_name is not None:
        bmp.SaveBitmapFile(memdc, file_name)
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
        return
    else:
        signedIntsArray = bmp.GetBitmapBits(True)
        img = numpy.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def compare_image(img_template, img_cmp):
    """
    查找图片
        :param img_template: 模板图片
        :param img_cmp: 待比较图片
        :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
    """
    try:
        res = cv2.matchTemplate(img_template, img_cmp, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal > 0.9:
            template = cv2.imread(img_cmp, cv2.IMREAD_COLOR)
            w, h = template.shape[::-1]
            img_loc = [maxLoc[0], maxLoc[1], maxLoc[0] + w, maxLoc[1] + h]
        return maxVal, img_loc
    except Exception:
        logger.warning('compare_image failed')
        a = traceback.format_exc()
        logger.warning(a)
        return 0, 0


def find_image(hwnd, img_template_path, pos_lt=None, pos_rb=None):
    """
    在窗口中找图
        :param hwnd: 窗口句柄
        :param img_template_path: 图片文件路径
        :param pos_lt: 截图区域的左上角坐标, 若为 None 则截取整个窗口
        :param pos_rb: 截图区域的右下角坐标, 若为 None 则截取整个窗口
        :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
    """
    img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
    img_cmp = screen_shot(hwnd, pos_lt, pos_rb)
    return compare_image(img_template, img_cmp)


def show_img(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)
