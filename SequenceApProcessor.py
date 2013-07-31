from SequenceProcessor import *
import stfio

class calciumAPProcessor(ProcessedSequence):
	def __init__(self,tiffSequence,abfFile,processedWidget,displayParameters,frameOptions,displayOptions,timeOptions):
		ProcessedSequence.__init__(tiffSequence,processedWidget,displayParameters,frameOptions,displayOptions,timeOptions)
		self.abfFile = abfFile
		self.times =None
		self.vTrace=None
		self.cameraExp = None
		self.cameraTrigger = None
	
	def loadTraces(self):
		record = stfio.read(self.abfFile)
		