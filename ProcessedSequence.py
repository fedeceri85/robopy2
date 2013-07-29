import SequenceProcessor


class ProcessedSequence:
	def __init__(self,tiffSequence,processedWidget,displayParameters):
		self.tiffSequence = tiffSequence
		self.processedWidget = processedWidget
		self.falseColorRefFrame = None
		self.HSVvalue = None
		self.displayParameters = displayParameters
	
	def computeProcessedFrameGLSL(self,n,frameOptions,displayOptions,returnType="float"):
		return SequenceProcessor.computeProcessedFrameGLSL(self.processedWidget, self.tiffSequence, n, frameOptions,displayOptions, self.falseColorRefFrame,returnType=returnType)
		
	
	def computeReference(self,frameOptions):
		self.falseColorRefFrame = SequenceProcessor.computeReference(self.tiffSequence, frameOptions)
		#return self.falseColorRefFrame
	
	def computeValue(self,ValueFrame):
		self.HSVvalue = SequenceProcessor.computeValue(ValueFrame,(self.tiffSequence.height,self.tiffSequence.width))
		#return self.HSVvalue
	
	def applyColormapGLSL(self,f,w,h):
		return SequenceProcessor.applyColormapGLSL(self.processedWidget, f, w, h,self.displayParameters.displayColorMin,self.displayParameters.displayColorMax)
		
	def HSVImageGLSL(self,f,w,h):
		return SequenceProcessor.HSVImageGLSL(self.processedWidget, f,self.HSVvalue, w, h, self.displayParameters.displayColorMin, self.displayParameters.displayColorMax)
					