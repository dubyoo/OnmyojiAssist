# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QButtonGroup
from PyQt5.QtCore import Qt
from MyHelper import *
import Onmyoji
import ui_onmyoji_assist
import threading
import logging
import win32com.client


class OnmyojiAssist(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_onmyoji_assist.Ui_OnmyojiAssist()
        self.init_ui()
        self.thread = None
        self.ts = None  # win32com.client.Dispatch('ts.tssoft')
        self.single = False
        self.dual = False
        self.onmyoji = Onmyoji.Onmyoji(self, self.ts)

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.spinBox_count.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)
        XStream.stdout().messageWritten.connect(self.ui.textBrowser.append)
        XStream.stderr().messageWritten.connect(self.ui.textBrowser.append)
        self.ui.checkBox_count.stateChanged.connect(self.on_checkbox_count_clicked)
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_stop.clicked.connect(self.stop)

    def on_checkbox_count_clicked(self):
        self.ui.spinBox_count.setEnabled(True if self.ui.checkBox_count.checkState() == Qt.Checked else False)

    def start(self):
        self.ui.pushButton_stop.setEnabled(True)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.checkBox_count.setEnabled(False)
        self.ui.spinBox_count.setEnabled(False)
        count = self.ui.spinBox_count.value() if self.ui.checkBox_count.checkState() == Qt.Checked else 0
        self.onmyoji.set_counts(count)
        # if not bind_window(self.ts, self.bind_window_name):
        #     logging.error('bind error')
        #     return
        # keep_awake()
        self.thread = threading.Thread(target=self.onmyoji.run)
        logging.debug('thread started')
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.onmyoji.terminate()
            self.thread.join()
            self.thread = None
            logging.debug('thread stopped')
        # unbind_window(self.ts)
        # keep_awake(False)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.checkBox_count.setEnabled(True)
        self.on_checkbox_count_clicked()

    def closeEvent(self, close_event):
        self.stop()
