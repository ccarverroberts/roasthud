from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cr.roastgraph import RoastGraph, DeltaGraph


'''
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
    self.plot = RoastGraphPlot()
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
'''
