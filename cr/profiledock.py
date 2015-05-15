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
  
  def visibilityToggled(self, visible):
    self.model.clear()
    for p in self.roastClient.profiles:
      item = QStandardItem()
      item.setText(p.label)
      item.setEditable(False)
      item.setCheckable(False)
      self.model.appendRow(item)
