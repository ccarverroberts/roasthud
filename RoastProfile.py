import random
from PyQt4.QtCore import *
from PyQt4.QtGui import *



class RoastProfile:
  def __init__(self, filename=None):
    self.PH       = []
    self.x        = []
    self.y        = []
    self.dy       = []
    self.comments = []
    self.qcolor   = QColor(40, 40, 40)
    if filename == None:
      pass
    else:
      self.readProfile(filename)

  def append(self, X, Y):
    self.x.append(X)
    self.y.append(Y)
    self.calculateDelta(istart=len(self.x)-1)

  def readProfile(self, filename):
    for line in open(filename, 'r'):
      if line.startswith('#'):
        # COMMENT and COLOR directives
        sp = line.strip().split(' ')
        if sp[0] == '#COLOR': self.qcolor = QColor(int(sp[1]), int(sp[2]), int(sp[3]))
        if sp[0] == '#COMMENT':
          self.comments.append([int(sp[1]), float(sp[2]), str.join(' ', sp[3:])])
        if sp[0] == '#EVENT:':
          c = [int(sp[2]), float(sp[3]), None]
          if sp[1] == 'FCS:': c[2] = 'FCS'
          elif sp[1] == 'EOR:': continue
          else: c[2] = str.join(' ', sp[4:])
          self.comments.append(c)
      else:
        # time, Temp data
        sp = line.split(', ')
        self.x.append(int(sp[0]))
        self.y.append(float(sp[1]))
    self.calculateDelta()

  def writeProfile(self, filename):
    fd = open(filename, 'w')
    fd.write('#COLOR %d %d %d\n' % (self.qcolor.red(), self.qcolor.green(), self.qcolor.blue()))
    for c in self.comments:
      fd.write('#COMMENT %d %f %s\n' % (c[0], c[1], c[2]))
    for i in range(len(self.x)):
      fd.write('%d, %f\n' % (self.x[i], self.y[i]))

  def calculateDelta(self, istart=0):
    y= self.y
    # Construct dT
    for i in range(int(istart), len(self.y)):
      if i > 1:
        dy = 0.
        ndy = 0
        r = 0 if len(self.y) < 10 else i-10
        for j in reversed(range(r, i-1)):
          if y[j] != y[i]:
            dy += 60.*(y[i]-y[j])/(self.x[i]-self.x[j])
            ndy += 1
        if ndy == 0: dy = 0.
        else: dy /= ndy
        self.dy.append(dy)
      else:
        self.dy.append(0.)
