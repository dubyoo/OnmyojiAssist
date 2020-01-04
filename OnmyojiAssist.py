# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from MyHelper import *
import OnmyojiThread
import ui_onmyoji_assist
import win32com.client


class OnmyojiAssist(QWidget):
    stop_signal = pyqtSignal(int)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_onmyoji_assist.Ui_OnmyojiAssist()
        self.init_ui()
        self.threads = {}
        try:
            self.main_ts = win32com.client.Dispatch('ts.tssoft')
        except:
            logger.error("加载天使插件失败")
            self.ui.pushButton_start.setEnabled(False)

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.spinBox_count.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_stop_after_finish.setEnabled(False)
        XStream.stdout().messageWritten.connect(self.ui.textBrowser.append)
        XStream.stderr().messageWritten.connect(self.ui.textBrowser.append)
        self.ui.checkBox_count.stateChanged.connect(self.on_checkbox_count_clicked)
        self.ui.checkBox_shutdown.stateChanged.connect(self.on_checkbox_count_clicked)
        self.ui.pushButton_start.clicked.connect(self.on_start_button_clicked)
        self.ui.pushButton_stop.clicked.connect(self.on_stop_button_clicked)
        self.ui.pushButton_stop_after_finish.clicked.connect(self.on_stop_after_finish_button_clicked)
        self.ui.pushButton_log_level.setCheckable(True)
        self.ui.pushButton_log_level.clicked[bool].connect(self.on_log_level_clicked)
        self.stop_signal.connect(self.stop_thread)

    def on_log_level_clicked(self, pressed):
        if pressed:
            logger.info('当前日志等级调整为：详细')
            self.ui.pushButton_log_level.setText('当前日志等级：详细')
            logger.setLevel(logging.DEBUG)
        else:
            logger.info('当前日志等级调整为：精简')
            self.ui.pushButton_log_level.setText('当前日志等级：精简')
            logger.setLevel(logging.INFO)

    def on_checkbox_count_clicked(self):
        self.ui.spinBox_count.setEnabled(True if self.ui.checkBox_count.checkState() == Qt.Checked else False)

    def detect_onmyoji_windows(self):
        hwnd_raw = self.main_ts.EnumWindowByProcess("onmyoji.exe", "", "", 16)
        handler_list = hwnd_raw.split(',')
        if handler_list == ['']:
            logger.error('未检测到运行中的窗口')
            return False
        for i, handler in enumerate(handler_list):
            ts = win32com.client.Dispatch('ts.tssoft')
            if ts.BindWindow(handler, 'dx2', 'windows', 'windows', 0) != 1:
                logger.error('窗口绑定失败')
                return False
            size = ts.GetClientSize(handler)  # size: (ret, width, height)
            if size[1] != 1136 or size[2] != 640:
                rect = ts.GetWindowRect(handler)  # rect: (ret, x1, y1, x2, y2)
                ts.SetClientSize(handler, 1136, 640)
                ts.MoveWindow(handler, rect[1], rect[2])
            count = self.ui.spinBox_count.value() if self.ui.checkBox_count.checkState() == Qt.Checked else 0
            onmyoji_thread = OnmyojiThread.OnmyojiThread(self, ts)
            onmyoji_thread.set_count(count)
            onmyoji_thread.setName(str(i))
            self.threads[i] = onmyoji_thread
        return True
        #
        # for i in range(3):
        #     count = self.ui.spinBox_count.value() if self.ui.checkBox_count.checkState() == Qt.Checked else 0
        #     onmyoji_thread = OnmyojiThread.OnmyojiThread(self, None)
        #     onmyoji_thread.set_count(count)
        #     onmyoji_thread.setName(str(i))
        #     self.threads[i] = onmyoji_thread
        # return True

    def on_start_button_clicked(self):
        if not self.detect_onmyoji_windows():
            return
        self.ui.pushButton_stop.setEnabled(True)
        self.ui.pushButton_stop_after_finish.setEnabled(True)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.checkBox_count.setEnabled(False)
        self.ui.spinBox_count.setEnabled(False)
        keep_awake()
        logger.info('开始所有线程')
        for thread in self.threads.values():
            thread.start()

    def on_stop_after_finish_button_clicked(self):
        logger.info('!!! 本次通关后即将全部停止 !!!')
        if self.ui.checkBox_shutdown.checkState():
            logger.info('任务被手动停止，取消[完成后关机]')
            self.ui.checkBox_shutdown.setCheckState(Qt.Unchecked)
        for thread in self.threads.values():
            thread.set_stop_after_finish()

    def on_stop_button_clicked(self):
        if self.ui.checkBox_shutdown.checkState():
            logger.info('任务被手动停止，取消[完成后关机]')
            self.ui.checkBox_shutdown.setCheckState(Qt.Unchecked)
        self.stop_all()

    def stop_all(self):
        logger.info('停止所有线程')
        for thread in self.threads.values():
            thread.stop()
        for thread in self.threads.values():
            thread.join()
            thread.unbind_window()
        self.threads.clear()
        keep_awake(False)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_stop_after_finish.setEnabled(False)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.checkBox_count.setEnabled(True)
        self.on_checkbox_count_clicked()
        if self.ui.checkBox_shutdown.checkState():
            logger.info('!!! 系统将在 30s 后关机 !!!')
            reply = TimedMessageBox(30, self).exec_()
            if reply == QMessageBox.Ok:
                logger.info("已取消自动关机")

    def stop_thread(self, index):
        thread = self.threads.pop(index)
        if thread is not None:
            thread.stop()
            thread.join()
            thread.unbind_window()
        logger.info("还有 %d 个线程正在运行", len(self.threads))
        if len(self.threads) == 0:
            self.stop_all()

    def closeEvent(self, close_event):
        if self.ui.checkBox_shutdown.checkState():
            self.ui.checkBox_shutdown.setCheckState(Qt.Unchecked)
        self.stop_all()
