import sys
sys.path.append('/home/federico/Desktop/robopy')
sys.path.append('./plugins')
from SequenceProcessor import *
from ProcessOptions import Properties
import os
sys.path.append('/usr/local/lib/python2.7/site-packages/stfio/')
import stfio
import numpy as np
import pickle
from TiffSequence import TiffSequence, HDF5Sequence
from SequenceApOptions import Ui_Dialog
associatedFileType = '.cap'
import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class calciumApDialog(Ui_Dialog, QDialog):
	def __init__(self, parent=None,saveFile=None):
		QDialog.__init__(self, parent=parent)		
		self.setupUi(self)
		self.valueDict = {}	
		self.saveFile = saveFile
		fo = Properties(self)
		try:
			d=cPickle.load(open(self.saveFile,'r'))
			fo.add('timeScale', d['timeScale'], self.timeScaleSpinBox)
			fo.add('dataScale', d['dataScale'], self.dataScaleFactor)
			fo.add('xoff', d['xoff'], self.xSpinBox)
			fo.add('yoff', d['yoff'], self.ySpinBox)
			fo.add('lineWidth', d['lineWidth'], self.lwSpinBox)
			fo.add('frameSpan', d['frameSpan'], self.frameSpanSpinBox)
			
		except:	
			fo.add('timeScale', 0.05, self.timeScaleSpinBox)
			fo.add('dataScale', 3.0, self.dataScaleFactor)
			fo.add('xoff', 0, self.xSpinBox)
			fo.add('yoff', 400, self.ySpinBox)
			fo.add('lineWidth', 1, self.lwSpinBox)
			fo.add('frameSpan', 25, self.frameSpanSpinBox)
		self.options = fo
			
class calciumAPProcessor(ProcessedSequence):
	def __init__(self,tiffSequence,abfFile,time0=0,processedWidget=None,displayParameters=None,frameOptions=None,displayOptions=None,timeOptions=None):
		ProcessedSequence.__init__(self,tiffSequence,processedWidget,displayParameters,frameOptions,displayOptions,timeOptions)
		if os.path.exists(abfFile):
			self.abfFile = abfFile
		else:
			#fold = abfFile[7:]
			abfFileName = os.path.split(abfFile)[1]
			fold = os.path.split(self.tiffSequence.fileName[0])[0]
			#self.abfFile = os.path.join('/run/media/federico/',fold)
			self.abfFile = os.path.join(fold,abfFileName)
		self.times =None
		self.vTrace=None
		self.cameraExp = None
		self.cameraTrigger = None
		self.expStartingIndexes = None
		self.time0 = time0
		self.dialog = calciumApDialog(saveFile='/dev/null')
		self.loadTraces()
		self.alignTraces()
		self.createTracesList()
		self.createTracesToDisplay(self.dialog.options.frameSpan)
		self.dialog.show()
		
	def loadTraces(self):
		record = stfio.read(self.abfFile)

		time_scale_factor = 0.001
		samp_rate= 1/(record.dt*time_scale_factor)
		#time_start = 0
		#time_end =  sum([len(record[0][i]) for i in xrange(len(record[0]))])*record.dt			
		#self.times = np.arange(time_start,time_end,record.dt)*time_scale_factor
		#print self.times.size
		section_idx = xrange(len(record[0]))
		self.vTrace=np.concatenate(list(record[0][j].asarray() for j in section_idx))
		self.cameraExp=np.concatenate(list(record[1][j].asarray() for j in section_idx))
		self.cameraTrigger=np.concatenate(list(record[2][j].asarray() for j in section_idx))
		self.times = np.arange(self.vTrace.size)*record.dt*time_scale_factor

	def alignTraces(self):
		#self.decimateTraces()
		self.expStartingIndexes = np.where(np.logical_and(np.diff(self.cameraExp)>1 , (self.times[1:]>=self.time0)))[0]
		self.expStartingTimes = self.times[self.expStartingIndexes]
		print('0 time (s):'+str(self.expStartingTimes[0]))
		#startingIndex = self.expStartingIndexes[0]
		#startingIndex2 = np.where(self.cameraTrigger>1)[0]
		#if startingIndex != startingIndex2:
			#print("Warning: camera acquisition started after the first trigger.Sync on exposure instead")
		#t0 = self.times[startingIndex]
		#self.times = self.times[startingIndex:]-t0
		#self.vTrace = self.vTrace[startingIndex:]
		return (self.times[self.expStartingIndexes[0]:]-self.expStartingTimes[0],self.vTrace[self.expStartingIndexes[0]:])
	
	
	def createTracesList(self):
		self.tracesList = []
		for i in xrange(len(self.expStartingIndexes)-1):
			self.tracesList.append(self.vTrace[self.expStartingIndexes[i]:self.expStartingIndexes[i+1]])
			

		
	def decimateTraces(self):
		self.vTrace = self.vTrace[::500]
		self.times = self.times[::500]
		self.cameraExp = self.cameraExp[::500]
		self.cameraTrigger = self.cameraTrigger[::500]
		
		
	def createTracesToDisplay(self,nFramesSpan=25):
		self.displayTracesList = []
		for i in xrange(0,len(self.tracesList)):
			self.displayTracesList.append(np.concatenate(list(np.array(self.tracesList[j]-self.tracesList[0][0]) for j in xrange(int(np.floor(i/nFramesSpan))*nFramesSpan,i+1))))
		

			
	def applyColormap(self,f,w,h):
		tex = ProcessedSequence.applyColormap(self,f,w,h)
		
		self.drawTrace()
		return tex
	
	def HSVImage(self,f,w,h):
		tex = ProcessedSequence.HSVImage(self,f,w,h)
		self.drawTrace()
		return tex
		
	def saveRoisToFile(self,filename):

		ProcessedSequence.saveRoisToFile(self,filename)
		data = np.vstack((self.times[self.expStartingIndexes[0]:],self.vTrace[self.expStartingIndexes[0]:]))
		f=os.path.splitext(filename)[0]

		np.save(f+'.ap',data)
		
	def drawTrace(self):
		x = np.arange(len(self.displayTracesList[self.currentProcessedFrame]))*self.dialog.options.timeScale
		y = self.displayTracesList[self.currentProcessedFrame]/self.dialog.options.dataScale
		data = np.empty(x.size+y.size)
		data[::2] = x
		data[1::2] = y
		self.processedWidget.drawTraces(data, y.size,self.dialog.options.xoff,self.dialog.options.yoff,lineWidth=self.dialog.options.lineWidth)



def load(sd):
	pass

def run(sd):
	db = pickle.load(open(sd.tiffFiles[0],'r'))
	tiffFiles = db['tiffFiles']
	abfFile = db['abfFile']
	try:
		time0 = db['time0']
	except KeyError:
		time0=0
	folder = os.path.split(sd.tiffFiles[0])[0]
	ext = os.path.splitext(tiffFiles[0])[1]
	tiffFilesOut=[]
	for f in tiffFiles:
		tiffFilesOut.append(os.path.join(folder,f))
	
	if ext == '.tif' or ext=='.tiff' or ext =='.TIF' or ext == '.TIFF':
		sd.tiffSequence = TiffSequence(tiffFilesOut,sd.rawTiffOptions)

	if ext == '.h5' or ext == 'h5f' or ext == '.H5' or ext == '.H5F':
		sd.tiffSequence = HDF5Sequence(tiffFilesOut,sd.rawTiffOptions)
		
	sd.processedSequence = calciumAPProcessor(sd.tiffSequence,abfFile,time0,sd.processedWidget,sd.displayParameters,sd.optionsDlg.frameOptions,
						sd.optionsDlg.displayOptions,sd.optionsDlg.timeOptions)