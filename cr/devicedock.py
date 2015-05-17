import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DeviceDock(QDockWidget):
  def __init__(self, parent=None):
    QDockWidget.__init__(self, parent)

  def setup(self, roastClient):
    self.roastClient = roastClient
    # setup widgets
    self.model = QStandardItemModel(self.listDevices)
    self.listDevices.setModel(self.model)
    self.pathDrivers = '%s/drivers/' % os.path.dirname(os.path.realpath(__file__))
    # signals
    self.model.itemChanged.connect(self.itemChecked)
    self.visibilityChanged.connect(self.visibilityToggled)
  
  def visibilityToggled(self, visible):
    self.model.clear()
    for fn in os.listdir(self.pathDrivers):
      if fn.startswith('.') or fn.startswith('_') or fn[-3:] != '.py': continue
      item = QStandardItem()
      item.setText(fn[:-3])
      item.setEditable(False)
      item.setCheckable(True)
      item.setCheckState(False)
      self.model.appendRow(item)

  def itemChecked(self, item):
    chek = item.checkState()
    name = item.text()
    if chek == 2:
      self.roastClient.loadDevice(name)
    else:
      #self.roastClient.unloadDevice(name)
      pass
