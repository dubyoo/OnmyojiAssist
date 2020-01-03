# -*- coding: utf-8 -*-
import time
import random
import ctypes
import logging
import sys
import os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox


# Detect Coordinate
Coord_XuanShang = 750, 458
Coord_TiaoZhan_Single = 1026, 513
Coord_TiaoZhan_Team = 1098, 591
Coord_TiaoZhan_Passenger = 0, 0
Coord_LiKaiDuiWu = 145, 520
Coord_InTheBattle = 71, 577
Coord_Finished = 59, 85
Coord_Bonus = 59, 85
Coord_Driver_Invite_CheckButton = 496, 312
Coord_Driver_Invite_OK = 620, 371
Coord_Passenger_Accept1 = 128, 228
Coord_Passenger_Accept2 = 211, 239

# Button Region (x1, y1, x2, y2)
Region_XuanShang = 750-5, 458-5, 750+5, 458+5
Region_TiaoZhan_Single = 995, 540, 1060, 590
# Region_TiaoZhan = 790, 417, 901, 465
Region_TiaoZhan_Driver = 1098-5, 591-5, 1098+5, 591+5
Region_Bonus = 163, 86, 244, 105
Region_Driver_Invite_CheckButton = 490, 310, 505, 327
Region_Driver_Invite_OK = 600, 360, 747, 405
Region_Passenger_Accept = 193, 212, 227, 245

# Color Baseline
Color_XuanShang = "df715e"
Color_TiaoZhan_Single = "beb19b"   # yuhun
Color_TiaoZhan_Single2 = "d7ccb4"  # juexing
Color_TiaoZhan_Single3 = "624f40"  # yuling
Color_TiaoZhan_Ready = "e7c769"
Color_TiaoZhan_Waiting = "c6c6c6"
Color_TiaoZhan_Passenger = "f8f3e0"
Color_InTheBattle = "f7f2df"
Color_Finished = "e8d9ce"
Color_Bonus = "746c67"
Color_Driver_Invite_CheckButton_NO = "725f4d"
Color_Driver_Invite_CheckButton_YES = "4b5ee9"
Color_Driver_Invite_OK = "f3b25e"
Color_Passenger_Accept = "58b563"

logger = logging.getLogger('my_logger')


class TimedMessageBox(QMessageBox):
    def __init__(self, timeout=30, parent=None):
        super(TimedMessageBox, self).__init__(parent)
        self.timeout = timeout
        self.setWindowTitle("自动关机")
        self.setText("系统将在 %d 秒后关机，点击按钮取消？" % self.timeout)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)
        self.timer.start()

    def tick(self):
        self.timeout -= 1
        if self.timeout >= 0:
            logger.info('%d' % self.timeout)
            self.setText("系统将在 %d 秒后关机，点击按钮取消？" % self.timeout)
        else:
            self.timer.stop()
            logger.info("正在关机")
            os.system('shutdown /s /t 5')


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr


class MyQtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s' % record)


def init_logger():
    text_browser_handler = MyQtHandler()
    terminal_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    text_browser_handler.setFormatter(formatter)
    terminal_handler.setFormatter(formatter)
    logger.addHandler(terminal_handler)
    logger.addHandler(text_browser_handler)
    logger.setLevel(logging.INFO)


def random_sleep(sleep_time, variable_time=0):
    """
    randomly sleep for a short time between `sleep_time` and `sleep_time + variable_time`
    because of the legacy reason, sleep_time and variable_time are in millisecond
    """
    slp = random.randint(sleep_time, sleep_time + variable_time)
    time.sleep(slp / 1000)


def click_in_region(ts, x1, y1, x2, y2):
    """
    randomly click a point in a rectangle region (x1, y1), (x2, y2)
    """
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    ts.MoveTo(x, y)
    logging.debug('move to (%d, %d)' % (x, y))
    random_sleep(100, 100)
    ts.LeftClick()
    logging.debug('left click')


def keep_awake(enable=True):
    """
    make the screen keep awake, do not go to sleep mode
    """
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    if enable:
        logging.info('enable screen awake')
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
    else:
        logging.info('disable screen awake')
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
