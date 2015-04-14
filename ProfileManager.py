import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ProfileManager(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, None)
    self.roastClient = parent
    self.setWindowTitle('Profile Manager')
    # Create list view
    self.view = QListView(self)
    self.model = QStandardItemModel(self.view)
    self.view.setModel(self.model)
    # Plot color selection
    self.btnPlotColor = QPushButton(" ")
    self.btnPlotColor.pressed.connect(self.selectPlotColor)
    # Create layout
    self.grid = QGridLayout()
    self.grid.addWidget(self.view, 0, 0, 5, 1)
    self.grid.addWidget(QLabel("Plot Color:"), 0, 1, 1, 1)
    self.grid.addWidget(self.btnPlotColor, 0, 2, 1, 1)
    self.grid.setColumnStretch(1, 1)
    self.grid.setColumnStretch(2, 1)
    self.setLayout(self.grid)
    # update
    self.update()

  def update(self):
    # Load available module names, add to list
    profiles = self.roastClient.profiles
    self.model.clear()
    for i,p in enumerate(profiles):
      item = QStandardItem()
      item.setText('Profile %d' % i)
      item.setEditable(False)
      self.model.appendRow(item)
    self.view.pressed.connect(self.clickItem)
    self.selectedProfile = profiles[0]
    self.btnPlotColor.setStyleSheet("QWidget { background-color: %s }" % self.selectedProfile.qcolor.name())

  def clickItem(self, itemindex):
    self.selectedProfile = self.roastClient.profiles[itemindex.row()]
    self.btnPlotColor.setStyleSheet("QWidget { background-color: %s }" % self.selectedProfile.qcolor.name())

  def selectPlotColor(self):
    color = QColorDialog.getColor(self.selectedProfile.qcolor)
    if color.isValid():
      self.selectedProfile.qcolor = color
      self.roastClient.repaint()
      self.btnPlotColor.setStyleSheet("QWidget { background-color: %s }" % color.name())
