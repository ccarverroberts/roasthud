import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ProfileDock(QDockWidget):
  def __init__(self, parent=None):
    QDockWidget.__init__(self, parent)
    # signals
    self.visibilityChanged.connect(self.visibilityToggled)

  def setup(self):
    pass
  
  def visibilityToggled(self, visible):
    print('profiles visibility', visible)
