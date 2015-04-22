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

