import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Bunch(dict):
  def __init__(self, **kwds):
    dict.__init__(self, kwds)
    self.__dict__ = self


class Settings:
  def __init__(self, qapp):
    self.axes = Bunch()
    self.axes.colorFont = QColor(0, 0, 0)
    self.axes.penTick = QPen(QColor(5, 5, 5), 2.0)
    self.axes.tickSize = 10.
    self.axes.size = 40.
    self.axes.rangeX = [0, 15.*60., 60, 30]
    self.axes.rangeY = [0, 250., 20., 10.]
    self.axes.rangeDY = [0, 50., 10., 5.]
    self.grid = Bunch()
    self.grid.major = True
    self.grid.minor = True
    self.grid.colorMajor = QColor(200, 200, 200)
    self.grid.colorMinor = QColor(220, 220, 220)
    self.plots = Bunch()
    self.plots.colorBackground = QColor(240, 240, 240)
    

  def load(self):
    sdir = self.settingsLocation('roasthud')
    sfn = '%s/settings' % sdir
    if os.path.isdir(sdir):
      if os.path.exists(sfn):
        for line in open(sfn, 'r'):
          print('SETTINGS:', line)
    else:
      pass
      #os.mkdir(sdir)
      #fd = open(sfn, 'w')
      #fd.write('')
      #fd.close()

  def settingsLocation(self, appname):
    if sys.platform == 'darwin':
      from AppKit import NSSearchPathForDirectoriesInDomains
      location = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], appname)
    elif sys.platform == 'win32':
      location = os.path.join(os.environ['APPDATA'], appname)
    else:
      location = os.path.expanduser(os.path.join("~", "." + appname))
    return location
