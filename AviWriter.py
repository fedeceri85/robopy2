from cv2 import cv, VideoWriter,cvtColor
from numpy import zeros,loadtxt,array,uint16,argwhere
import numpy as np



class AviWriter:
	def __init__(self, fName, size=None, fps=25, isColor = True, fourcc = cv.CV_FOURCC(*'MJPG')):#('X','V', 'I', 'D')):
		
		self.fileName = fName
		self.width = -1
		self.height = -1
		self.frames = 0
		self.fps = fps
		self.aviHandler = None
		self.fourcc = fourcc
		self.isColor = isColor
		self.size = size
		
		
	def __del__(self):
		self.clearAviHandler()
	
	def clearAviHandler(self):
		if self.aviHandler != None:
			self.aviHandler.release()
			self.aviHandler = None
		
	
	def getFileName(self):
		return self.fileName
		
	def getWidth(self):
		return self.width
		
	def getHeight(self):
		return self.height
		
	def getFrames(self):
		return self.frames
		
	def open(self, w, h):
		self.clearAviHandler()
		print(self.fileName)
		print(self.fourcc)
		print(self.fps)
		print(self.size)
		print(self.isColor)
		self.aviHandler = VideoWriter(self.fileName, self.fourcc, self.fps, (w,h), self.isColor)
		
	def addFrame(self, data):
		h,w,z = data.shape
		
		if self.aviHandler == None:
			self.open(w,h)
			
		if not self.aviHandler.isOpened():
			print("AviWriter file is not opened, cannot save!")
			return
		data = cvtColor(data, cv.CV_RGB2BGR)
		self.aviHandler.write(data)
		
	
		
	
