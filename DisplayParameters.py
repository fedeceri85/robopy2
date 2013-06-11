'''
Module that holds display sequence parameters as min max auto
'''
import numpy as np
import matplotlib

class DisplayPamrameters:
	def __init__(self):
		self.initColorRangeParam()
		self.initRoiRelatedParams()
		
		self.falseColorRefFrame = None
		self.HSVvalue = None
		#self.HSVsaturation = None
		self.initHSVColormap()
		
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
		
	def initHSVColormap(self):
		
		[ph,pv] = np.meshgrid(range(256), range(256), dtype=np.float)
		ps = np.ones((256, 256), dtype = np.float)
		hsvM = np.zeros((256,256,3), dtype = np.float)
		hsvM[:,:,0] = ph / 255.0
		hsvM[:,:,1] = ps
		hsvM[:,:,2] = pv / 255.0
		
		self.HSVmap = matplotlib.colors.hsv_to_rgb(hsvM)
		self.HSVmap = (self.HSVmap * 255.0).astype(np.uint32)
		self.HSVmap = (255 << 24 | self.HSVmap[:,:,0] << 16 | self.HSVmap[:,:,1] << 8 | self.HSVmap[:,:,2]).flatten() 
		self.HSVmap = self.HSVmap.astype(np.uint32)
		
		
