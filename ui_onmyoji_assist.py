# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_onmyoji_assist.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OnmyojiAssist(object):
    def setupUi(self, OnmyojiAssist):
        OnmyojiAssist.setObjectName("OnmyojiAssist")
        OnmyojiAssist.resize(540, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(OnmyojiAssist)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_counter = QtWidgets.QHBoxLayout()
        self.horizontalLayout_counter.setObjectName("horizontalLayout_counter")
        self.checkBox_count = QtWidgets.QCheckBox(OnmyojiAssist)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.checkBox_count.setFont(font)
        self.checkBox_count.setObjectName("checkBox_count")
        self.horizontalLayout_counter.addWidget(self.checkBox_count)
        self.spinBox_count = QtWidgets.QSpinBox(OnmyojiAssist)
        self.spinBox_count.setMaximum(99999)
        self.spinBox_count.setObjectName("spinBox_count")
        self.horizontalLayout_counter.addWidget(self.spinBox_count)
        self.verticalLayout.addLayout(self.horizontalLayout_counter)
        self.checkBox_close_buff = QtWidgets.QCheckBox(OnmyojiAssist)
        self.checkBox_close_buff.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.checkBox_close_buff.setFont(font)
        self.checkBox_close_buff.setChecked(False)
        self.checkBox_close_buff.setObjectName("checkBox_close_buff")
        self.verticalLayout.addWidget(self.checkBox_close_buff)
        self.checkBox_shutdown = QtWidgets.QCheckBox(OnmyojiAssist)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.checkBox_shutdown.setFont(font)
        self.checkBox_shutdown.setObjectName("checkBox_shutdown")
        self.verticalLayout.addWidget(self.checkBox_shutdown)
        self.horizontalLayout_button = QtWidgets.QHBoxLayout()
        self.horizontalLayout_button.setObjectName("horizontalLayout_button")
        self.pushButton_start = QtWidgets.QPushButton(OnmyojiAssist)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_start.setFont(font)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout_button.addWidget(self.pushButton_start)
        self.pushButton_stop_after_finish = QtWidgets.QPushButton(OnmyojiAssist)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_stop_after_finish.setFont(font)
        self.pushButton_stop_after_finish.setObjectName("pushButton_stop_after_finish")
        self.horizontalLayout_button.addWidget(self.pushButton_stop_after_finish)
        self.pushButton_stop = QtWidgets.QPushButton(OnmyojiAssist)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout_button.addWidget(self.pushButton_stop)
        self.verticalLayout.addLayout(self.horizontalLayout_button)
        self.pushButton_log_level = QtWidgets.QPushButton(OnmyojiAssist)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.pushButton_log_level.setFont(font)
        self.pushButton_log_level.setObjectName("pushButton_log_level")
        self.verticalLayout.addWidget(self.pushButton_log_level)
        self.textBrowser = QtWidgets.QTextBrowser(OnmyojiAssist)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(OnmyojiAssist)
        QtCore.QMetaObject.connectSlotsByName(OnmyojiAssist)

    def retranslateUi(self, OnmyojiAssist):
        _translate = QtCore.QCoreApplication.translate
        OnmyojiAssist.setWindowTitle(_translate("OnmyojiAssist", "Onmyoji Assist"))
        self.checkBox_count.setText(_translate("OnmyojiAssist", "计数"))
        self.checkBox_close_buff.setText(_translate("OnmyojiAssist", "完成后关闭 Buff"))
        self.checkBox_shutdown.setText(_translate("OnmyojiAssist", "完成后关机"))
        self.pushButton_start.setText(_translate("OnmyojiAssist", "开始"))
        self.pushButton_stop_after_finish.setText(_translate("OnmyojiAssist", "通关后停止"))
        self.pushButton_stop.setText(_translate("OnmyojiAssist", "立即停止"))
        self.pushButton_log_level.setText(_translate("OnmyojiAssist", "当前日志等级：精简"))

