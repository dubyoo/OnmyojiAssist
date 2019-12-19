# -*- coding: utf-8 -*-
import time
import random
import ctypes
import logging
import sys
from PyQt5 import QtCore


# Detect Coordinate
Coord_XuanShang = 750, 458
Coord_TiaoZhan_Single = 807, 442
Coord_TiaoZhan_Team = 1098, 591
Coord_LiKaiDuiWu = 145, 520
Coord_InTheBattle = 71, 577
Coord_Finished = 59, 85
Coord_Bonus = 59, 85
Coord_Driver_Invite_CheckButton = 496, 312
Coord_Driver_Invite_OK = 620,371
Coord_Passenger_Accept1 = 128,228
Coord_Passenger_Accept2 = 211,239

# Button Region (x1, x2, y1, y2)
Region_XuanShang = 750-5, 750+5, 458-5, 458+5
Region_TiaoZhan = 790, 901, 417, 465
Region_KaiShiZhanDou = 1098-5, 1098+5, 591-5, 591+5
Region_Bonus = 980, 1030, 225, 275
Region_Driver_Invite_CheckButton = 490, 505, 310, 327
Region_Driver_Invite_OK = 600, 747, 360, 405
Region_Passenger_Accept = 193, 227, 212, 245

# Color Baseline
Color_XuanShang = "df715e"
Color_TiaoZhan_Single = "f3b25e"
Color_KaiShiZhanDou_Ready = "e7c769"
Color_KaiShiZhanDou_Waiting = "c6c6c6"
Color_KaiShiZhanDou_Passenger = "f8f3e0"
Color_InTheBattle = "f7f2df"
Color_Finished = "e8d9ce"
Color_Bonus = "746c67"
Color_Driver_Invite_CheckButton_NO = "725f4d"
Color_Driver_Invite_CheckButton_YES = "4b5ee9"
Color_Driver_Invite_OK = "f3b25e"
Color_Passenger_Accept = "58b563"


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
