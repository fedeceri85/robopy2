# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SequenceDisplayGui.ui'
#
# Created: Mon Mar  3 18:43:28 2014
#      by: PyQt4 UI code generator 4.10.3
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
        SequenceDisplayWnd.resize(628, 480)
        self.centralwidget = QtGui.QWidget(SequenceDisplayWnd)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.colorMaxSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.colorMaxSpinBox.setDecimals(4)
        self.colorMaxSpinBox.setObjectName(_fromUtf8("colorMaxSpinBox"))
        self.verticalLayout_2.addWidget(self.colorMaxSpinBox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.colorMinSlider = QtGui.QSlider(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.colorMinSlider.sizePolicy().hasHeightForWidth())
        self.colorMinSlider.setSizePolicy(sizePolicy)
        self.colorMinSlider.setOrientation(QtCore.Qt.Vertical)
        self.colorMinSlider.setObjectName(_fromUtf8("colorMinSlider"))
        self.horizontalLayout_2.addWidget(self.colorMinSlider)
        self.colorMaxSlider = QtGui.QSlider(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.colorMaxSlider.sizePolicy().hasHeightForWidth())
        self.colorMaxSlider.setSizePolicy(sizePolicy)
        self.colorMaxSlider.setOrientation(QtCore.Qt.Vertical)
        self.colorMaxSlider.setObjectName(_fromUtf8("colorMaxSlider"))
        self.horizontalLayout_2.addWidget(self.colorMaxSlider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.colorMinSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.colorMinSpinBox.setDecimals(4)
        self.colorMinSpinBox.setObjectName(_fromUtf8("colorMinSpinBox"))
        self.verticalLayout_2.addWidget(self.colorMinSpinBox)
        self.colorAutoRadioButton = QtGui.QRadioButton(self.centralwidget)
        self.colorAutoRadioButton.setObjectName(_fromUtf8("colorAutoRadioButton"))
        self.verticalLayout_2.addWidget(self.colorAutoRadioButton)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.ImageTabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.ImageTabWidget.sizePolicy().hasHeightForWidth())
        self.ImageTabWidget.setSizePolicy(sizePolicy)
        self.ImageTabWidget.setObjectName(_fromUtf8("ImageTabWidget"))
        self.RawTab = QtGui.QWidget()
        self.RawTab.setObjectName(_fromUtf8("RawTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.RawTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.ImageFrameWidget = QtGui.QWidget(self.RawTab)
        self.ImageFrameWidget.setObjectName(_fromUtf8("ImageFrameWidget"))
        self.verticalLayout_3.addWidget(self.ImageFrameWidget)
        self.ImageTabWidget.addTab(self.RawTab, _fromUtf8(""))
        self.ProcessedTab = QtGui.QWidget()
        self.ProcessedTab.setObjectName(_fromUtf8("ProcessedTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.ProcessedTab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ProcessedFrameWidget = QtGui.QWidget(self.ProcessedTab)
        self.ProcessedFrameWidget.setObjectName(_fromUtf8("ProcessedFrameWidget"))
        self.verticalLayout.addWidget(self.ProcessedFrameWidget)
        self.ImageTabWidget.addTab(self.ProcessedTab, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.ImageTabWidget)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
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
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        SequenceDisplayWnd.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SequenceDisplayWnd)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 17))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuRois = QtGui.QMenu(self.menubar)
        self.menuRois.setObjectName(_fromUtf8("menuRois"))
        self.menuStacks = QtGui.QMenu(self.menubar)
        self.menuStacks.setObjectName(_fromUtf8("menuStacks"))
        self.menuMath_2 = QtGui.QMenu(self.menuStacks)
        self.menuMath_2.setObjectName(_fromUtf8("menuMath_2"))
        self.menuDisplay = QtGui.QMenu(self.menubar)
        self.menuDisplay.setObjectName(_fromUtf8("menuDisplay"))
        self.menuFilters = QtGui.QMenu(self.menuDisplay)
        self.menuFilters.setObjectName(_fromUtf8("menuFilters"))
        self.menuOutput = QtGui.QMenu(self.menubar)
        self.menuOutput.setObjectName(_fromUtf8("menuOutput"))
        SequenceDisplayWnd.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SequenceDisplayWnd)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SequenceDisplayWnd.setStatusBar(self.statusbar)
        self.actionCompute_Rois = QtGui.QAction(SequenceDisplayWnd)
        self.actionCompute_Rois.setObjectName(_fromUtf8("actionCompute_Rois"))
        self.actionLoad_from_file = QtGui.QAction(SequenceDisplayWnd)
        self.actionLoad_from_file.setObjectName(_fromUtf8("actionLoad_from_file"))
        self.actionSave_to_file = QtGui.QAction(SequenceDisplayWnd)
        self.actionSave_to_file.setObjectName(_fromUtf8("actionSave_to_file"))
        self.actionDelete_Last = QtGui.QAction(SequenceDisplayWnd)
        self.actionDelete_Last.setObjectName(_fromUtf8("actionDelete_Last"))
        self.actionBack_Projection = QtGui.QAction(SequenceDisplayWnd)
        self.actionBack_Projection.setObjectName(_fromUtf8("actionBack_Projection"))
        self.actionAverage = QtGui.QAction(SequenceDisplayWnd)
        self.actionAverage.setObjectName(_fromUtf8("actionAverage"))
        self.actionAdd = QtGui.QAction(SequenceDisplayWnd)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.actionSubtract = QtGui.QAction(SequenceDisplayWnd)
        self.actionSubtract.setObjectName(_fromUtf8("actionSubtract"))
        self.actionDivide = QtGui.QAction(SequenceDisplayWnd)
        self.actionDivide.setObjectName(_fromUtf8("actionDivide"))
        self.actionMultiply = QtGui.QAction(SequenceDisplayWnd)
        self.actionMultiply.setObjectName(_fromUtf8("actionMultiply"))
        self.actionAdd_image = QtGui.QAction(SequenceDisplayWnd)
        self.actionAdd_image.setObjectName(_fromUtf8("actionAdd_image"))
        self.actionSubtract_image = QtGui.QAction(SequenceDisplayWnd)
        self.actionSubtract_image.setObjectName(_fromUtf8("actionSubtract_image"))
        self.actionDivide_by_image = QtGui.QAction(SequenceDisplayWnd)
        self.actionDivide_by_image.setObjectName(_fromUtf8("actionDivide_by_image"))
        self.actionMultiply_by_image = QtGui.QAction(SequenceDisplayWnd)
        self.actionMultiply_by_image.setObjectName(_fromUtf8("actionMultiply_by_image"))
        self.actionMedian_filter = QtGui.QAction(SequenceDisplayWnd)
        self.actionMedian_filter.setObjectName(_fromUtf8("actionMedian_filter"))
        self.actionGaussian_filter = QtGui.QAction(SequenceDisplayWnd)
        self.actionGaussian_filter.setObjectName(_fromUtf8("actionGaussian_filter"))
        self.actionTemporal_Smoothing = QtGui.QAction(SequenceDisplayWnd)
        self.actionTemporal_Smoothing.setObjectName(_fromUtf8("actionTemporal_Smoothing"))
        self.actionSave_raw_sequence = QtGui.QAction(SequenceDisplayWnd)
        self.actionSave_raw_sequence.setObjectName(_fromUtf8("actionSave_raw_sequence"))
        self.actionSave_traces = QtGui.QAction(SequenceDisplayWnd)
        self.actionSave_traces.setObjectName(_fromUtf8("actionSave_traces"))
        self.actionSave_as_avi = QtGui.QAction(SequenceDisplayWnd)
        self.actionSave_as_avi.setObjectName(_fromUtf8("actionSave_as_avi"))
        self.actionForce_recomputation = QtGui.QAction(SequenceDisplayWnd)
        self.actionForce_recomputation.setObjectName(_fromUtf8("actionForce_recomputation"))
        self.actionSave_as_hd5_table = QtGui.QAction(SequenceDisplayWnd)
        self.actionSave_as_hd5_table.setObjectName(_fromUtf8("actionSave_as_hd5_table"))
        self.menuRois.addAction(self.actionCompute_Rois)
        self.menuRois.addSeparator()
        self.menuRois.addAction(self.actionLoad_from_file)
        self.menuRois.addAction(self.actionSave_to_file)
        self.menuRois.addAction(self.actionSave_traces)
        self.menuRois.addSeparator()
        self.menuRois.addAction(self.actionDelete_Last)
        self.menuRois.addSeparator()
        self.menuRois.addAction(self.actionForce_recomputation)
        self.menuMath_2.addAction(self.actionAdd)
        self.menuMath_2.addAction(self.actionSubtract)
        self.menuMath_2.addAction(self.actionDivide)
        self.menuMath_2.addAction(self.actionMultiply)
        self.menuMath_2.addSeparator()
        self.menuMath_2.addAction(self.actionAdd_image)
        self.menuMath_2.addAction(self.actionSubtract_image)
        self.menuMath_2.addAction(self.actionDivide_by_image)
        self.menuMath_2.addAction(self.actionMultiply_by_image)
        self.menuStacks.addAction(self.actionBack_Projection)
        self.menuStacks.addAction(self.actionAverage)
        self.menuStacks.addAction(self.menuMath_2.menuAction())
        self.menuFilters.addAction(self.actionMedian_filter)
        self.menuFilters.addAction(self.actionGaussian_filter)
        self.menuFilters.addSeparator()
        self.menuFilters.addAction(self.actionTemporal_Smoothing)
        self.menuDisplay.addAction(self.menuFilters.menuAction())
        self.menuOutput.addAction(self.actionSave_raw_sequence)
        self.menuOutput.addAction(self.actionSave_as_avi)
        self.menuOutput.addAction(self.actionSave_as_hd5_table)
        self.menubar.addAction(self.menuRois.menuAction())
        self.menubar.addAction(self.menuStacks.menuAction())
        self.menubar.addAction(self.menuDisplay.menuAction())
        self.menubar.addAction(self.menuOutput.menuAction())

        self.retranslateUi(SequenceDisplayWnd)
        self.ImageTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SequenceDisplayWnd)

    def retranslateUi(self, SequenceDisplayWnd):
        SequenceDisplayWnd.setWindowTitle(_translate("SequenceDisplayWnd", "SequenceDisplay", None))
        self.colorAutoRadioButton.setText(_translate("SequenceDisplayWnd", "Auto", None))
        self.ImageTabWidget.setTabText(self.ImageTabWidget.indexOf(self.RawTab), _translate("SequenceDisplayWnd", "Raw", None))
        self.ImageTabWidget.setTabText(self.ImageTabWidget.indexOf(self.ProcessedTab), _translate("SequenceDisplayWnd", "Processed", None))
        self.FirstFrameButton.setText(_translate("SequenceDisplayWnd", "<<", None))
        self.BackFrameButton.setText(_translate("SequenceDisplayWnd", "<", None))
        self.PlayButton.setText(_translate("SequenceDisplayWnd", "P", None))
        self.ForwardFrameButton.setText(_translate("SequenceDisplayWnd", ">", None))
        self.LastFrameButton.setText(_translate("SequenceDisplayWnd", ">>", None))
        self.menuRois.setTitle(_translate("SequenceDisplayWnd", "Rois", None))
        self.menuStacks.setTitle(_translate("SequenceDisplayWnd", "Stack", None))
        self.menuMath_2.setTitle(_translate("SequenceDisplayWnd", "Math", None))
        self.menuDisplay.setTitle(_translate("SequenceDisplayWnd", "Display", None))
        self.menuFilters.setTitle(_translate("SequenceDisplayWnd", "Filters", None))
        self.menuOutput.setTitle(_translate("SequenceDisplayWnd", "Output", None))
        self.actionCompute_Rois.setText(_translate("SequenceDisplayWnd", "Compute Roi", None))
        self.actionLoad_from_file.setText(_translate("SequenceDisplayWnd", "Load from file...", None))
        self.actionSave_to_file.setText(_translate("SequenceDisplayWnd", "Save to file", None))
        self.actionDelete_Last.setText(_translate("SequenceDisplayWnd", "Delete Last", None))
        self.actionBack_Projection.setText(_translate("SequenceDisplayWnd", "Back Projection", None))
        self.actionAverage.setText(_translate("SequenceDisplayWnd", "Average", None))
        self.actionAdd.setText(_translate("SequenceDisplayWnd", "Add", None))
        self.actionSubtract.setText(_translate("SequenceDisplayWnd", "Subtract", None))
        self.actionDivide.setText(_translate("SequenceDisplayWnd", "Divide", None))
        self.actionMultiply.setText(_translate("SequenceDisplayWnd", "Multiply", None))
        self.actionAdd_image.setText(_translate("SequenceDisplayWnd", "Add image", None))
        self.actionSubtract_image.setText(_translate("SequenceDisplayWnd", "Subtract image", None))
        self.actionDivide_by_image.setText(_translate("SequenceDisplayWnd", "Divide by image", None))
        self.actionMultiply_by_image.setText(_translate("SequenceDisplayWnd", "Multiply by image", None))
        self.actionMedian_filter.setText(_translate("SequenceDisplayWnd", "Median filter", None))
        self.actionGaussian_filter.setText(_translate("SequenceDisplayWnd", "Gaussian filter", None))
        self.actionTemporal_Smoothing.setText(_translate("SequenceDisplayWnd", "Temporal Smoothing", None))
        self.actionSave_raw_sequence.setText(_translate("SequenceDisplayWnd", "Save raw sequence", None))
        self.actionSave_traces.setText(_translate("SequenceDisplayWnd", "Export traces", None))
        self.actionSave_as_avi.setText(_translate("SequenceDisplayWnd", "Save as avi", None))
        self.actionForce_recomputation.setText(_translate("SequenceDisplayWnd", "Force roi recomputation", None))
        self.actionSave_as_hd5_table.setText(_translate("SequenceDisplayWnd", "Save as hd5 table", None))

