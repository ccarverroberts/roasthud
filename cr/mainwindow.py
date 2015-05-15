# external dependencies
import os, os.path
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from cr.profile import Profile

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
    self.devices = []
    self.profiles = [Profile()]
    self.setupUi(self)
    # setup
    self.dockDevices.listDevices = self.listDevices;
    self.dockDevices.setup(self)
    self.dockProfiles.listProfiles = self.listProfiles;
    self.dockProfiles.setup(self)
    # connect signals
    self.buttonDevices.clicked.connect(self.toggleDevices)
    self.buttonProfiles.clicked.connect(self.toggleProfiles)
    self.buttonConnection.toggled.connect(self.toggleConnect)

  def toggleDevices(self):
    if self.dockDevices.isVisible(): self.dockDevices.hide()
    else: self.dockDevices.show()

  def toggleProfiles(self):
    if self.dockProfiles.isVisible(): self.dockProfiles.hide()
    else: self.dockProfiles.show()

  def toggleConnect(self):
    if self.buttonConnection.isChecked():
      for dev in self.devices:
        dev.connect()
    else:
      for dev in self.devices:
        dev.stop()

  def loadDevice(self, name):
    mod = __import__(name, fromlist=['*'])
    cls = getattr(mod, name)
    gui = uic.loadUiType('%s/drivers/%s.ui' % (os.path.dirname(os.path.realpath(__file__)), name))[0]
    drv = cls(self, gui)
    self.devices.append(drv)
    
