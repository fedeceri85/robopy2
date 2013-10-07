from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from PyQt4.QtCore import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.ARB.multitexture import *

import numpy as np

'''
Video processing implemented on a QGLFramebuffer and using GLSL programmin
'''
class VideoProcessor(QGLFramebufferObject):
        def __init__(self, w, h, openglContext, internalType = GL_RGB32F): # = GL_LUMINANCE_FLOAT32_ATI):
                
                self.openglContext = openglContext
                openglContext.makeCurrent()
                
                super(VideoProcessor, self).__init__(w, h, QGLFramebufferObject.NoAttachment, GL_TEXTURE_RECTANGLE, internalType)
                
                
                supMulti = glGetIntegerv(GL_MAX_TEXTURE_UNITS_ARB)
                print("VideoProcessor: " + str(supMulti) + " textures supported")
                if supMulti < 3:
                        print("VideoProcessor: needed multi texture mode of at least 3, while only " + str(supMulti) + " supported")
                
                glActiveTexture(GL_TEXTURE3)
                glEnable(GL_TEXTURE_RECTANGLE)
                        
                glActiveTexture(GL_TEXTURE1)
                glEnable(GL_TEXTURE_RECTANGLE)
                
                glActiveTexture(GL_TEXTURE0)
                glEnable(GL_TEXTURE_RECTANGLE)
                
                glActiveTexture(GL_TEXTURE2)
                glEnable(GL_TEXTURE_RECTANGLE)
                        
                glActiveTexture(GL_TEXTURE1)
                glEnable(GL_TEXTURE_RECTANGLE)
                
                glActiveTexture(GL_TEXTURE0)
                glEnable(GL_TEXTURE_RECTANGLE)
                
                glEnable(GL_LINE_SMOOTH)
                openglContext.doneCurrent()
                
        def __del__(self):
                pass
                
        def saveGLState(self):
                glPushAttrib(GL_ALL_ATTRIB_BITS)
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                
        def restoreGLState(self):
                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPopMatrix()
                glPopAttrib()
                
        def prepareRender(self, prg):
                w = self.width()
                h = self.height()
                
                self.openglContext.makeCurrent()
                self.checkGLError()
                self.bind()
                self.saveGLState()
                
                
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                
                glViewport(0,0,w,h)
                glOrtho(0, w, 0, h, -1, 1) #must modify if a flip is introduced
                
                
                
                glClearColor(0.0, 1.0, 0.0, 0.0)
                glClear(GL_COLOR_BUFFER_BIT)
                prg.bind()
                
        def drawTexes(self, tex, w, h):
                
                texParams = list({GL_TEXTURE0, GL_TEXTURE1, GL_TEXTURE2, GL_TEXTURE3})
                nTex = len(tex)
                for i in range(0,nTex):
                        glActiveTexture(texParams[i])
                        glEnable(GL_TEXTURE_RECTANGLE)
                        glBindTexture(GL_TEXTURE_RECTANGLE, tex[i])
                        
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
                        
                for i in range(0,nTex):
                        glActiveTexture(texParams[i])
                        glBindTexture(GL_TEXTURE_RECTANGLE, 0)
                        
                glActiveTexture(texParams[0])
                
        def endRender(self, prg):
                        
                glFlush()
                prg.release()
                self.restoreGLState()
                self.release()
                        
                self.checkGLError()
                self.openglContext.doneCurrent()
                
        def addTraces(self, data, nPoints, x, y, scalex, scaley, color, lineWidth = 1):
                
                w = self.width()
                h = self.height()
                
                self.openglContext.makeCurrent()
                self.checkGLError()
                self.bind()
                self.saveGLState()
                
                
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                
                glViewport(0,0,w,h)
                glOrtho(0, w, h, 0, -1, 1) 
                
                glColor4f(color[0], color[1], color[2], 0.0)
                glLineWidth(lineWidth);
                glTranslatef(x, y, 0.0)
                glScalef(scalex, scaley, 1.0)
                glBegin(GL_LINE_STRIP)
                
                for i in range(0, 2*nPoints, 2):
                        glVertex2f(data[i], data[i+1])
                
                glEnd()
                
                glFlush()
                self.restoreGLState()
                self.release()
                        
                self.checkGLError()
                self.openglContext.doneCurrent()
                
        def niceNumber(self, value, round_=False):
                exponent = math.floor(math.log(value,10))
                fraction = value / 10 ** exponent
                
                if round_:
                        if fraction < 1.5:
                                niceFraction = 1.
                        elif fraction < 3.:
                                niceFraction = 2.
                        elif fraction < 7.:
                                niceFraction = 5.
                        else:
                                niceFraction = 10.
                else:
                        if fraction <= 1:
                                niceFraction = 1.
                        elif fraction <= 2:
                                niceFraction = 2.
                        elif fraction <= 5:
                                niceFraction = 5.
                        else:
                                niceFraction = 10.
                
                return niceFraction * 10 ** exponent
        
        def niceBounds(self, axisStart, axisEnd, numTicks= 10):
                axisWidth = axisEnd - axisStart
                if axisWidth == 0:
                        niceTick = 0
                else:
                        niceRange = niceNumber(axisWidth)
                        niceTick = niceNumber(niceRange / (numTicks - 1), round_=True)
                        axisStart = math.floor(axisStart / niceTick) * niceTick
                        axisEnd = math.ceil(axisEnd / niceTick) * niceTick
                return axisStart, axisEnd, niceTick
        
                
        def addText(self, s, x, y, color,fontsize=12.0):
                
                w = self.width()
                h = self.height()
                
                self.openglContext.makeCurrent()
                self.checkGLError()
                self.bind()
                self.saveGLState()
                
                
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                
                glMatrixMode(GL_MODELVIEW)
                glLoadIdentity()
                
                glViewport(0,0,w,h)
                glOrtho(0, w, 0, h, -1, 1) 
                
                fontWidth = glutStrokeWidth(GLUT_STROKE_ROMAN, ord('O'))
                fontScale = fontsize/fontWidth
                glTranslatef(x, y, 0.0)
                glScalef(fontScale, -fontScale, 1.0)
                
                glColor4f(color[0], color[1], color[2], 0.0)
                glutStrokeString(GLUT_STROKE_ROMAN, s)
                
                glFlush()
                self.restoreGLState()
                self.release()
                        
                self.checkGLError()
                self.openglContext.doneCurrent()        
        
        def imAdjust(self, prg, tex, w, h, mn=0.0, mx=65535.0, r=1.0, g=1.0, b=1.0):
                if self.isValid():
                        
                        #print("Imadjust: " + str(mn) + " " + str(mx))
                        
                        self.prepareRender(prg)
                        
                        mnLoc = prg.uniformLocation("mn")
                        mxLoc = prg.uniformLocation("mx")
                        
                        prg.setUniformValue(mnLoc, float(mn) / 65535.0)
                        prg.setUniformValue(mxLoc, float(mx) / 65535.0)
                        
                        rLoc = prg.uniformLocation("r")
                        gLoc = prg.uniformLocation("g")
                        bLoc = prg.uniformLocation("b")
                        
                        prg.setUniformValue(rLoc, r)
                        prg.setUniformValue(gLoc, g)
                        prg.setUniformValue(bLoc, b)
                        
                        self.drawTexes(list([tex]), w, h)
                        self.endRender(prg)
                        
        def medGaussFilt(self, prg, tex, w, h):
                if self.isValid():
                        self.prepareRender(prg)
                        self.drawTexes(list([tex]), w, h)
                        self.endRender(prg)
                        
        def hsv2rgb(self, prg, tex, valTex, w, h, hmn, hmx, mn, mx, hcutoff=0.47):
                if self.isValid():
                        
                        #print("hsv2rgb params: " + str(hmn) + ", " + str(hmx) + ", " + str(mn) + ", " + str(mx))
                        
                        self.prepareRender(prg)
                        
                        hmnLoc = prg.uniformLocation("hmn")
                        hmxLoc = prg.uniformLocation("hmx")
                        mnLoc = prg.uniformLocation("mn")
                        mxLoc = prg.uniformLocation("mx")
                        hcutoffLoc = prg.uniformLocation("hcutoff")
                        prg.setUniformValue(hmnLoc, float(hmn))
                        prg.setUniformValue(hmxLoc, float(hmx))
                        prg.setUniformValue(mnLoc, float(mn))
                        prg.setUniformValue(mxLoc, float(mx))
                        prg.setUniformValue(hcutoffLoc,float(hcutoff))
                        prg.setUniformValue("view1", 0)
                        prg.setUniformValue("bckView", 1)
                        
                        self.drawTexes(list([tex, valTex]), w, h)
                        self.endRender(prg)
                        
        def processFluorescence(self, prg, t1, t2, tref, w, h, pType, dType, bck1=0, bck2=0):
                if self.isValid():
                        self.prepareRender(prg)
                        
                        #print("processFluorescence params: " + str(w) + ", " + str(h) + ", " + str(pType) + ", " + str(dType) + ", " + str(bck1) + ", " + str(bck2))
                        
                        pTypeLoc = prg.uniformLocation("procType")
                        dTypeLoc = prg.uniformLocation("dispType")
                        bck1Loc = prg.uniformLocation("bck1")
                        bck2Loc = prg.uniformLocation("bck2")
                        if pTypeLoc != -1:
                                prg.setUniformValue(pTypeLoc, int(pType))
                        else:
                                print("pType not used!")
                        
                        if dTypeLoc != -1:
                                prg.setUniformValue(dTypeLoc, int(dType))
                        else:
                                print("dTypeLoc not used!")
                        
                        if bck1Loc != -1:
                                prg.setUniformValue(bck1Loc, float(bck1))
                        else:
                                print("bck1Loc not used!")
                        
                        if bck2Loc != -1:
                                prg.setUniformValue(bck2Loc, float(bck2))
                        else:
                                print("bck2Loc not used!")
                        
                        #prg.setUniformValue("procType", pType)
                        #prg.setUniformValue("dispType", dType)
                        #prg.setUniformValue("bck1", bck1)
                        #prg.setUniformValue("bck2", bck2)
                        
                        f1Loc = prg.uniformLocation("f1")
                        f2Loc = prg.uniformLocation("f2")
                        refLoc = prg.uniformLocation("ref")
                        
                        if f1Loc != -1:
                                prg.setUniformValue("f1", 0)
                        else:
                                print("f1Loc not used!")
                        
                        if f2Loc != -1:
                                prg.setUniformValue("f2", 1)
                        else:
                                print("f2Loc not used!")
                        
                        if refLoc != -1:
                                prg.setUniformValue("ref", 2)
                        else:
                                print("refLoc not used!")
                        
                        self.drawTexes(list([t1, t2, tref]), w, h)
                        self.endRender(prg)
                        
        def applyColormapGLSL(self, data, prg, w, h, imMin=0.0, imMax=1.0):
                if self.isValid():
                        self.prepareRender(prg)
                        
                        mnLoc = prg.uniformLocation("mapMn")
                        mxLoc = prg.uniformLocation("mapMx")
                        prg.setUniformValue(mnLoc, float(imMin))
                        prg.setUniformValue(mxLoc, float(imMax))
                        
                        prg.setUniformValue("f1", 0)
                        
                        self.drawTexes(list([data]), w, h)
                        self.endRender(prg)
        
        def checkGLError(self, msg=None):
                err = glGetError()
                if err != GL_NO_ERROR:
                        s = "Opengl error "
                        if msg != None:
                                s = s + msg
                                
                        print s 
                
        def checkError(self, msg=None):
                status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
                if status != GL_FRAMEBUFFER_COMPLETE_EXT:
                        s = "Framebuffer object error! "
                        if msg != None:
                                s = s + msg
                                
                        print s