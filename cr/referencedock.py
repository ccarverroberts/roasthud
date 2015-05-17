import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from cr.profile import Profile, RoastProfile


class ReferenceDock(QDockWidget):
  def __init__(self, parent=None):
    QDockWidget.__init__(self, parent)

  def setup(self, roastClient):
    self.roastClient = roastClient
    # setup widgets
    self.model = QStandardItemModel(self.listReferences)
    self.listReferences.setModel(self.model)
    # signals
    self.visibilityChanged.connect(self.visibilityToggled)
    self.roastClient.buttonReferenceColor.clicked.connect(self.setReferenceColor)
    self.roastClient.buttonAddReference.clicked.connect(self.loadReference)
    self.roastClient.sliderReferenceThickness.valueChanged.connect(self.setReferenceThickness)
    self.listReferences.clicked.connect(self.changeSelection)
    # selection
    self.selection = 0
  
  def visibilityToggled(self, visible):
    self.model.clear()
    if self.roastClient.reference:
      for p in self.roastClient.reference.profiles:
        item = QStandardItem()
        item.setText(p.label)
        item.setEditable(False)
        item.setCheckable(False)
        self.model.appendRow(item)

  def setReferenceThickness(self, t):
    try:
      p = self.roastClient.reference.profiles[self.selection]
      p.setThickness(t)
    except IndexError:
      pass
    self.roastClient.graphT.update()
    self.roastClient.graphDT.update()

  def setReferenceColor(self):
    clr = QColorDialog.getColor()
    self.roastClient.buttonReferenceColor.setStyleSheet('background-color: %s' % clr.name())
    try:
      p = self.roastClient.reference.profiles[self.selection]
      p.setColor(clr)
    except IndexError:
      pass
    self.roastClient.graphT.update()
    self.roastClient.graphDT.update()

  def changeSelection(self, item):
    if self.roastClient.reference:
      i = item.row()
      self.selection = i
      p = self.roastClient.reference.profiles[i]
      self.roastClient.buttonReferenceColor.setStyleSheet('background-color: %s' % p.color.name())
      self.roastClient.sliderReferenceThickness.setValue(p.thickness)

  def loadReference(self):
    fname = QFileDialog.getOpenFileName(self, 'Open file')
    if fname:
      rp = RoastProfile(filename=fname)
      self.roastClient.reference = rp
      self.visibilityToggled(True)
      self.roastClient.graphT.update()
      self.roastClient.graphDT.update()
