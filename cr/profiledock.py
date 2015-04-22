import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ProfileDock(QWidget):
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
    print('profiles visibility', visible)
