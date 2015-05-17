from PyQt4.QtCore import *
from PyQt4.QtGui import *


class RoastGraphPlot(QWidget):
  def __init__(self, parent=None, xaxis=None, yaxis=None):
    QWidget.__init__(self, parent)
    self.xaxis = xaxis
    self.yaxis = yaxis

  def setup(self, roastClient):
    self.roastClient = roastClient

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    # ticks
    xtick = self.xaxis.tickRange
    ytick = self.yaxis.tickRange
    xconv = (xtick[1] - xtick[0]) / self.width()
    yconv = (ytick[1] - ytick[0]) / self.height()
    # draw grid
    if self.roastClient.settings.grid.major:
      painter.setPen(QPen(self.roastClient.settings.grid.colorMajor, 1.0))
      for i in range(int(ytick[0]), int(ytick[1]), int(ytick[2])):
        Y = self.height() - ((i - ytick[0]) / yconv)
        painter.drawLine(0, Y, self.width(), Y)
      for i in range(int(xtick[0]), int(xtick[1]), int(xtick[2])):
        X = self.width() - ((i - xtick[0]) / xconv)
        painter.drawLine(X, 0, X, self.height())
    if self.roastClient.settings.grid.minor:
      painter.setPen(QPen(self.roastClient.settings.grid.colorMinor, 1.0))
      for i in range(int(ytick[0]), int(ytick[1]), int(ytick[3])):
        if i % ytick[2] == 0: continue
        Y = self.height() - ((i - ytick[0]) / yconv)
        painter.drawLine(0, Y, self.width(), Y)
      for i in range(int(xtick[0]), int(xtick[1]), int(xtick[3])):
        if i % xtick[2] == 0: continue
        X = self.width() - ((i - xtick[0]) / xconv)
        painter.drawLine(X, 0, X, self.height())
    # draw profiles
    if self.roastClient.roastProfile:
      for p in self.roastClient.roastProfile.profiles:
        t = p.time
        if type(self.yaxis) is RoastGraphAxisDY: T = p.ror
        else: T = p.temp
        painter.setPen(p.pen)
        path = QPainterPath()
        for i in range(len(t)):
          X = (t[i] - xtick[0]) / xconv
          Y = self.height() - ((T[i] - ytick[0]) / yconv)
          if i == 0:
            path.moveTo(X, Y)
          else:
            path.lineTo(X, Y)
        painter.drawPath(path)
        



class RoastGraphAxisX(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)

  def setup(self, roastClient):
    self.roastClient = roastClient

  def updateSettings(self):
    # pull in settings
    self.penTick = self.roastClient.settings.axes.penTick
    self.tickSize = self.roastClient.settings.axes.tickSize
    self.tickRange = self.roastClient.settings.axes.rangeX
    self.axisSize = self.roastClient.settings.axes.size
    self.convFact = (self.tickRange[1] - self.tickRange[0]) / self.width()

  def paintEvent(self, event):
    self.updateSettings()
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    painter.setPen(self.penTick)
    painter.drawLine(0, 0, self.width(), 0)
    for i in range(int(self.tickRange[0]), int(self.tickRange[1]), int(self.tickRange[2])):
      X = (i - self.tickRange[0]) / self.convFact
      painter.drawLine(X, 0, X, self.tickSize)
    for i in range(int(self.tickRange[0]), int(self.tickRange[1]), int(self.tickRange[3])):
      if i % self.tickRange[2] == 0: continue
      X = (i - self.tickRange[0]) / self.convFact
      painter.drawLine(X, 0, X, self.tickSize * 0.5)
      



class RoastGraphAxisY(RoastGraphAxisX):
  def __init__(self, parent=None):
    RoastGraphAxisX.__init__(self, parent)

  def updateSettings(self):
    # pull in settings
    self.penTick = self.roastClient.settings.axes.penTick
    self.tickSize = self.roastClient.settings.axes.tickSize
    self.tickRange = self.roastClient.settings.axes.rangeY
    self.axisSize = self.roastClient.settings.axes.size
    self.convFact = (self.tickRange[1] - self.tickRange[0]) / self.height()

  def paintEvent(self, event):
    self.updateSettings()
    # paint
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    painter.setPen(self.penTick)
    painter.drawLine(self.axisSize, 0, self.axisSize, self.height())
    for i in range(int(self.tickRange[0]), int(self.tickRange[1]), int(self.tickRange[2])):
      Y = self.height() - ((i - self.tickRange[0]) / self.convFact)
      painter.drawLine(self.axisSize, Y, self.axisSize - self.tickSize, Y)
    for i in range(int(self.tickRange[0]), int(self.tickRange[1]), int(self.tickRange[3])):
      if i % self.tickRange[2] == 0: continue
      Y = self.height() - ((i - self.tickRange[0]) / self.convFact)
      painter.drawLine(self.axisSize, Y, self.axisSize - self.tickSize/2., Y)




class RoastGraphAxisDY(RoastGraphAxisY):
  def __init__(self, parent=None):
    RoastGraphAxisY.__init__(self, parent)

  def updateSettings(self):
    RoastGraphAxisY.updateSettings(self)
    self.tickRange = self.roastClient.settings.axes.rangeDY
    self.convFact = (self.tickRange[1] - self.tickRange[0]) / self.height()




class RoastGraph(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)

  def setup(self, roastClient):
    self.roastClient = roastClient
    # Setup layout
    self.grid = QGridLayout(self)
    self.setLayout(self.grid)
    self.xaxis = RoastGraphAxisX()
    self.xaxis.setup(roastClient)
    self.yaxis = RoastGraphAxisY()
    self.yaxis.setup(roastClient)
    self.plot = RoastGraphPlot(xaxis=self.xaxis, yaxis=self.yaxis)
    self.plot.setup(roastClient)
    self.grid.addWidget(self.xaxis, 1, 1)
    self.grid.addWidget(self.yaxis, 0, 0)
    self.grid.addWidget(self.plot,  0, 1)
    self.grid.setRowStretch(0, 1)
    self.grid.setColumnStretch(1, 1)
    self.grid.setSpacing(0)
    self.grid.setMargin(0)
    # Configure settings
    axisSize = self.roastClient.settings.axes.size;
    self.grid.setRowMinimumHeight(1, axisSize)
    self.grid.setColumnMinimumWidth(0, axisSize)

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.fillRect(0, 0, self.width(), self.height(), self.roastClient.settings.plots.colorBackground)



class DeltaGraph(RoastGraph):
  def __init__(self, parent=None):
    RoastGraph.__init__(self, parent)

  def setup(self, roastClient):
    self.roastClient = roastClient
    # Setup layout
    self.grid = QGridLayout(self)
    self.setLayout(self.grid)
    self.xaxis = RoastGraphAxisX()
    self.xaxis.setup(roastClient)
    self.yaxis = RoastGraphAxisDY() #this is the only change relative to RoastGraph
    self.yaxis.setup(roastClient)
    self.plot = RoastGraphPlot(xaxis=self.xaxis, yaxis=self.yaxis)
    self.plot.setup(roastClient)
    self.grid.addWidget(self.xaxis, 1, 1)
    self.grid.addWidget(self.yaxis, 0, 0)
    self.grid.addWidget(self.plot,  0, 1)
    self.grid.setRowStretch(0, 1)
    self.grid.setColumnStretch(1, 1)
    self.grid.setSpacing(0)
    self.grid.setMargin(0)
    # Configure settings
    axisSize = self.roastClient.settings.axes.size;
    self.grid.setRowMinimumHeight(1, axisSize)
    self.grid.setColumnMinimumWidth(0, axisSize)
