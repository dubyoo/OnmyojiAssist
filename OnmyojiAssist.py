# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from MyHelper import *
import OnmyojiThread
import ui_onmyoji_assist
import logging
import win32com.client


class OnmyojiAssist(QWidget):
    stop_signal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_onmyoji_assist.Ui_OnmyojiAssist()
        self.init_ui()
        self.main_ts = None  # win32com.client.Dispatch('ts.tssoft')
        self.threads = {}

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.spinBox_count.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)
        XStream.stdout().messageWritten.connect(self.ui.textBrowser.append)
        XStream.stderr().messageWritten.connect(self.ui.textBrowser.append)
        self.ui.checkBox_count.stateChanged.connect(self.on_checkbox_count_clicked)
        self.ui.pushButton_start.clicked.connect(self.start_all)
        self.ui.pushButton_stop.clicked.connect(self.stop_all)
        self.stop_signal.connect(self.stop_thread)

    def on_checkbox_count_clicked(self):
        self.ui.spinBox_count.setEnabled(True if self.ui.checkBox_count.checkState() == Qt.Checked else False)

    def detect_onmyoji_windows(self):
        # hwnd_raw = self.main_ts.EnumWindowByProcess("onmyoji.exe", "", "", 16)
        # handler_list = hwnd_raw.split(',')
        # logging.error('windows handle:', handler_list)
        # if len(handler_list) < 1:
        #     logging.error('Need at least one window!')
        #     return False
        # for i, handler in enumerate(handler_list):
        #     ts = win32com.client.Dispatch('ts.tssoft')
        #     if ts.BindWindow(handler, 'dx2', 'windows', 'windows', 0) != 1:
        #         logging.error('window binding failed')
        #         continue
        for i in range(5):
            count = self.ui.spinBox_count.value() if self.ui.checkBox_count.checkState() == Qt.Checked else 0
            onmyoji_thread = OnmyojiThread.OnmyojiThread(self, None)  # ts)
            onmyoji_thread.set_count(count)
            onmyoji_thread.setName(str(i))
            self.threads[i] = onmyoji_thread
        return True

    def start_all(self):
        self.detect_onmyoji_windows()
        self.ui.pushButton_stop.setEnabled(True)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.checkBox_count.setEnabled(False)
        self.ui.spinBox_count.setEnabled(False)
        # keep_awake()
        logging.info('start all threads')
        for thread in self.threads.values():
            thread.start()

    def stop_all(self):
        logging.info('stop all threads')
        for thread in self.threads.values():
            thread.stop()
        for thread in self.threads.values():
            thread.join()
            # thread.unbind_window()
        self.threads.clear()
        # keep_awake(False)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.checkBox_count.setEnabled(True)
        self.on_checkbox_count_clicked()

    def stop_thread(self, index):
        thread = self.threads.pop(index)
        if thread is not None:
            thread.stop()
            thread.join()
            # thread.unbind_window()
        # logging.info(self.threads)
        if len(self.threads) == 0:
            self.stop_all()

    def closeEvent(self, close_event):
        self.stop_all()
