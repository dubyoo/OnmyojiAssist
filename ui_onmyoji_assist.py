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
        OnmyojiAssist.resize(367, 178)
        self.verticalLayout = QtWidgets.QVBoxLayout(OnmyojiAssist)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_counter = QtWidgets.QHBoxLayout()
        self.horizontalLayout_counter.setObjectName("horizontalLayout_counter")
        self.checkBox_count = QtWidgets.QCheckBox(OnmyojiAssist)
        self.checkBox_count.setObjectName("checkBox_count")
        self.horizontalLayout_counter.addWidget(self.checkBox_count)
        self.spinBox_count = QtWidgets.QSpinBox(OnmyojiAssist)
        self.spinBox_count.setMaximum(99999)
        self.spinBox_count.setObjectName("spinBox_count")
        self.horizontalLayout_counter.addWidget(self.spinBox_count)
        self.verticalLayout.addLayout(self.horizontalLayout_counter)
        self.horizontalLayout_button = QtWidgets.QHBoxLayout()
        self.horizontalLayout_button.setObjectName("horizontalLayout_button")
        self.pushButton_start = QtWidgets.QPushButton(OnmyojiAssist)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout_button.addWidget(self.pushButton_start)
        self.pushButton_stop = QtWidgets.QPushButton(OnmyojiAssist)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout_button.addWidget(self.pushButton_stop)
        self.verticalLayout.addLayout(self.horizontalLayout_button)
        self.textBrowser = QtWidgets.QTextBrowser(OnmyojiAssist)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(OnmyojiAssist)
        QtCore.QMetaObject.connectSlotsByName(OnmyojiAssist)

    def retranslateUi(self, OnmyojiAssist):
        _translate = QtCore.QCoreApplication.translate
        OnmyojiAssist.setWindowTitle(_translate("OnmyojiAssist", "Onmyoji Assist"))
        self.checkBox_count.setText(_translate("OnmyojiAssist", "Count"))
        self.pushButton_start.setText(_translate("OnmyojiAssist", "Start"))
        self.pushButton_stop.setText(_translate("OnmyojiAssist", "Stop"))

