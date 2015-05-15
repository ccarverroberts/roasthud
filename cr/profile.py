from PyQt4.QtGui import QColor


class Profile:
  def __init__(self, label='Active'):
    self.label = label
    self.time = []
    self.temp = []
    self.color = QColor(0, 0, 0)
