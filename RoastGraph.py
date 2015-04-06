#!/usr/bin/python3

import sys, time, threading, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from RoastProfile import RoastProfile

class RoastGraph(QWidget):
  def __init__(self, parent):
    super(RoastGraph, self).__init__(parent)
    # value boundaries
    self.boundsX = [0., 15.*60.]
    self.boundsY = [0., 300.]
    # gridding
    self.minorTickX = 10
    self.minorTickY = 10
    self.majorTickX = 60
    self.majorTickY = 20
    # colors
    self.colorBackground = QColor(240., 240., 240.)
    self.Tdry = 155.
    self.colorBackgroundDry = QColor(240., 255., 240.)
    self.Tfc = 195.
    self.colorBackgroundRamp = QColor(255., 255., 240.)
    self.colorBackgroundFC = QColor(255., 240., 235.)
    self.colorTicks = QColor(190, 190, 190)
    self.colorTicksBold = QColor(160, 160, 160)
    self.colorText = QColor(0, 0, 0)
    # fonts
    self.font = QFont("Fixed", pointSize=11.)
    self.fontBig = QFont("Fixed", pointSize=14.)
    self.fontSmall = QFont("Fixed", pointSize=9.)
    # visual preferences
    self.padding = [80., 20., 60., 60]
    # labels
    self.labelTitle = ''
    self.labelX = 'Time (min)'
    self.labelY = 'Temperature (°C)'
    # plots
    self.Tplots = []
    self.dTplots = []
    #self.plots.append(RoastProfile(label='Active'))
    #for fn in sys.argv[2:]:
    #  self.plots.append(RoastProfile(filename=fn, label=fn))

  def screenX(self, x):
    x = float(x)
    return self.padding[0] + ((x / self.boundsX[1]) * (self.width() - self.padding[0] - self.padding[1]))

  def screenY(self, y):
    y = float(y)
    return (self.height() - self.padding[3]) - (((float(y) - self.boundsY[0]) / (self.boundsY[1] - self.boundsY[0])) * (self.height() - self.padding[2] - self.padding[3]))

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.HighQualityAntialiasing)
    # paint background and borders
    if self.boundsY[1] > 100.:
      painter.fillRect(self.padding[0], self.screenY(self.boundsY[1]), self.width() - self.padding[0] - self.padding[1], self.screenY(self.Tfc)-self.screenY(self.boundsY[1]), self.colorBackgroundFC)
      painter.fillRect(self.padding[0], self.screenY(self.Tfc), self.width() - self.padding[0] - self.padding[1], self.screenY(self.Tdry)-self.screenY(self.Tfc), self.colorBackgroundRamp)
      painter.fillRect(self.padding[0], self.screenY(self.Tdry), self.width() - self.padding[0] - self.padding[1], self.screenY(self.boundsY[0])-self.screenY(self.Tdry), self.colorBackgroundDry)
    else:
      painter.fillRect(self.padding[0], self.screenY(self.boundsY[1]), self.width() - self.padding[0] - self.padding[1], self.height() - self.padding[2] - self.padding[3], self.colorBackground)
    self.paintTicks(painter)
    # paint all plots
    for plot in reversed(self.Tplots):
      painter.setPen(QPen(plot.qcolor, 2.0))
      self.paintPlot(painter, plot)
    for plot in reversed(self.dTplots):
      painter.setPen(QPen(plot.qcolor, 2.0))
      self.paintPlot(painter, plot, dy=True)
    # paint title area
    painter.setFont(self.fontBig)
    painter.setPen(self.colorText)
    painter.drawText(QRect(0, 15., self.width(), 20.), Qt.AlignCenter, self.labelTitle)
    #if len(self.plots[0].y) > 0:
    #  try:
    #    ady = 0.
    #    for i in range(10):
    #      ady += self.plots[0].dy[-1-i]
    #    ady /= 10
    #    painter.drawText(QRect(0, 15., self.width(), 20.), Qt.AlignCenter, 'T: %.1f°C     dT: %.1f°C/min     t: %s' % (self.plots[0].y[-1], ady, self.readableTime(self.plots[0].x[-1])))
    #  except IndexError:
    #    painter.drawText(QRect(0, 15., self.width(), 20.), Qt.AlignCenter, 'T: %.1f°C     dT: --°C/min     t: %s' % (self.plots[0].y[-1], self.readableTime(self.plots[0].x[-1])))

  def paintTicks(self, painter):
    painter.setPen(self.colorTicks)
    painter.setFont(self.fontSmall)
    Nticks = int((self.boundsX[1]-self.boundsX[0]) / self.minorTickX)
    for xi in range(Nticks):
      i = (xi * (self.boundsX[1] - self.boundsX[0]) / Nticks) + self.boundsX[0]
      x = self.screenX(i)
      painter.drawLine(x, self.padding[2], x, self.height() - self.padding[3])
    Nticks = int((self.boundsY[1]-self.boundsY[0]) / self.minorTickY)
    for yi in range(Nticks):
      i = (yi * (self.boundsY[1] - self.boundsY[0]) / Nticks) + self.boundsY[0]
      y = self.screenY(i)
      painter.drawLine(self.padding[0], y, self.width() - self.padding[1], y)
      if i % self.majorTickY != 0:
        painter.drawText(QRect(-5, y - 5, self.padding[0] - 1., 20), Qt.AlignRight, '%d' % i)

    painter.setFont(self.font)
    painter.setPen(self.colorTicksBold)
    Nticks = int((self.boundsX[1]-self.boundsX[0]) / self.majorTickX)
    for xi in range(Nticks + 1):
      i = (xi * (self.boundsX[1] - self.boundsX[0]) / Nticks) + self.boundsX[0]
      x = self.screenX(i)
      painter.setPen(self.colorTicksBold)
      painter.drawLine(x, self.padding[2], x, self.height() - self.padding[3])
      painter.setPen(self.colorText)
      if i != 0:
        painter.drawText(QRect(x-3, self.height() - self.padding[3] + 2, 30, 20), 0, '%d' % ((i - self.boundsX[0])/60))
    Nticks = int((self.boundsY[1]-self.boundsY[0]) / self.majorTickY)
    for yi in range(Nticks + 1):
      i = (yi * (self.boundsY[1] - self.boundsY[0]) / Nticks) + self.boundsY[0]
      y = self.screenY(i)
      painter.setPen(self.colorTicksBold)
      painter.drawLine(self.padding[0], y, self.width() - self.padding[1], y)
      painter.setPen(self.colorText)
      painter.drawText(QRect(-5, y - 5, self.padding[0] - 1., 20), Qt.AlignRight, '%d' % i)

    painter.setFont(self.fontBig)
    painter.setPen(self.colorText)
    painter.drawText(QRect(0, self.height() - 10. - 20., self.width(), 20.), Qt.AlignCenter, self.labelX)
    painter.save()
    painter.rotate(-90.)
    painter.drawText(QRect(-self.height(), 10., self.height(), 20.), Qt.AlignCenter, self.labelY)
    painter.restore()

  def paintPlot(self, painter, plot, dy=False):
    if dy: Ydist = plot.dy
    else:  Ydist = plot.y
    lastP = []
    for i in range(len(plot.x)):
      X = self.screenX(plot.x[i])
      #Y = self.screenY(Ysmooth[plot.x[i]])
      Y = self.screenY(Ydist[i])
      if plot.x[i] >= self.boundsX[0] and Ydist[i] >= self.boundsY[0] and plot.x[i] <= self.boundsX[1] and Ydist[i] <= self.boundsY[1]:
        if i == 0:
          painter.drawPoint(X, Y)
        else:
          painter.drawLine(lastP[0], lastP[1], X, Y)
      lastP = [X, Y]
    painter.setPen(QPen(plot.qcolor, 1.0))
    painter.setFont(self.font)
    for comment in plot.comments:
      X = self.screenX(int(comment[0]))
      Y = self.screenY(float(comment[1]))
      if int(comment[0]) < 0: continue
      C = comment[2]
      painter.drawPoint(X, Y)
      painter.drawLine(X, self.screenY(self.boundsY[1]), X, self.screenY(self.boundsY[0]))
      #if X < 90: painter.drawText(QRect(X, Y - 15., 100, 20.), Qt.AlignLeft, C)
      #else: painter.drawText(QRect(X - 100, Y - 20., 100, 20.), Qt.AlignRight, C)
      painter.drawText(QRect(X - 100, self.height() - self.padding[3] - 20., 99, 20.), Qt.AlignRight, C)

  def readableTime(self, s):
    tMin = int(s / 60)
    tSec = int(s % 60)
    stSec = ''
    if tSec < 10:
      stSec = '0%d' % tSec
    else:
      stSec = str(tSec)
    return '%d:%s' % (tMin, stSec)




