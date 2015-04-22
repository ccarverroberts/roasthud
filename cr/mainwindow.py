# external dependencies
import os, os.path
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

windowClass = uic.loadUiType('%s/GUI/MainWindow.ui' % os.path.dirname(os.path.realpath(__file__)))[0]

# Used for spacing GUI elements in the toolbar
class Spacer(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 


# Main roast profiling window
class MainWindow(QMainWindow, windowClass):
  def __init__(self):
    QMainWindow.__init__(self)
    self.setupUi(self)
    # setup
    self.dockDevices.hide()
    self.dockProfiles.hide()
    # connect signals
    self.buttonDevices.clicked.connect(self.toggleDevices)
    self.buttonProfiles.clicked.connect(self.toggleProfiles)
    #self.dockDevices.visibilityChanged.connect(self.dockDevicesContents.visibilityToggled)
    #self.dockProfiles.visibilityChanged.connect(self.dockProfilesContents.visibilityToggled)

  def toggleDevices(self):
    if self.dockDevices.isVisible(): self.dockDevices.hide()
    else: self.dockDevices.show()

  def toggleProfiles(self):
    if self.dockProfiles.isVisible(): self.dockProfiles.hide()
    else: self.dockProfiles.show()
