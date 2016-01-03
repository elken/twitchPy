# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twitch.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


# noinspection PyArgumentList,PyTypeChecker
class Ui_TwitchWindow(object):
    def setupUi(self, TwitchWindow):
        TwitchWindow.setObjectName("TwitchWindow")
        TwitchWindow.resize(1081, 769)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TwitchWindow.sizePolicy().hasHeightForWidth())
        TwitchWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TwitchWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(TwitchWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.main_layout.setObjectName("main_layout")
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setObjectName("right_layout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.right_layout.addWidget(self.label_3)
        self.main_layout.addLayout(self.right_layout, 0, 2, 1, 1)
        self.center_layout = QtWidgets.QGridLayout()
        self.center_layout.setHorizontalSpacing(10)
        self.center_layout.setObjectName("center_layout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.center_layout.addWidget(self.label_2, 0, 0, 1, 1)
        self.main_layout.addLayout(self.center_layout, 0, 1, 1, 1)
        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_layout.setObjectName("left_layout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.left_layout.addWidget(self.label)
        self.main_layout.addLayout(self.left_layout, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.main_layout)
        TwitchWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TwitchWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 21))
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
        self.label_3.setText(_translate("TwitchWindow", "right"))
        self.label_2.setText(_translate("TwitchWindow", "center"))
        self.label.setText(_translate("TwitchWindow", "left"))
