# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twitch.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TwitchWindow(object):
    def setupUi(self, TwitchWindow):
        TwitchWindow.setObjectName("TwitchWindow")
        TwitchWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TwitchWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(TwitchWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 791, 531))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.main_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.main_layout.setObjectName("main_layout")
        self.center_layout = QtWidgets.QGridLayout()
        self.center_layout.setObjectName("center_layout")
        self.main_layout.addLayout(self.center_layout, 0, 1, 1, 1)
        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_layout.setObjectName("left_layout")
        self.main_layout.addLayout(self.left_layout, 0, 0, 1, 1)
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setObjectName("right_layout")
        self.main_layout.addLayout(self.right_layout, 0, 2, 1, 1)
        TwitchWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TwitchWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        TwitchWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TwitchWindow)
        self.statusbar.setObjectName("statusbar")
        TwitchWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TwitchWindow)
        QtCore.QMetaObject.connectSlotsByName(TwitchWindow)

    def retranslateUi(self, TwitchWindow):
        _translate = QtCore.QCoreApplication.translate
        TwitchWindow.setWindowTitle(_translate("TwitchWindow", "Twitch.py"))

