import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DeviceDock(QDockWidget):
  def __init__(self, parent=None):
    QDockWidget.__init__(self, parent)

  def setup(self):
    # setup widgets
    self.model = QStandardItemModel(self.listDevices)
    self.listDevices.setModel(self.model)
    self.pathDrivers = '%s/drivers/' % os.path.dirname(os.path.realpath(__file__))
    # signals
    self.visibilityChanged.connect(self.visibilityToggled)
  
  def visibilityToggled(self, visible):
    print('devices visibility', visible)
    self.model.clear()
    for fn in os.listdir(self.pathDrivers):
      if fn.startswith('.') or fn.startswith('_'): continue
      item = QStandardItem()
      item.setText(fn[:-3])
      item.setEditable(False)
      item.setCheckable(True)
      item.setCheckState(False)
      self.model.appendRow(item)
