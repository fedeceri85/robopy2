import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
from RoboPyGui import Ui_RoboMainWnd
from RawSequenceOptionsGui import Ui_Dialog
from SequenceDisplay import SequenceDisplay
from IPython.frontend.terminal.embed import InteractiveShellEmbed

from OpenGL.GLUT import *

'''
Main window of Robopy project
Launches various windows and tools

'''
class RawSequenceOptions(Ui_Dialog,PyQt4.QtGui.QDialog):
	def __init__(self,parent=None):
		PyQt4.QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.connect(self.LCcheckBox,SIGNAL("stateChanged(int)"),self.LCstateChanged)
		self.connect(self.cropCheckBox,SIGNAL("stateChanged(int)"),self.cropStateChanged)
		
		self.show()
	
	def LCstateChanged(self):
		if self.LCcheckBox.isChecked():
			self.label_2.setEnabled(True)
			self.label_3.setEnabled(True)
			self.leftLCSpinBox.setEnabled(True)
			self.rightLCSpinBox.setEnabled(True)
		else:
			self.label_2.setEnabled(False)
			self.label_3.setEnabled(False)
			self.leftLCSpinBox.setEnabled(False)
			self.rightLCSpinBox.setEnabled(False)
	
	def cropStateChanged(self):
		if self.cropCheckBox.isChecked():
			self.label_4.setEnabled(True)
			self.label_5.setEnabled(True)
			self.label_6.setEnabled(True)
			self.label_7.setEnabled(True)
			self.leftCropSpinBox.setEnabled(True)
			self.rightCropSpinBox.setEnabled(True)
			self.topCropSpinBox.setEnabled(True)
			self.bottomCropSpinBox.setEnabled(True)
		else:
			self.label_4.setEnabled(False)
			self.label_5.setEnabled(False)
			self.label_6.setEnabled(False)
			self.label_7.setEnabled(False)
			self.leftCropSpinBox.setEnabled(False)
			self.rightCropSpinBox.setEnabled(False)
			self.topCropSpinBox.setEnabled(False)
			self.bottomCropSpinBox.setEnabled(False)
			
	def getValues(self):
		options = {}
		rebin = int(str(self.rebinComboBox.currentText()))
		if rebin == 1:
			options['rebin'] = None
		else:
			options['rebin'] = int(rebin)
		

		if self.LCcheckBox.isChecked():
			options['LineCorrection'] = True
			options['RightLC'] = self.rightLCSpinBox.value()
			options['LeftLC'] = self.rightLCSpinBox.value()
		else:
			options['LineCorrection'] = False
			options['RightLC'] = 0
			options['LeftLC'] = 0
		options['leftMargin'] = self.leftCropSpinBox.value()
		options['rightMargin'] = self.rightCropSpinBox.value()
		options['topMargin'] = self.topCropSpinBox.value()
		options['bottomMargin'] = self.bottomCropSpinBox.value()
		if self.cropCheckBox.isChecked():
			options['crop'] = True
			options['leftMargin'] = self.leftCropSpinBox.value()
			options['rightMargin'] = self.rightCropSpinBox.value()
			options['topMargin'] = self.topCropSpinBox.value()
			options['bottomMargin'] = self.bottomCropSpinBox.value()
		else:
			options['crop'] = False
			options['leftMargin'] = None
			options['rightMargin'] = None
			options['topMargin'] = None
			options['bottomMargin'] = None
			
		return options
	
class RoboPy(Ui_RoboMainWnd, PyQt4.QtGui.QMainWindow):
	def __init__(self, parent = None):
		PyQt4.QtGui.QMainWindow.__init__(self, parent=parent)
		
		self.setupUi(self)

		
		self.initData()
		self.makeConnections()
		self.seqDispList=[]
		self.show()
		
	def initData(self):
		self.sequences = list();
		
	def initSaveFolders(self):
		self.optDir = os.path.join(os.path.expanduser('~'),'.robopy')
		print self.optDir
		if not os.path.isdir(self.optDir):
			os.mkdir(self.optDir)
		self.lastDirFile = os.path.join(self.optDir,'lastDir')
		if os.path.isfile(self.lastDirFile):
			with open (self.lastDirFile,'r') as myfile:
				self.lastDirectory=myfile.read()
				myfile.close()
		else:
			self.lastDirectory = "";
		
	def makeConnections(self):
		self.connect(self.roboActionOpen, SIGNAL("triggered()"), self.roboActionOpenCb)
		self.connect(self.roboActionLoadInRam, SIGNAL("triggered()"), self.roboActionLoadInRamCb)
		
	def makeImageOptionsConnections(self, seqDisp, procOpt):
		seqDisp.ImageTabWidget.currentChanged.connect(procOpt.sequenceChangedTab)
		
	def roboActionOpenCb(self):
		self.initSaveFolders()

		files = self.getFileNamesGui("Select sequence", QString(self.lastDirectory), "Tiff images (*.tif);; HDF5 images (*.h5 *.hf5) ")
		optDlg = RawSequenceOptions(parent=self)
		options = None
		if optDlg.exec_():
			options = optDlg.getValues()
			print(options)
		sd = SequenceDisplay(self, files,rawTiffOptions=options)
		#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)
		self.seqDispList.append(sd)
		self.showStatusMessage("Ready!" + " sequences " + str(len(self.sequences)))
		with open (self.lastDirFile,'w') as myfile:
			myfile.write(os.path.split(files[0])[0])
			myfile.close()
		
		
	def roboActionLoadInRamCb(self):
		self.initSaveFolders()
		files = self.getFileNamesGui("Select sequence", QString(self.lastDirectory), "Tiff images (*.tif);; HDF5 images (*.h5 *.hf5) ")
		optDlg = RawSequenceOptions(parent=self)
		options = None
		if optDlg.exec_():
			options = optDlg.getValues()
			print(options)
		
		sd = SequenceDisplay(self, files,loadInRam = True,rawTiffOptions=options)
		#self.sequences.append(sd)
		self.seqDispList.append(sd)
		self.showStatusMessage("Ready!" + " sequences " + str(len(self.sequences)))
		
	def showStatusMessage(self, msg):
		self.statusBar().showMessage(msg)
		
	def getFileNamesGui(self, caption, directory, filt):
		fnames = QFileDialog.getOpenFileNames(self, caption, directory, filt)
		
		nFiles = fnames.count()
		
		files = [fnames[i].toAscii().data() for i in xrange(nFiles)]
			
		return files

if __name__== "__main__":
	
	glutInit(sys.argv)
	
	app = PyQt4.QtGui.QApplication(sys.argv)
	robopy = RoboPy()
	robopy.show()

	#ipshell = InteractiveShellEmbed()
	#ipshell()
	
	ans = app.exec_()

	sys.exit(ans)
