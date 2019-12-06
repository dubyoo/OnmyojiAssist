# -*- coding: utf-8 -*-
import time
import random
import ctypes
import logging
import sys
from PyQt5 import QtCore


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


def bind_window(ts_plugin, window_name):
    need_ver = '4.019'
    if ts_plugin.ver() != need_ver:
        logging.error('register failed')
        return False
    else:
        logging.info('register success')

    hwnd = ts_plugin.FindWindow('', window_name)
    ts_ret = ts_plugin.BindWindow(hwnd, 'dx2', 'windows', 'windows', 0)
    if ts_ret != 1:
        logging.error('binding failed')
        return False
    logging.info('binding success')
    return True


def unbind_window(ts_plugin):
    logging.info('UnBindWindow return: %d' % ts_plugin.UnBindWindow())
