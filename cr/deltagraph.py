from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DeltaGraph(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.colorBackground = QColor(240., 240., 240.)

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.fillRect(0, 0, self.width(), self.height(), self.colorBackground)
