# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\gleb\diploma\fingerprint-recognition-main\design.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(793, 552)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadImage = QtWidgets.QPushButton(self.centralwidget)
        self.loadImage.setGeometry(QtCore.QRect(340, 10, 141, 31))
        self.loadImage.setObjectName("loadImage")
        self.processImage = QtWidgets.QPushButton(self.centralwidget)
        self.processImage.setGeometry(QtCore.QRect(80, 330, 141, 31))
        self.processImage.setObjectName("processImage")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 330, 141, 31))
        self.pushButton.setObjectName("pushButton")
        self.srcInfo = QtWidgets.QLabel(self.centralwidget)
        self.srcInfo.setGeometry(QtCore.QRect(80, 70, 141, 16))
        self.srcInfo.setObjectName("srcInfo")
        self.reconInfo = QtWidgets.QLabel(self.centralwidget)
        self.reconInfo.setGeometry(QtCore.QRect(310, 70, 151, 16))
        self.reconInfo.setObjectName("reconInfo")
        self.reconInfoText = QtWidgets.QLabel(self.centralwidget)
        self.reconInfoText.setGeometry(QtCore.QRect(530, 340, 221, 21))
        self.reconInfoText.setObjectName("reconInfoText")
        self.infoAboutImage = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.infoAboutImage.setGeometry(QtCore.QRect(530, 370, 201, 71))
        self.infoAboutImage.setObjectName("infoAboutImage")
        self.sourceImgLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceImgLabel.setGeometry(QtCore.QRect(60, 90, 191, 231))
        self.sourceImgLabel.setStyleSheet("border-style: solid;\n"
"border-width: 1px;\n"
"border-color: black;")
        self.sourceImgLabel.setText("")
        self.sourceImgLabel.setObjectName("sourceImgLabel")
        self.procImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.procImageLabel.setGeometry(QtCore.QRect(300, 90, 191, 231))
        self.procImageLabel.setStyleSheet("border-style: solid;\n"
"border-width: 1px;\n"
"border-color: black;")
        self.procImageLabel.setText("")
        self.procImageLabel.setObjectName("procImageLabel")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 40, 801, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.foundImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.foundImageLabel.setGeometry(QtCore.QRect(530, 90, 191, 231))
        self.foundImageLabel.setStyleSheet("border-style: solid;\n"
"border-width: 1px;\n"
"border-color: black;")
        self.foundImageLabel.setText("")
        self.foundImageLabel.setObjectName("foundImageLabel")
        self.foundInfoText = QtWidgets.QLabel(self.centralwidget)
        self.foundInfoText.setGeometry(QtCore.QRect(560, 70, 151, 16))
        self.foundInfoText.setObjectName("foundInfoText")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadImage.setText(_translate("MainWindow", "Load Source Image"))
        self.processImage.setText(_translate("MainWindow", "Process a fingerprint"))
        self.pushButton.setText(_translate("MainWindow", "Recognize a fingerprint"))
        self.srcInfo.setText(_translate("MainWindow", "Source Image Window"))
        self.reconInfo.setText(_translate("MainWindow", "Processed Image Window"))
        self.reconInfoText.setText(_translate("MainWindow", "Information about recognized print"))
        self.foundInfoText.setText(_translate("MainWindow", "Founded fingerprint"))

