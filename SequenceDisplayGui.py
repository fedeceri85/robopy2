# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SequenceDisplayGui.ui'
#
# Created: Tue May  7 21:46:50 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SequenceDisplayWnd(object):
    def setupUi(self, SequenceDisplayWnd):
        SequenceDisplayWnd.setObjectName(_fromUtf8("SequenceDisplayWnd"))
        SequenceDisplayWnd.resize(640, 480)
        self.centralwidget = QtGui.QWidget(SequenceDisplayWnd)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ImageFrameWidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.ImageFrameWidget.sizePolicy().hasHeightForWidth())
        self.ImageFrameWidget.setSizePolicy(sizePolicy)
        self.ImageFrameWidget.setObjectName(_fromUtf8("ImageFrameWidget"))
        self.verticalLayout.addWidget(self.ImageFrameWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.CurrentFrameSpinBox = QtGui.QSpinBox(self.centralwidget)
        self.CurrentFrameSpinBox.setMaximum(100000)
        self.CurrentFrameSpinBox.setObjectName(_fromUtf8("CurrentFrameSpinBox"))
        self.horizontalLayout.addWidget(self.CurrentFrameSpinBox)
        self.FirstFrameButton = QtGui.QPushButton(self.centralwidget)
        self.FirstFrameButton.setObjectName(_fromUtf8("FirstFrameButton"))
        self.horizontalLayout.addWidget(self.FirstFrameButton)
        self.BackFrameButton = QtGui.QPushButton(self.centralwidget)
        self.BackFrameButton.setObjectName(_fromUtf8("BackFrameButton"))
        self.horizontalLayout.addWidget(self.BackFrameButton)
        self.PlayButton = QtGui.QPushButton(self.centralwidget)
        self.PlayButton.setObjectName(_fromUtf8("PlayButton"))
        self.horizontalLayout.addWidget(self.PlayButton)
        self.ForwardFrameButton = QtGui.QPushButton(self.centralwidget)
        self.ForwardFrameButton.setObjectName(_fromUtf8("ForwardFrameButton"))
        self.horizontalLayout.addWidget(self.ForwardFrameButton)
        self.LastFrameButton = QtGui.QPushButton(self.centralwidget)
        self.LastFrameButton.setObjectName(_fromUtf8("LastFrameButton"))
        self.horizontalLayout.addWidget(self.LastFrameButton)
        self.CurrentFrameSlider = QtGui.QSlider(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CurrentFrameSlider.sizePolicy().hasHeightForWidth())
        self.CurrentFrameSlider.setSizePolicy(sizePolicy)
        self.CurrentFrameSlider.setOrientation(QtCore.Qt.Horizontal)
        self.CurrentFrameSlider.setObjectName(_fromUtf8("CurrentFrameSlider"))
        self.horizontalLayout.addWidget(self.CurrentFrameSlider)
        spacerItem = QtGui.QSpacerItem(178, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        SequenceDisplayWnd.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SequenceDisplayWnd)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        SequenceDisplayWnd.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SequenceDisplayWnd)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SequenceDisplayWnd.setStatusBar(self.statusbar)

        self.retranslateUi(SequenceDisplayWnd)
        QtCore.QMetaObject.connectSlotsByName(SequenceDisplayWnd)

    def retranslateUi(self, SequenceDisplayWnd):
        SequenceDisplayWnd.setWindowTitle(_translate("SequenceDisplayWnd", "SequenceDisplay", None))
        self.FirstFrameButton.setText(_translate("SequenceDisplayWnd", "<<", None))
        self.BackFrameButton.setText(_translate("SequenceDisplayWnd", "<", None))
        self.PlayButton.setText(_translate("SequenceDisplayWnd", "P", None))
        self.ForwardFrameButton.setText(_translate("SequenceDisplayWnd", ">", None))
        self.LastFrameButton.setText(_translate("SequenceDisplayWnd", ">>", None))

