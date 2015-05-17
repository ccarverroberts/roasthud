from PyQt4.QtGui import QColor, QPen
from cr.settings import Bunch


class Profile:
  def __init__(self, label='T', filename=None):
    self.label = label
    self.time = []
    self.temp = []
    self.ror = []
    self.thickness = 2.0
    self.color = QColor(0, 0, 0)
    self.pen = QPen(self.color, self.thickness)

  def setT(self, t, T):
    self.time.append(t)
    self.temp.append(T)
    self.calculateDelta(istart=len(self.time)-1)

  def setColor(self, color):
    self.color = color
    self.pen = QPen(self.color, self.thickness)

  def setThickness(self, thick):
    self.thickness = thick
    self.pen = QPen(self.color, self.thickness)

  def calculateDelta(self, istart=0):
    y = self.temp
    # Construct dT
    for i in range(int(istart), len(self.temp)):
      if i > 1:
        dy = 0.
        ndy = 0
        r = 0 if len(y) < 10 else i-10
        for j in reversed(range(r, i-1)):
          if y[j] != y[i]:
            dy += 60.*(y[i]-y[j])/(self.time[i]-self.time[j])
            ndy += 1
        if ndy == 0: dy = 0.
        else: dy /= ndy
        self.ror.append(dy)
      else:
        self.ror.append(0.)


class RoastProfile:
  def __init__(self, filename=None):
    self.profiles = []
    self.comments = []
    if filename:
      Nplots = -1
      for line in open(filename, 'r'):
        sp = line.split(',')
        x = sp[0]
        if x.startswith('#'):
          x = x[1:]
          self.comments.append([x, ','.join([s.strip() for s in sp[1:]])])
        else:
          if Nplots < 0:
            Nplots = len(sp) - 1
            for i in range(Nplots): self.createProfile()
          for i in range(Nplots): 
            y = sp[i+1]
            self.profiles[i].time.append(int(x))
            self.profiles[i].temp.append(float(y))
      for p in self.profiles:
        p.calculateDelta()
      

  def createProfile(self):
    p = Profile(label=str('T%d' % (len(self.profiles)+1)))
    self.profiles.append(p)
    return p
