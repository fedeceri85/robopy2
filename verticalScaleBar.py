from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.GraphicsObject import *
from pyqtgraph.GraphicsWidgetAnchor import *
from pyqtgraph.TextItem import TextItem
import numpy as np
from pyqtgraph import functions as fn
from pyqtgraph import getConfigOption
from pyqtgraph.Point import Point


class verticalScaleBar(GraphicsObject, GraphicsWidgetAnchor):
    """
    Displays a rectangular bar to indicate the relative scale of objects on the view.
    """
    def __init__(self, size, width=5, brush=None, pen=None, suffix='m', offset=None):
        GraphicsObject.__init__(self)
        GraphicsWidgetAnchor.__init__(self)
        self.setFlag(self.ItemHasNoContents)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        
        if brush is None:
            brush = getConfigOption('foreground')
        self.brush = fn.mkBrush(brush)
        self.pen = fn.mkPen(pen)
        self._width = width
        self.size = size
        if offset == None:
            offset = (0,0)
        self.offset = offset
        
        self.bar = QtGui.QGraphicsRectItem()
        self.bar.setPen(self.pen)
        self.bar.setBrush(self.brush)
        self.bar.setParentItem(self)
        
        self.text = TextItem(text=fn.siFormat(size, suffix=suffix), anchor=(1,0.5))
        self.text.setParentItem(self)

    def parentChanged(self):
        view = self.parentItem()
        if view is None:
            return
        view.sigRangeChanged.connect(self.updateBar)
        self.updateBar()
        
        
    def updateBar(self):
        view = self.parentItem()
        if view is None:
            return
        p1 = view.mapFromViewToItem(self, QtCore.QPointF(0,0))
        p2 = view.mapFromViewToItem(self, QtCore.QPointF(self.size,0))
        w = (p2-p1).x()
        self.bar.setRect(QtCore.QRectF(0,-w,self._width,w))
        self.text.setPos(0,-w/2.)

    def boundingRect(self):
        return QtCore.QRectF()

    def setParentItem(self, p):
        ret = GraphicsObject.setParentItem(self, p)
        if self.offset is not None:
            offset = Point(self.offset)
            anchorx = 1 if offset[0] <= 0 else 0
            anchory = 1 if offset[1] <= 0 else 0
            anchor = (anchorx, anchory)
            self.anchor(itemPos=anchor, parentPos=anchor, offset=offset)
        return ret