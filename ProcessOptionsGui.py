# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProcessOptionsGui.ui'
#
# Created: Wed Jul 31 11:58:00 2013
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

class Ui_ProcessOptionsDlg(object):
    def setupUi(self, ProcessOptionsDlg):
        ProcessOptionsDlg.setObjectName(_fromUtf8("ProcessOptionsDlg"))
        ProcessOptionsDlg.resize(515, 380)
        self.verticalLayout = QtGui.QVBoxLayout(ProcessOptionsDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.PO_TabWidget = QtGui.QTabWidget(ProcessOptionsDlg)
        self.PO_TabWidget.setObjectName(_fromUtf8("PO_TabWidget"))
        self.FrameOptionsTab = QtGui.QWidget()
        self.FrameOptionsTab.setObjectName(_fromUtf8("FrameOptionsTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.FrameOptionsTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setHorizontalSpacing(15)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.FirstFrameLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.FirstFrameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FirstFrameLabel.setObjectName(_fromUtf8("FirstFrameLabel"))
        self.gridLayout.addWidget(self.FirstFrameLabel, 0, 0, 1, 1)
        self.FirstFrameSpinBox = QtGui.QSpinBox(self.FrameOptionsTab)
        self.FirstFrameSpinBox.setMinimum(1)
        self.FirstFrameSpinBox.setMaximum(99999)
        self.FirstFrameSpinBox.setObjectName(_fromUtf8("FirstFrameSpinBox"))
        self.gridLayout.addWidget(self.FirstFrameSpinBox, 0, 1, 1, 1)
        self.ProcessTypeLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.ProcessTypeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ProcessTypeLabel.setObjectName(_fromUtf8("ProcessTypeLabel"))
        self.gridLayout.addWidget(self.ProcessTypeLabel, 0, 2, 1, 1)
        self.ProcessTypeComboBox = QtGui.QComboBox(self.FrameOptionsTab)
        self.ProcessTypeComboBox.setObjectName(_fromUtf8("ProcessTypeComboBox"))
        self.ProcessTypeComboBox.addItem(_fromUtf8(""))
        self.ProcessTypeComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.ProcessTypeComboBox, 0, 3, 2, 1)
        self.LastFrameLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.LastFrameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.LastFrameLabel.setObjectName(_fromUtf8("LastFrameLabel"))
        self.gridLayout.addWidget(self.LastFrameLabel, 1, 0, 2, 1)
        self.LastFrameSpinBox = QtGui.QSpinBox(self.FrameOptionsTab)
        self.LastFrameSpinBox.setMinimum(1)
        self.LastFrameSpinBox.setMaximum(99999)
        self.LastFrameSpinBox.setObjectName(_fromUtf8("LastFrameSpinBox"))
        self.gridLayout.addWidget(self.LastFrameSpinBox, 1, 1, 2, 1)
        self.FirstWavelengthLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.FirstWavelengthLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FirstWavelengthLabel.setObjectName(_fromUtf8("FirstWavelengthLabel"))
        self.gridLayout.addWidget(self.FirstWavelengthLabel, 2, 2, 1, 1)
        self.FirstWavelengthSpinBox = QtGui.QSpinBox(self.FrameOptionsTab)
        self.FirstWavelengthSpinBox.setMinimum(1)
        self.FirstWavelengthSpinBox.setMaximum(99999)
        self.FirstWavelengthSpinBox.setObjectName(_fromUtf8("FirstWavelengthSpinBox"))
        self.gridLayout.addWidget(self.FirstWavelengthSpinBox, 2, 3, 1, 1)
        self.CycleSizeLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.CycleSizeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CycleSizeLabel.setObjectName(_fromUtf8("CycleSizeLabel"))
        self.gridLayout.addWidget(self.CycleSizeLabel, 3, 0, 1, 1)
        self.CycleSizeSpinBox = QtGui.QSpinBox(self.FrameOptionsTab)
        self.CycleSizeSpinBox.setMinimum(1)
        self.CycleSizeSpinBox.setMaximum(99999)
        self.CycleSizeSpinBox.setObjectName(_fromUtf8("CycleSizeSpinBox"))
        self.gridLayout.addWidget(self.CycleSizeSpinBox, 3, 1, 1, 1)
        self.SecondWavelengthLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.SecondWavelengthLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.SecondWavelengthLabel.setObjectName(_fromUtf8("SecondWavelengthLabel"))
        self.gridLayout.addWidget(self.SecondWavelengthLabel, 3, 2, 1, 1)
        self.SecondWavelengthSpinBox = QtGui.QSpinBox(self.FrameOptionsTab)
        self.SecondWavelengthSpinBox.setMinimum(1)
        self.SecondWavelengthSpinBox.setMaximum(99999)
        self.SecondWavelengthSpinBox.setObjectName(_fromUtf8("SecondWavelengthSpinBox"))
        self.gridLayout.addWidget(self.SecondWavelengthSpinBox, 3, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.FrameOptionsTab)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.DisplayTypeComboBox = QtGui.QComboBox(self.FrameOptionsTab)
        self.DisplayTypeComboBox.setObjectName(_fromUtf8("DisplayTypeComboBox"))
        self.DisplayTypeComboBox.addItem(_fromUtf8(""))
        self.DisplayTypeComboBox.addItem(_fromUtf8(""))
        self.DisplayTypeComboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.DisplayTypeComboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.referenceFramesLabel = QtGui.QLabel(self.FrameOptionsTab)
        self.referenceFramesLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.referenceFramesLabel.setObjectName(_fromUtf8("referenceFramesLabel"))
        self.horizontalLayout_2.addWidget(self.referenceFramesLabel)
        self.referenceFrameSpinBox = QtGui.QSpinBox(self.FrameOptionsTab)
        self.referenceFrameSpinBox.setMinimum(1)
        self.referenceFrameSpinBox.setMaximum(99999)
        self.referenceFrameSpinBox.setObjectName(_fromUtf8("referenceFrameSpinBox"))
        self.horizontalLayout_2.addWidget(self.referenceFrameSpinBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.PO_TabWidget.addTab(self.FrameOptionsTab, _fromUtf8(""))
        self.timeOptionsTab = QtGui.QWidget()
        self.timeOptionsTab.setObjectName(_fromUtf8("timeOptionsTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.timeOptionsTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.timesGroupBox = QtGui.QGroupBox(self.timeOptionsTab)
        self.timesGroupBox.setTitle(_fromUtf8(""))
        self.timesGroupBox.setObjectName(_fromUtf8("timesGroupBox"))
        self.time0SpinBox = QtGui.QSpinBox(self.timesGroupBox)
        self.time0SpinBox.setGeometry(QtCore.QRect(210, 150, 54, 24))
        self.time0SpinBox.setObjectName(_fromUtf8("time0SpinBox"))
        self.label_3 = QtGui.QLabel(self.timesGroupBox)
        self.label_3.setGeometry(QtCore.QRect(70, 160, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.layoutWidget = QtGui.QWidget(self.timesGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 327, 82))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.associatedTimesRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.associatedTimesRadioButton.setObjectName(_fromUtf8("associatedTimesRadioButton"))
        self.verticalLayout_3.addWidget(self.associatedTimesRadioButton)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.userInterframeRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.userInterframeRadioButton.setObjectName(_fromUtf8("userInterframeRadioButton"))
        self.horizontalLayout_3.addWidget(self.userInterframeRadioButton)
        self.interframeIntervalSpinBox = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.interframeIntervalSpinBox.setDecimals(2)
        self.interframeIntervalSpinBox.setMinimum(0.1)
        self.interframeIntervalSpinBox.setMaximum(10000.0)
        self.interframeIntervalSpinBox.setSingleStep(0.1)
        self.interframeIntervalSpinBox.setProperty("value", 0.1)
        self.interframeIntervalSpinBox.setObjectName(_fromUtf8("interframeIntervalSpinBox"))
        self.horizontalLayout_3.addWidget(self.interframeIntervalSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.FrameBasedRadioButton = QtGui.QRadioButton(self.layoutWidget)
        self.FrameBasedRadioButton.setObjectName(_fromUtf8("FrameBasedRadioButton"))
        self.verticalLayout_3.addWidget(self.FrameBasedRadioButton)
        self.gridLayout_2.addWidget(self.timesGroupBox, 0, 0, 1, 1)
        self.PO_TabWidget.addTab(self.timeOptionsTab, _fromUtf8(""))
        self.displayOptionsTab = QtGui.QWidget()
        self.displayOptionsTab.setObjectName(_fromUtf8("displayOptionsTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.displayOptionsTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.DOgroupBox = QtGui.QGroupBox(self.displayOptionsTab)
        self.DOgroupBox.setTitle(_fromUtf8(""))
        self.DOgroupBox.setObjectName(_fromUtf8("DOgroupBox"))
        self.layoutWidget1 = QtGui.QWidget(self.DOgroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 190, 54))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.LUTradioButton = QtGui.QRadioButton(self.layoutWidget1)
        self.LUTradioButton.setChecked(True)
        self.LUTradioButton.setObjectName(_fromUtf8("LUTradioButton"))
        self.horizontalLayout_4.addWidget(self.LUTradioButton)
        self.ColorMapcomboBox = QtGui.QComboBox(self.layoutWidget1)
        self.ColorMapcomboBox.setObjectName(_fromUtf8("ColorMapcomboBox"))
        self.ColorMapcomboBox.addItem(_fromUtf8(""))
        self.ColorMapcomboBox.addItem(_fromUtf8(""))
        self.ColorMapcomboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_4.addWidget(self.ColorMapcomboBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.HSVradioButton = QtGui.QRadioButton(self.layoutWidget1)
        self.HSVradioButton.setObjectName(_fromUtf8("HSVradioButton"))
        self.verticalLayout_4.addWidget(self.HSVradioButton)
        self.layoutWidget2 = QtGui.QWidget(self.DOgroupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(240, 33, 106, 49))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.medianFilterCheckbox = QtGui.QCheckBox(self.layoutWidget2)
        self.medianFilterCheckbox.setObjectName(_fromUtf8("medianFilterCheckbox"))
        self.verticalLayout_6.addWidget(self.medianFilterCheckbox)
        self.gaussianFilterCheckbox = QtGui.QCheckBox(self.layoutWidget2)
        self.gaussianFilterCheckbox.setObjectName(_fromUtf8("gaussianFilterCheckbox"))
        self.verticalLayout_6.addWidget(self.gaussianFilterCheckbox)
        self.gridLayout_3.addWidget(self.DOgroupBox, 0, 0, 1, 2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.chooseBackgroundButton = QtGui.QPushButton(self.displayOptionsTab)
        self.chooseBackgroundButton.setEnabled(False)
        self.chooseBackgroundButton.setObjectName(_fromUtf8("chooseBackgroundButton"))
        self.horizontalLayout_5.addWidget(self.chooseBackgroundButton)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 0, 1, 2)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.saturationLabel = QtGui.QLabel(self.displayOptionsTab)
        self.saturationLabel.setEnabled(False)
        self.saturationLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.saturationLabel.setObjectName(_fromUtf8("saturationLabel"))
        self.horizontalLayout_6.addWidget(self.saturationLabel)
        self.saturationSpinBox = QtGui.QDoubleSpinBox(self.displayOptionsTab)
        self.saturationSpinBox.setEnabled(False)
        self.saturationSpinBox.setMaximum(1.0)
        self.saturationSpinBox.setSingleStep(0.05)
        self.saturationSpinBox.setProperty("value", 1.0)
        self.saturationSpinBox.setObjectName(_fromUtf8("saturationSpinBox"))
        self.horizontalLayout_6.addWidget(self.saturationSpinBox)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)
        self.HSVbackGroupBox = QtGui.QGroupBox(self.displayOptionsTab)
        self.HSVbackGroupBox.setEnabled(False)
        self.HSVbackGroupBox.setObjectName(_fromUtf8("HSVbackGroupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.HSVbackGroupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.FrameByFrameRadioButton = QtGui.QRadioButton(self.HSVbackGroupBox)
        self.FrameByFrameRadioButton.setChecked(True)
        self.FrameByFrameRadioButton.setObjectName(_fromUtf8("FrameByFrameRadioButton"))
        self.verticalLayout_5.addWidget(self.FrameByFrameRadioButton)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.NomarskiRadioButton = QtGui.QRadioButton(self.HSVbackGroupBox)
        self.NomarskiRadioButton.setObjectName(_fromUtf8("NomarskiRadioButton"))
        self.horizontalLayout_7.addWidget(self.NomarskiRadioButton)
        self.backgroundLineEdit = QtGui.QLineEdit(self.HSVbackGroupBox)
        self.backgroundLineEdit.setEnabled(False)
        self.backgroundLineEdit.setObjectName(_fromUtf8("backgroundLineEdit"))
        self.horizontalLayout_7.addWidget(self.backgroundLineEdit)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.gridLayout_3.addWidget(self.HSVbackGroupBox, 2, 1, 1, 1)
        self.enlargeToBckCheckBox = QtGui.QCheckBox(self.displayOptionsTab)
        self.enlargeToBckCheckBox.setEnabled(False)
        self.enlargeToBckCheckBox.setObjectName(_fromUtf8("enlargeToBckCheckBox"))
        self.gridLayout_3.addWidget(self.enlargeToBckCheckBox, 3, 0, 1, 2)
        self.PO_TabWidget.addTab(self.displayOptionsTab, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.displayTimesCheckBox = QtGui.QCheckBox(self.tab)
        self.displayTimesCheckBox.setChecked(True)
        self.displayTimesCheckBox.setObjectName(_fromUtf8("displayTimesCheckBox"))
        self.verticalLayout_9.addWidget(self.displayTimesCheckBox)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.fontSizeLabel = QtGui.QLabel(self.tab)
        self.fontSizeLabel.setObjectName(_fromUtf8("fontSizeLabel"))
        self.horizontalLayout_8.addWidget(self.fontSizeLabel)
        self.fontSizeSpinBox = QtGui.QSpinBox(self.tab)
        self.fontSizeSpinBox.setProperty("value", 12)
        self.fontSizeSpinBox.setObjectName(_fromUtf8("fontSizeSpinBox"))
        self.horizontalLayout_8.addWidget(self.fontSizeSpinBox)
        self.verticalLayout_9.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.xOffsetLabel = QtGui.QLabel(self.tab)
        self.xOffsetLabel.setObjectName(_fromUtf8("xOffsetLabel"))
        self.horizontalLayout_9.addWidget(self.xOffsetLabel)
        self.xOffsetSpinBox = QtGui.QSpinBox(self.tab)
        self.xOffsetSpinBox.setMaximum(2560)
        self.xOffsetSpinBox.setProperty("value", 50)
        self.xOffsetSpinBox.setObjectName(_fromUtf8("xOffsetSpinBox"))
        self.horizontalLayout_9.addWidget(self.xOffsetSpinBox)
        self.verticalLayout_9.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.yOffsetLabel = QtGui.QLabel(self.tab)
        self.yOffsetLabel.setObjectName(_fromUtf8("yOffsetLabel"))
        self.horizontalLayout_10.addWidget(self.yOffsetLabel)
        self.yOffsetSpinBox = QtGui.QSpinBox(self.tab)
        self.yOffsetSpinBox.setMaximum(2560)
        self.yOffsetSpinBox.setProperty("value", 50)
        self.yOffsetSpinBox.setObjectName(_fromUtf8("yOffsetSpinBox"))
        self.horizontalLayout_10.addWidget(self.yOffsetSpinBox)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem1)
        self.scalebarCheckBox = QtGui.QCheckBox(self.tab)
        self.scalebarCheckBox.setChecked(True)
        self.scalebarCheckBox.setObjectName(_fromUtf8("scalebarCheckBox"))
        self.verticalLayout_9.addWidget(self.scalebarCheckBox)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_12.addWidget(self.label_2)
        self.sbScaleFactorSpinBox = QtGui.QDoubleSpinBox(self.tab)
        self.sbScaleFactorSpinBox.setDecimals(3)
        self.sbScaleFactorSpinBox.setMaximum(1000.0)
        self.sbScaleFactorSpinBox.setSingleStep(0.01)
        self.sbScaleFactorSpinBox.setProperty("value", 0.5)
        self.sbScaleFactorSpinBox.setObjectName(_fromUtf8("sbScaleFactorSpinBox"))
        self.horizontalLayout_12.addWidget(self.sbScaleFactorSpinBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_11.addWidget(self.label_4)
        self.sbLengthSpinBox = QtGui.QDoubleSpinBox(self.tab)
        self.sbLengthSpinBox.setDecimals(3)
        self.sbLengthSpinBox.setMaximum(1000.0)
        self.sbLengthSpinBox.setSingleStep(0.01)
        self.sbLengthSpinBox.setProperty("value", 25.0)
        self.sbLengthSpinBox.setObjectName(_fromUtf8("sbLengthSpinBox"))
        self.horizontalLayout_11.addWidget(self.sbLengthSpinBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_17.addWidget(self.label_5)
        self.lineSizeSpinBox = QtGui.QSpinBox(self.tab)
        self.lineSizeSpinBox.setMinimum(1)
        self.lineSizeSpinBox.setProperty("value", 10)
        self.lineSizeSpinBox.setObjectName(_fromUtf8("lineSizeSpinBox"))
        self.horizontalLayout_17.addWidget(self.lineSizeSpinBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_16.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.fontSizeLabel_2 = QtGui.QLabel(self.tab)
        self.fontSizeLabel_2.setObjectName(_fromUtf8("fontSizeLabel_2"))
        self.horizontalLayout_14.addWidget(self.fontSizeLabel_2)
        self.sbFontSizeSpinBox = QtGui.QSpinBox(self.tab)
        self.sbFontSizeSpinBox.setProperty("value", 12)
        self.sbFontSizeSpinBox.setObjectName(_fromUtf8("sbFontSizeSpinBox"))
        self.horizontalLayout_14.addWidget(self.sbFontSizeSpinBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.xOffsetLabel_2 = QtGui.QLabel(self.tab)
        self.xOffsetLabel_2.setObjectName(_fromUtf8("xOffsetLabel_2"))
        self.horizontalLayout_15.addWidget(self.xOffsetLabel_2)
        self.sbXOffsetSpinBox = QtGui.QSpinBox(self.tab)
        self.sbXOffsetSpinBox.setMaximum(2560)
        self.sbXOffsetSpinBox.setProperty("value", 50)
        self.sbXOffsetSpinBox.setObjectName(_fromUtf8("sbXOffsetSpinBox"))
        self.horizontalLayout_15.addWidget(self.sbXOffsetSpinBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.yOffsetLabel_2 = QtGui.QLabel(self.tab)
        self.yOffsetLabel_2.setObjectName(_fromUtf8("yOffsetLabel_2"))
        self.horizontalLayout_13.addWidget(self.yOffsetLabel_2)
        self.sbYOffsetSpinBox = QtGui.QSpinBox(self.tab)
        self.sbYOffsetSpinBox.setMaximum(2560)
        self.sbYOffsetSpinBox.setProperty("value", 50)
        self.sbYOffsetSpinBox.setObjectName(_fromUtf8("sbYOffsetSpinBox"))
        self.horizontalLayout_13.addWidget(self.sbYOffsetSpinBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_16.addLayout(self.verticalLayout_8)
        self.verticalLayout_9.addLayout(self.horizontalLayout_16)
        self.PO_TabWidget.addTab(self.tab, _fromUtf8(""))
        self.FiltersTab = QtGui.QWidget()
        self.FiltersTab.setObjectName(_fromUtf8("FiltersTab"))
        self.PO_TabWidget.addTab(self.FiltersTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.PO_TabWidget)

        self.retranslateUi(ProcessOptionsDlg)
        self.PO_TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProcessOptionsDlg)

    def retranslateUi(self, ProcessOptionsDlg):
        ProcessOptionsDlg.setWindowTitle(_translate("ProcessOptionsDlg", "Dialog", None))
        self.FirstFrameLabel.setText(_translate("ProcessOptionsDlg", "First frame:", None))
        self.ProcessTypeLabel.setText(_translate("ProcessOptionsDlg", "Process type:", None))
        self.ProcessTypeComboBox.setItemText(0, _translate("ProcessOptionsDlg", "Single wavelength", None))
        self.ProcessTypeComboBox.setItemText(1, _translate("ProcessOptionsDlg", "Ratiometric", None))
        self.LastFrameLabel.setText(_translate("ProcessOptionsDlg", "Last frame:", None))
        self.FirstWavelengthLabel.setText(_translate("ProcessOptionsDlg", "First wavelength:", None))
        self.CycleSizeLabel.setText(_translate("ProcessOptionsDlg", "Cycle size:", None))
        self.SecondWavelengthLabel.setText(_translate("ProcessOptionsDlg", "Second wavelength:", None))
        self.label.setText(_translate("ProcessOptionsDlg", "Display type", None))
        self.DisplayTypeComboBox.setItemText(0, _translate("ProcessOptionsDlg", "F", None))
        self.DisplayTypeComboBox.setItemText(1, _translate("ProcessOptionsDlg", "dF", None))
        self.DisplayTypeComboBox.setItemText(2, _translate("ProcessOptionsDlg", "dF/F0", None))
        self.referenceFramesLabel.setText(_translate("ProcessOptionsDlg", "Number of F0 reference frames", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.FrameOptionsTab), _translate("ProcessOptionsDlg", "Frame options", None))
        self.label_3.setText(_translate("ProcessOptionsDlg", "Time 0 frame", None))
        self.associatedTimesRadioButton.setText(_translate("ProcessOptionsDlg", "Use associated times", None))
        self.userInterframeRadioButton.setText(_translate("ProcessOptionsDlg", "Specify interframe time interval (ms)", None))
        self.FrameBasedRadioButton.setText(_translate("ProcessOptionsDlg", "Do not use times", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.timeOptionsTab), _translate("ProcessOptionsDlg", "Time options", None))
        self.LUTradioButton.setText(_translate("ProcessOptionsDlg", "Look up table", None))
        self.ColorMapcomboBox.setItemText(0, _translate("ProcessOptionsDlg", "Jet", None))
        self.ColorMapcomboBox.setItemText(1, _translate("ProcessOptionsDlg", "Winter", None))
        self.ColorMapcomboBox.setItemText(2, _translate("ProcessOptionsDlg", "...", None))
        self.HSVradioButton.setText(_translate("ProcessOptionsDlg", "HSV", None))
        self.medianFilterCheckbox.setText(_translate("ProcessOptionsDlg", "Median filter", None))
        self.gaussianFilterCheckbox.setText(_translate("ProcessOptionsDlg", "Gaussian filter", None))
        self.chooseBackgroundButton.setText(_translate("ProcessOptionsDlg", "Choose HSV Background", None))
        self.saturationLabel.setText(_translate("ProcessOptionsDlg", "Saturation", None))
        self.HSVbackGroupBox.setTitle(_translate("ProcessOptionsDlg", "HSV background", None))
        self.FrameByFrameRadioButton.setText(_translate("ProcessOptionsDlg", "Frame by frame", None))
        self.NomarskiRadioButton.setText(_translate("ProcessOptionsDlg", "Nomarski", None))
        self.enlargeToBckCheckBox.setText(_translate("ProcessOptionsDlg", "Enlarge to background", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.displayOptionsTab), _translate("ProcessOptionsDlg", "Display options", None))
        self.displayTimesCheckBox.setText(_translate("ProcessOptionsDlg", "Display time stamp on the video", None))
        self.fontSizeLabel.setText(_translate("ProcessOptionsDlg", "Font Size", None))
        self.xOffsetLabel.setText(_translate("ProcessOptionsDlg", "X offset", None))
        self.yOffsetLabel.setText(_translate("ProcessOptionsDlg", "Y offset", None))
        self.scalebarCheckBox.setText(_translate("ProcessOptionsDlg", "Display scalebar on the video", None))
        self.label_2.setText(_translate("ProcessOptionsDlg", "Scale Factor (um/pixel)", None))
        self.label_4.setText(_translate("ProcessOptionsDlg", "Length (um)", None))
        self.label_5.setText(_translate("ProcessOptionsDlg", "Line Size", None))
        self.fontSizeLabel_2.setText(_translate("ProcessOptionsDlg", "Font Size", None))
        self.xOffsetLabel_2.setText(_translate("ProcessOptionsDlg", "X offset", None))
        self.yOffsetLabel_2.setText(_translate("ProcessOptionsDlg", "Y offset", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.tab), _translate("ProcessOptionsDlg", "Tags", None))
        self.PO_TabWidget.setTabText(self.PO_TabWidget.indexOf(self.FiltersTab), _translate("ProcessOptionsDlg", "Filters", None))

