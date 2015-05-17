import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ProfileDock(QDockWidget):
  def __init__(self, parent=None):
    QDockWidget.__init__(self, parent)

  def setup(self, roastClient):
    self.roastClient = roastClient
    # setup widgets
    self.model = QStandardItemModel(self.listProfiles)
    self.listProfiles.setModel(self.model)
    # signals
    self.visibilityChanged.connect(self.visibilityToggled)
    self.roastClient.buttonPlotColor.clicked.connect(self.setPlotColor)
    self.roastClient.sliderPlotThickness.valueChanged.connect(self.setPlotThickness)
    self.listProfiles.clicked.connect(self.changeSelection)
    # selection
    self.selection = 0
  
  def visibilityToggled(self, visible):
    self.model.clear()
    if self.roastClient.roastProfile:
      for p in self.roastClient.roastProfile.profiles:
        item = QStandardItem()
        item.setText(p.label)
        item.setEditable(False)
        item.setCheckable(False)
        self.model.appendRow(item)

  def setPlotThickness(self, t):
    try:
      p = self.roastClient.roastProfile.profiles[self.selection]
      p.setThickness(t)
    except IndexError:
      pass
    self.roastClient.graphT.update()
    self.roastClient.graphDT.update()

  def setPlotColor(self):
    clr = QColorDialog.getColor()
    self.roastClient.buttonPlotColor.setStyleSheet('background-color: %s' % clr.name())
    try:
      p = self.roastClient.roastProfile.profiles[self.selection]
      p.setColor(clr)
    except IndexError:
      pass
    self.roastClient.graphT.update()
    self.roastClient.graphDT.update()

  def changeSelection(self, item):
    i = item.row()
    self.selection = i
    p = self.roastClient.roastProfile.profiles[i]
    self.roastClient.buttonPlotColor.setStyleSheet('background-color: %s' % p.color.name())
    self.roastClient.sliderPlotThickness.setValue(p.thickness)
