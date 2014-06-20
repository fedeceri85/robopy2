import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
from RoboPyGui import Ui_RoboMainWnd
from RawSequenceOptionsGui import Ui_Dialog
from SequenceDisplay import SequenceDisplay
from IPython.frontend.terminal.embed import InteractiveShellEmbed
import cPickle
from OpenGL.GLUT import *

'''
Main window of Robopy project
Launches various windows and tools

'''
class RawSequenceOptions(Ui_Dialog,PyQt4.QtGui.QDialog):
	def __init__(self,parent=None,cropL=None):
		PyQt4.QtGui.QDialog.__init__(self,parent)
		self.setupUi(self)
		self.connect(self.LCcheckBox,SIGNAL("stateChanged(int)"),self.LCstateChanged)
		self.connect(self.cropCheckBox,SIGNAL("stateChanged(int)"),self.cropStateChanged)
		if cropL is not None:
			self.cropCheckBox.setChecked(True)
			self.leftCropSpinBox.setValue(cropL[0])
			self.rightCropSpinBox.setValue(cropL[1])
			self.topCropSpinBox.setValue(cropL[2])
			self.bottomCropSpinBox.setValue(cropL[3])

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
		self.filesList = list()
		self.options = None
		
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
		self.connect(self.actionLoad_Sequentially, SIGNAL("triggered()"), self.roboActionLoadSequentially)
		self.connect(self.actionOpen_Next, SIGNAL("triggered()"), self.RoboActionOpen_Next)

		
	def makeImageOptionsConnections(self, seqDisp, procOpt):
		seqDisp.ImageTabWidget.currentChanged.connect(procOpt.sequenceChangedTab)
		
	def roboActionOpenCb(self):
		self.initSaveFolders()

		files = self.getFileNamesGui("Select sequence", QString(self.lastDirectory), "Tiff images (*.tif);; HDF5 images (*.h5 *.hf5) ")
		try:
			f=open(files[0]+'_cropInfo','r')
			try:
				cropL = cPickle.load(f)
			except:
				cropL = None
			f.close()
		except:
			cropL = None
		optDlg = RawSequenceOptions(parent=self,cropL=cropL)

		if optDlg.exec_():
			self.options = optDlg.getValues()
		if 	self.options['crop']:
			cropL = [self.options['leftMargin'], self.options['rightMargin'] ,self.options['topMargin'],self.options['bottomMargin']]
			f=open(files[0]+'_cropInfo','w')
			cPickle.dump(cropL,f)
			f.close()
		sd = SequenceDisplay(self, files,rawTiffOptions=self.options)
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
		
		if optDlg.exec_():
			self.options = optDlg.getValues()
		
		sd = SequenceDisplay(self, files,loadInRam = True,rawTiffOptions=self.options)
		#self.sequences.append(sd)
		self.seqDispList.append(sd)
		self.showStatusMessage("Ready!" + " sequences " + str(len(self.sequences)))
		with open (self.lastDirFile,'w') as myfile:
			myfile.write(os.path.split(files[0])[0])
			myfile.close()
			
			
	def roboActionLoadSequentially(self):
		self.initSaveFolders()

		files = self.getFileNamesGui("Select sequence", QString(self.lastDirectory), "Tiff images (*.tif);; HDF5 images (*.h5 *.hf5) ")
	
		with open (self.lastDirFile,'w') as myfile:
			myfile.write(os.path.split(files[0])[0])
			myfile.close()
		
		optDlg = RawSequenceOptions(parent=self)
		
		if optDlg.exec_():
			self.options = optDlg.getValues()
			
		files.sort()
		self.filesList = files
		self.fileIndex = -1
		self.RoboActionOpen_Next()

	def RoboActionOpen_Next(self):
		if self.filesList == []:
			return
		try:	
			self.seqDispList[-1].optionsDlg.close()
			self.seqDispList[-1].close()
		except:
			pass
		self.fileIndex = self.fileIndex + 1 

		self.seqDispList = []
		if self.fileIndex >= len(self.filesList):
			self.showStatusMessage("End of the list")
			self.fileIndex = len(self.fileList)-1
		else:
			sd = SequenceDisplay(self,[self.filesList[self.fileIndex],] ,rawTiffOptions=self.options)
			#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)
			self.seqDispList.append(sd)
			self.showStatusMessage("opening file "+str(self.fileIndex+1)+" of "+str(len(self.filesList)))
	
	def RoboActionOpen_Prev(self):
		if self.filesList == []:
			return
		try:	
			self.seqDispList[-1].optionsDlg.close()
			self.seqDispList[-1].close()
		except:
			pass

		self.fileIndex = self.fileIndex -1 
		self.seqDispList = []
		if self.fileIndex >= len(self.filesList) or self.fileIndex <0:
			self.showStatusMessage("End of the list")
			self.fileIndex = 0
		else:
			sd = SequenceDisplay(self,[self.filesList[self.fileIndex],] ,rawTiffOptions=self.options)
			#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)#self.sequences.append(sd)
			self.seqDispList.append(sd)
			self.showStatusMessage("opening file "+str(self.fileIndex+1)+" of "+str(len(self.filesList)))
			
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
