# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RawSequenceOptionsGui.ui'
#
# Created: Mon Jun  8 13:07:42 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(262, 338)
        Dialog.setAutoFillBackground(False)
        self.verticalLayout_5 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_5.addWidget(self.label)
        self.rebinComboBox = QtGui.QComboBox(Dialog)
        self.rebinComboBox.setObjectName(_fromUtf8("rebinComboBox"))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.rebinComboBox.addItem(_fromUtf8(""))
        self.verticalLayout_5.addWidget(self.rebinComboBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.LCcheckBox = QtGui.QCheckBox(Dialog)
        self.LCcheckBox.setObjectName(_fromUtf8("LCcheckBox"))
        self.verticalLayout.addWidget(self.LCcheckBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setEnabled(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.leftLCSpinBox = QtGui.QSpinBox(Dialog)
        self.leftLCSpinBox.setEnabled(False)
        self.leftLCSpinBox.setObjectName(_fromUtf8("leftLCSpinBox"))
        self.horizontalLayout_2.addWidget(self.leftLCSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.rightLCSpinBox = QtGui.QSpinBox(Dialog)
        self.rightLCSpinBox.setEnabled(False)
        self.rightLCSpinBox.setObjectName(_fromUtf8("rightLCSpinBox"))
        self.horizontalLayout_3.addWidget(self.rightLCSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        self.cropCheckBox = QtGui.QCheckBox(Dialog)
        self.cropCheckBox.setObjectName(_fromUtf8("cropCheckBox"))
        self.verticalLayout_5.addWidget(self.cropCheckBox)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setEnabled(False)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.leftCropSpinBox = QtGui.QSpinBox(Dialog)
        self.leftCropSpinBox.setEnabled(False)
        self.leftCropSpinBox.setMinimum(0)
        self.leftCropSpinBox.setMaximum(10000)
        self.leftCropSpinBox.setObjectName(_fromUtf8("leftCropSpinBox"))
        self.horizontalLayout_4.addWidget(self.leftCropSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setEnabled(False)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_5.addWidget(self.label_5)
        self.rightCropSpinBox = QtGui.QSpinBox(Dialog)
        self.rightCropSpinBox.setEnabled(False)
        self.rightCropSpinBox.setMinimum(-1)
        self.rightCropSpinBox.setMaximum(10000)
        self.rightCropSpinBox.setProperty("value", -1)
        self.rightCropSpinBox.setObjectName(_fromUtf8("rightCropSpinBox"))
        self.horizontalLayout_5.addWidget(self.rightCropSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setEnabled(False)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_7.addWidget(self.label_7)
        self.topCropSpinBox = QtGui.QSpinBox(Dialog)
        self.topCropSpinBox.setEnabled(False)
        self.topCropSpinBox.setMinimum(-1)
        self.topCropSpinBox.setMaximum(10000)
        self.topCropSpinBox.setProperty("value", -1)
        self.topCropSpinBox.setObjectName(_fromUtf8("topCropSpinBox"))
        self.horizontalLayout_7.addWidget(self.topCropSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setEnabled(False)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.bottomCropSpinBox = QtGui.QSpinBox(Dialog)
        self.bottomCropSpinBox.setEnabled(False)
        self.bottomCropSpinBox.setMinimum(-1)
        self.bottomCropSpinBox.setMaximum(10000)
        self.bottomCropSpinBox.setProperty("value", 0)
        self.bottomCropSpinBox.setObjectName(_fromUtf8("bottomCropSpinBox"))
        self.horizontalLayout_6.addWidget(self.bottomCropSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rotateCheckBox = QtGui.QCheckBox(Dialog)
        self.rotateCheckBox.setObjectName(_fromUtf8("rotateCheckBox"))
        self.horizontalLayout.addWidget(self.rotateCheckBox)
        self.rotateComboBox = QtGui.QComboBox(Dialog)
        self.rotateComboBox.setEnabled(False)
        self.rotateComboBox.setObjectName(_fromUtf8("rotateComboBox"))
        self.rotateComboBox.addItem(_fromUtf8(""))
        self.rotateComboBox.addItem(_fromUtf8(""))
        self.rotateComboBox.addItem(_fromUtf8(""))
        self.rotateComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.rotateComboBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_5.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.rebinComboBox.setCurrentIndex(3)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Raw Sequence Options", None))
        self.label.setText(_translate("Dialog", "Rebin", None))
        self.rebinComboBox.setItemText(0, _translate("Dialog", "0.125", None))
        self.rebinComboBox.setItemText(1, _translate("Dialog", "0.25", None))
        self.rebinComboBox.setItemText(2, _translate("Dialog", "0.5", None))
        self.rebinComboBox.setItemText(3, _translate("Dialog", "1", None))
        self.rebinComboBox.setItemText(4, _translate("Dialog", "2", None))
        self.rebinComboBox.setItemText(5, _translate("Dialog", "4", None))
        self.rebinComboBox.setItemText(6, _translate("Dialog", "8", None))
        self.LCcheckBox.setText(_translate("Dialog", "Line correction", None))
        self.label_2.setText(_translate("Dialog", "Left", None))
        self.label_3.setText(_translate("Dialog", "Right", None))
        self.cropCheckBox.setText(_translate("Dialog", "Crop", None))
        self.label_4.setText(_translate("Dialog", "Left", None))
        self.label_5.setText(_translate("Dialog", "Right", None))
        self.label_7.setText(_translate("Dialog", "Top", None))
        self.label_6.setText(_translate("Dialog", "Bottom", None))
        self.rotateCheckBox.setText(_translate("Dialog", "Rotate (buggy)", None))
        self.rotateComboBox.setItemText(0, _translate("Dialog", "0", None))
        self.rotateComboBox.setItemText(1, _translate("Dialog", "90", None))
        self.rotateComboBox.setItemText(2, _translate("Dialog", "180", None))
        self.rotateComboBox.setItemText(3, _translate("Dialog", "270", None))

