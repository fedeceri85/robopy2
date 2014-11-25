# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SaveRawSequenceOptionsGui.ui'
#
# Created: Tue Oct 21 10:51:07 2014
#      by: PyQt4 UI code generator 4.11.2
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
        frameIntervalDialog.resize(229, 183)
        self.verticalLayout_3 = QtGui.QVBoxLayout(frameIntervalDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(frameIntervalDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.label_4 = QtGui.QLabel(frameIntervalDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_2 = QtGui.QLabel(frameIntervalDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(frameIntervalDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.firstFrameSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.firstFrameSpinBox.setObjectName(_fromUtf8("firstFrameSpinBox"))
        self.verticalLayout.addWidget(self.firstFrameSpinBox)
        self.stepSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.stepSpinBox.setObjectName(_fromUtf8("stepSpinBox"))
        self.verticalLayout.addWidget(self.stepSpinBox)
        self.lastFrameSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.lastFrameSpinBox.setObjectName(_fromUtf8("lastFrameSpinBox"))
        self.verticalLayout.addWidget(self.lastFrameSpinBox)
        self.compLevelSpinBox = QtGui.QSpinBox(frameIntervalDialog)
        self.compLevelSpinBox.setMaximum(10)
        self.compLevelSpinBox.setProperty("value", 5)
        self.compLevelSpinBox.setObjectName(_fromUtf8("compLevelSpinBox"))
        self.verticalLayout.addWidget(self.compLevelSpinBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(frameIntervalDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(frameIntervalDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), frameIntervalDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), frameIntervalDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(frameIntervalDialog)

    def retranslateUi(self, frameIntervalDialog):
        frameIntervalDialog.setWindowTitle(_translate("frameIntervalDialog", "Select frames", None))
        self.label.setText(_translate("frameIntervalDialog", "First frame", None))
        self.label_4.setText(_translate("frameIntervalDialog", "Step", None))
        self.label_2.setText(_translate("frameIntervalDialog", "Last Frame", None))
        self.label_3.setText(_translate("frameIntervalDialog", "Compression level (HDF only)", None))

