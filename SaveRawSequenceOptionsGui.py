# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SaveRawSequenceOptions.ui'
#
# Created: Thu Apr  3 11:08:26 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_frameIntervalDialog(object):
    def setupUi(self, frameIntervalDialog):
        frameIntervalDialog.setObjectName(_fromUtf8("frameIntervalDialog"))
        frameIntervalDialog.resize(251, 117)
        self.gridLayout = QtGui.QGridLayout(frameIntervalDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(frameIntervalDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.firstFrameSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.firstFrameSpinBox.setObjectName(_fromUtf8("firstFrameSpinBox"))
        self.gridLayout.addWidget(self.firstFrameSpinBox, 0, 2, 1, 1)
        self.label = QtGui.QLabel(frameIntervalDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.stepSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.stepSpinBox.setProperty("value", 1)
        self.stepSpinBox.setObjectName(_fromUtf8("stepSpinBox"))
        self.gridLayout.addWidget(self.stepSpinBox, 1, 1, 1, 2)
        self.label_2 = QtGui.QLabel(frameIntervalDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.lastFrameSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.lastFrameSpinBox.setObjectName(_fromUtf8("lastFrameSpinBox"))
        self.gridLayout.addWidget(self.lastFrameSpinBox, 2, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(frameIntervalDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)

        self.retranslateUi(frameIntervalDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), frameIntervalDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), frameIntervalDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(frameIntervalDialog)

    def retranslateUi(self, frameIntervalDialog):
        frameIntervalDialog.setWindowTitle(_translate("frameIntervalDialog", "Select frames", None))
        self.label_3.setText(_translate("frameIntervalDialog", "Step             ", None))
        self.label.setText(_translate("frameIntervalDialog", "First frame", None))
        self.label_2.setText(_translate("frameIntervalDialog", "Last Frame", None))

