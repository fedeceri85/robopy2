from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from PyQt4.QtCore import *

from Shader import Shader
from VideoProcessor import VideoProcessor

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from Roi import Roi
import sys
import matplotlib

'''
Main Image display widget ontop of QGLWidget (to use opengl hardware)
computer running must be opengl es 2.0 capable
'''
class ImageDisplayWidget(QGLWidget):
	def __init__(self, parent=None, brother=None):
		super(ImageDisplayWidget, self).__init__(QGLFormat(QGL.SampleBuffers), parent, brother)
		
		self.textures = {'rawData':list(), 'toDraw':list(), 'texId': list(), 'texShape':list(), 
		'internalType':list(), 'dataType':list()}
		
		self.shadePrograms = list()
		self.videoBuffers = list()
		
		self.currentDrawData = {"tex":None, "width":0, "height":0}
		
		self.SequenceDisplay = parent
		
		self.setMouseTracking(True)
		
		self.ImagePositionX = 0
		self.ImagePositionY = 0
		
		self.ImageZoom = 1.0
		self.ImageZoomSteps = 1
		
		self.IsMouseDown = 0
		self.RightMouseButtonClicked = 0
		self.DrawRoiStatus = "idle"
		self.rois = list()
		
	def close(self):
		self.makeCurrent()
		n = len(self.textures['texId'])
		for i in range(0,n):
			glDeleteTextures(self.textures['texId'][i])
			
		self.textures = list()
			
		for i in range(0, len(self.shadePrograms)):
			self.shadePrograms[i].removeAllShaders()
			
		self.shadePrograms = list()
		
		self.doneCurrent()
	
	def initializeGL(self):
		glClearColor(0.2, 0.2, 0.2, 0.0)
		glClearAccum(0.0, 0.0, 0.0, 0.0)
		glShadeModel(GL_SMOOTH)
		
		glEnable(GL_LINE_SMOOTH)
		glLineWidth(2.0)
		
		glEnable(GL_TEXTURE_RECTANGLE)
		
		
		glTexParameterf(GL_TEXTURE_RECTANGLE, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_RECTANGLE, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
		glTexParameterf(GL_TEXTURE_RECTANGLE, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
		
	def createShaders(self):
		self.makeCurrent()
		sh = Shader()
		
		nSh = len(sh.shaderCodes)
		for i in range(0,nSh):
			prg = QGLShaderProgram(self.context())
			prg.addShaderFromSourceCode(QGLShader.Fragment, sh.shaderCodes[i])
			prg.link()
			
			self.shadePrograms.append(prg)
		
		self.doneCurrent()
		
	def createOfflineBuffers(self, w, h):
		if len(self.videoBuffers) < 2 or self.videoBuffers[0].size().width() != w or self.videoBuffers[0].size().height() != h:
			self.videoBuffers = list()
			self.videoBuffers.append(VideoProcessor(w,h, self.context()))
			self.videoBuffers.append(VideoProcessor(w,h, self.context()))
			self.videoBuffers.append(VideoProcessor(w,h, self.context(), GL_RGBA8))
		
	def resizeGL(self, w, h):
		
		#print("Resizing with "  + str(w) + "," + str(h))
		
		if w==0 or h==0:
			return
			
		glViewport(0,0,w,h)
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		
		glOrtho(0, w, h, 0, -1, 1)
		
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
	def selectRawTexture(self):
		self.currentDrawData = {"tex":None, "width":0, "height":0}
		
		for i in range(len(self.textures['texId'])):
			isDrawing = self.textures['toDraw'][i]
			
			if isDrawing:
				tex = self.textures['texId'][i]
				h,w = self.textures['texShape'][i]
				self.currentDrawData["tex"] = tex
				self.currentDrawData["width"] = w
				self.currentDrawData["height"] = h
		
	def paintGL(self):
		
		
		glClear(GL_COLOR_BUFFER_BIT or GL_DEPTH_BUFFER_BIT)
		
		
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		glColor3f(1.0, 1.0, 1.0)
		
		glActiveTexture(GL_TEXTURE0)
		
		
		if self.currentDrawData["tex"] != None:
		
			glBindTexture(GL_TEXTURE_RECTANGLE, self.currentDrawData["tex"])
			w = self.currentDrawData["width"]
			h = self.currentDrawData["height"]
			
			glScalef(self.ImageZoom, self.ImageZoom, 1.0)
				
			glBegin(GL_QUADS)
			glTexCoord2d(0,0)
			glVertex2d(0,0)
				
			glTexCoord2d(w,0)
			glVertex2d(w,0)
				
			glTexCoord2d(w,h)
			glVertex2d(w,h)
				
			glTexCoord(0,h)
			glVertex2d(0,h)
				
			glEnd()
				
			
		glBindTexture(GL_TEXTURE_RECTANGLE, 0)
		
		if len(self.rois) > 0:
			for i in self.rois:
				self.drawRoi(i)
		
	def drawRoi(self, r):
		
		glColor3f(r.color.redF(), r.color.greenF(), r.color.blueF())
		
		
		nPoints = r.size()
		glBegin(GL_LINE_LOOP)
		for i in range(0,nPoints):
			glVertex2f(r.point(i).x(), r.point(i).y())
			
		glEnd()

		if r.mapSize > 0:
			x,y = r.computeMassCenter()
			glPushMatrix()
			
			fontWidth = glutStrokeWidth(GLUT_STROKE_ROMAN, ord('O'))
			fontScale = 12.0/fontWidth
			glTranslatef(x, y, 1.0)
			glScalef(fontScale, -fontScale, 1.0)
			#glTranslatef(- fontWidth /2.0, - glutStrokeHeight(GLUT_STROKE_ROMAN)/2.0, 1.0)
			
			glutStrokeString(GLUT_STROKE_ROMAN, str(r.ordinal + 1))
			glPopMatrix()
			
		
	def arrayToTexture(self, data, w, h, nOrd, internalType = GL_LUMINANCE, 
		dataType = GL_UNSIGNED_SHORT ):
		
		self.makeCurrent()
		tex = 0
		
		err = glGetError()
		
		nTex = len(self.textures['texId'])
		outOrd = nOrd
		
		ts = self.textures
		
		isSafeSubLoad = False
		
		if nOrd < nTex and ts['texShape'][nOrd][0] == h and ts['texShape'][nOrd][1] == w and ts['internalType'][nOrd] == internalType and ts['dataType'][nOrd] == dataType:
			tex = ts['texId'][nOrd]
			isSafeSubLoad = True
		else:
			if nOrd < nTex:
				tex = ts['texId'][nOrd]
				
				self.textures['texShape'][nOrd] = (h,w)
				self.textures['rawData'][nOrd] = data
				self.textures['internalType'][nOrd] = internalType
				self.textures['dataType'][nOrd] = dataType
			else:
				outOrd = nTex
				tex = glGenTextures(1)
				self.textures['texId'].append(tex)
				self.textures['texShape'].append((h,w))
				self.textures['rawData'].append(data)
				self.textures['toDraw'].append(False)
				self.textures['internalType'].append(internalType)
				self.textures['dataType'].append(dataType)
				
			
		
		
		glBindTexture(GL_TEXTURE_RECTANGLE, tex)
		self.checkGLError("glBindTexture - GL_TEXTURE_RECTANGLE")
		
		
		glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
		
		if isSafeSubLoad:
			glTexSubImage2D(GL_TEXTURE_RECTANGLE, 0, 0, 0, w, h, internalType, dataType, data)
		else:
			if dataType == GL_UNSIGNED_SHORT:
				vType = GL_LUMINANCE16
			else:
				vType = GL_RGB32F #GL_LUMINANCE_FLOAT32_ATI
			glTexImage2D(GL_TEXTURE_RECTANGLE, 0, vType, w, h, 0, internalType, dataType, data)
			
		
		glBindTexture(GL_TEXTURE_RECTANGLE, 0)
		self.checkGLError("glBindTexture - GL_TEXTURE_RECTANGLE")
		
		self.doneCurrent()
		
		return outOrd
		
	def buffersToVideo(self, buffers, bufferTypes = None):	
		nBuf = len(buffers)
		if nBuf < 1:
			return False
			
		h,w = buffers[0].shape
		for i in range(1, nBuf):
			nh, nw = buffers[i].shape
			if nh != h or nw != w:
				print("Buffer dimension inconsistency! Old size " + str(w) + "," + str(h) + ", new size " + str(nw) + "," + str(nh))
				return False
				
		self.createOfflineBuffers(w,h)
		
		for i in range(0, nBuf):
			biType = GL_LUMINANCE
			bdType = GL_UNSIGNED_SHORT
			
			if bufferTypes != None:
				if bufferTypes[i] == "float":
					bdType = GL_FLOAT
			
			self.arrayToTexture(buffers[i], w, h, i, biType, bdType)
			
		return True
			
	def processData(self, buffers, programs, argList, returnType = "texture", bufferTypes = None):
		
		if self.buffersToVideo(buffers, bufferTypes):
			pingPong = 0
			h,w = buffers[0].shape
			
			texs = list()
			
			for i in range(0, len(buffers)):
				texs.append(self.textures["texId"][i])
			
			self.applyProgram(programs[0], texs, pingPong, w, h, argList[0])
			
			for i in range(1, len(programs)):
				texs[0] = self.videoBuffers[pingPong].texture()
				pingPong = 1 - pingPong
				pingPong = self.applyProgram(programs[i], texs, pingPong, w, h, argList[i])
					
			return self.textureToArray(self.videoBuffers[pingPong].texture(), returnType)
		else:
			print("Couldn't load buffers to video memory!")
		
		return None
		
	def textureToArray(self, tex, returnType="texture"):
		if returnType == "texture":
			return tex
		if returnType == "uint16":
			self.makeCurrent()
			glBindTexture(GL_TEXTURE_RECTANGLE, tex)
			outData = glGetTexImageus(GL_TEXTURE_RECTANGLE, 0, GL_GREEN)
			glBindTexture(GL_TEXTURE_RECTANGLE, 0)
			self.doneCurrent()
			return outData
		if returnType == "float":
			self.makeCurrent()
			glBindTexture(GL_TEXTURE_RECTANGLE, tex)
			outData = glGetTexImagef(GL_TEXTURE_RECTANGLE, 0, GL_GREEN)
			glBindTexture(GL_TEXTURE_RECTANGLE, 0)
			self.doneCurrent()
			return outData
		if returnType == "floatRGB":
			self.makeCurrent()
			glBindTexture(GL_TEXTURE_RECTANGLE, tex)
			outData = glGetTexImagef(GL_TEXTURE_RECTANGLE, 0, GL_RGB)
			glBindTexture(GL_TEXTURE_RECTANGLE, 0)
			self.doneCurrent()
			return outData
			
		return None
		
		
	def applyProgram(self, pType, texs, pingPong, w, h, argList):
		
		#print("Calling program " + str(pType) + " argList is " + str(argList) + " ping pong " + str(pingPong))
		
		if pType == 0:
			self.videoBuffers[pingPong].imAdjust(self.shadePrograms[pType], texs[0], w, h, *argList)
		elif pType == 1 or pType == 2:
			self.videoBuffers[pingPong].medGaussFilt(self.shadePrograms[pType], texs[0], w, h)
		elif pType == 3:
			pingPong = 2
			self.videoBuffers[pingPong].hsv2rgb(self.shadePrograms[pType], texs[0], texs[1], w, h, *argList)
		elif pType == 4:
			self.videoBuffers[pingPong].processFluorescence(self.shadePrograms[pType], texs[0], texs[1], texs[2], w, h, *argList)
		elif pType == 5:
			pingPong = 2
			self.videoBuffers[pingPong].applyColormapGLSL(self.shadePrograms[pType], texs[0], w, h)
		
		return pingPong
		
	def applyColormapGLSL(self, image, w, h, imMin, imMax, returnType="texture"):
		if str(type(image)) != "<type 'numpy.ndarray'>":
			tex1= image
		else:
			buffers = list([image])
			bufferType = list(['float'])
			self.buffersToVideo(buffers, bufferType)
			tex1 = self.textures["texId"][0]
		
		self.videoBuffers[2].applyColormapGLSL(tex1, self.shadePrograms[5], w, h, imMin, imMax)
		return self.textureToArray(self.videoBuffers[2].texture(), returnType)
			
	def HSVImageGLSL(self, image, value, w, h, hmn, hmx, mn, mx, returnType="texture"):
		
		if str(type(image)) != "<type 'numpy.ndarray'>":
			buffers = list([value])
			bufferType = list(['float'])
			self.buffersToVideo(buffers, bufferType)
			tex1 = image
			tex2 = self.textures["texId"][0]
		else:
			buffers = list([value, image])
			bufferType = list(['float', 'float'])
			self.buffersToVideo(buffers, bufferType)
			tex1 = self.textures["texId"][1]
			tex2 = self.textures["texId"][0]
		
		
		
		self.videoBuffers[2].hsv2rgb(self.shadePrograms[3], tex1, tex2, w, h, hmn, hmx, mn, mx)
		
		return self.textureToArray(self.videoBuffers[2].texture(), returnType)
		
	def checkGLError(self, msg=None):
		err = glGetError()
		if err != GL_NO_ERROR:
			s = "Opengl error "
			if msg != None:
				s = s + msg
				
			print s
			
	def wheelEvent(self, event):
		if event.delta() > 0:
			self.ImageZoomSteps = self.ImageZoomSteps + 1
		else:
			self.ImageZoomSteps = self.ImageZoomSteps - 1
			
		self.ImageZoom = pow(1.25, self.ImageZoomSteps)
		self.updateGL()
		
	def mousePressEvent(self, event):
		self.IsMouseDown = 1
		if event.button() == Qt.RightButton:
			self.RightMouseButtonClicked = 1
		else:
			self.RightMouseButtonClicked = 0
			
	def mouseReleaseEvent(self, event):
		
		if self.IsMouseDown == 1 and self.RightMouseButtonClicked == 1:
			
			a,b = self.screenToImage(event.x(), event.y())
			
			w, h = self.SequenceDisplay.frameWidth, self.SequenceDisplay.frameHeight
			
			if w > a and a > 0 and h > b and b > 0:
				if self.DrawRoiStatus == "idle":
					self.DrawRoiStatus = "drawing"
					self.rois.append(Roi())

					
				self.rois[-1].addPoint(a,b)
				self.repaint()
		
		self.IsMouseDown = 0
	
	def screenToImage(self,x,y):
		a = x / self.ImageZoom
		b = y / self.ImageZoom
		
		return a,b
		
	def mouseMoveEvent(self, event):
		a,b = self.screenToImage(event.x(), event.y())
		self.emit(QtCore.SIGNAL("mousePositionChanged(int, int)"), a, b)
		
	def mouseDoubleClickEvent(self, event):
		if self.DrawRoiStatus == "drawing":
			self.DrawRoiStatus = "idle"
			self.addRoi(self.rois[-1])
			
	def addRoi(self,roi,fromImageDisplayWidget = True):
		if not fromImageDisplayWidget:
			self.rois.append(roi)
		roi.computePointMap()
		roi.ordinal = len(self.rois) - 1
		
		colorCycle = matplotlib.rcParams["axes.color_cycle"]
		
		roiCol = matplotlib.colors.colorConverter.to_rgb(colorCycle[self.rois[-1].ordinal % len(colorCycle)])
		
		c = QColor()
		c.setRgbF(roiCol[0], roiCol[1], roiCol[2])
		roi.color = c
		
		self.emit(QtCore.SIGNAL("roiRecomputeNeeded(bool)"), True)
		
		self.SequenceDisplay.tiffSequence.rois.append(self.rois[-1])
		self.updateGL()
		
		self.emit(QtCore.SIGNAL("roiAdded(int)"), id(self))
