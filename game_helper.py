# -*- coding:utf-8 -*-
import ctypes
import logging
import sys
import os
import random
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox

IMG_TEAM_TIAO_ZHAN = (1054, 552, 1110, 594)
IMG_TEAM_READY = (21, 14, 191, 56)
IMG_XUAN_SHANG = (496, 137, 620, 176)

POS_REJECT_XUAN_SHANG = (739, 442, 776, 480)
POS_TEAM_TIAO_ZHAN = IMG_TEAM_TIAO_ZHAN

POS_OVERFLOW_OK_LT = (515, 354)
POS_OVERFLOW_OK_RB = (620, 396)

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


def keep_awake(enable=True):
    """
    make the screen keep awake, do not go to sleep mode
    """
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    if enable:
        logger.info('enable screen awake')
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
    else:
        logger.info('disable screen awake')
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def random_sleep(sleep_time, variable_time=0):
    """
    随机睡眠一段时间，单位是 ms
    """
    slp = random.randint(sleep_time, sleep_time + variable_time)
    time.sleep(slp / 1000)

