'''
Module that holds display sequence parameters as min max auto
'''

class DisplayPamrameters:
	def __init__(self):
		self.initColorRangeParam()
		self.initRoiRelatedParams()
		
		self.falseColorRefFrame = None
		self.HSVvalue = None
		#self.HSVsaturation = None
		
	def initColorRangeParam(self):
		self.displayGrayMin = 0
		self.displayGrayMax = 16383
		self.displayColorMin = 0.0
		self.displayColorMax = 16383.0
		self.displayColorSteps = 1000
		self.autoAdjust = True
		
	def initRoiRelatedParams(self):
		self.roiProfile = None
		self.roiAverageRecomputeNeeded = True
		
