import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DeviceDock(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    vlayout = QVBoxLayout()
    self.view = QListView(self)
    self.model = QStandardItemModel(self.view)
    self.view.setModel(self.model)
    vlayout.addWidget(self.view)
    self.setLayout(vlayout)
    # signals
    self.driversPath = '%s/drivers/' % os.path.dirname(os.path.realpath(__file__))

  
  def visibilityToggled(self, visible):
    if visible:
      self.model.clear()
      for fn in os.listdir(self.driversPath):
        if fn.startswith('.') or fn.startswith('_'): continue
        item = QStandardItem()
        item.setText(fn[:-3])
        item.setEditable(False)
        self.model.appendRow(item)
