import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DeviceManager(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, None)
    self.roastClient = parent
    # Create list view
    self.view = QListView(self)
    self.model = QStandardItemModel(self.view)
    self.view.setModel(self.model)
    # Create layout
    self.grid = QGridLayout()
    self.grid.addWidget(self.view, 0, 0, 1, 1)
    self.grid.setRowStretch(0, 1)
    self.grid.setColumnStretch(0, 1)
    self.setLayout(self.grid)
    # Load available module names, add to list
    self.dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append('%s/Drivers/' % self.dir)
    self.N = 0
    for fn in os.listdir('%s/Drivers' % self.dir):
      if fn.startswith('.') or fn.startswith('_'): continue
      item = QStandardItem()
      item.setText(fn[:-3])
      item.setEditable(False)
      self.model.appendRow(item)
      self.N += 1
    self.view.doubleClicked.connect(self.doubleClickItem)

  def doubleClickItem(self, itemindex):
    filename = '%s/Drivers/%s.py' % (self.dir, itemindex.data())
    if os.path.isfile(filename):
      self.loadDevice(itemindex.data())
      self.hide()
      self.roastClient.connectDevice()
      self.roastClient.show()

  def loadDevice(self, module):
    print('Loading device driver: ', module)
    plugin = __import__(module)
    driver = plugin.Driver(self.roastClient)
    driver.IPaddress = '192.168.1.13'
    self.roastClient.device = driver
