# external dependencies
import os, os.path, time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from cr.profile import Profile, RoastProfile


windowClass = uic.loadUiType('%s/GUI/MainWindow.ui' % os.path.dirname(os.path.realpath(__file__)))[0]


# Used for spacing GUI elements in the toolbar
class Spacer(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 


# Main roast profiling window
class MainWindow(QMainWindow, windowClass):
  def __init__(self, settings):
    QMainWindow.__init__(self)
    self.settings = settings
    self.devices = []
    self.reference = None
    self.roastProfile = RoastProfile()
    self.setupUi(self)
    # setup
    self.dockDevices.listDevices = self.listDevices;
    self.dockDevices.setup(self)
    self.dockProfiles.listProfiles = self.listProfiles;
    self.dockProfiles.setup(self)
    self.dockReferences.listReferences = self.listReferences;
    self.dockReferences.setup(self)
    self.graphT.setup(self)
    self.graphDT.setup(self)
    # connect signals
    self.buttonDevices.clicked.connect(self.toggleDevices)
    self.buttonProfiles.clicked.connect(self.toggleProfiles)
    self.buttonConnection.toggled.connect(self.toggleConnect)
    self.buttonRoasting.toggled.connect(self.toggleRoasting)
    self.button1C.toggled.connect(self.toggle1C)
    self.buttonComment.clicked.connect(self.recordComment)
    # start timer
    self.t = 0.
    self.timerClock = QTimer()
    self.timerClock.timeout.connect(self.updateTime)
    self.timerClock.start(1000)
    self.timerStart = time.time()
    self.roasting = False

  def closeEvent(self, e):
    for d in self.devices:
      d.stop()

  def toggleDevices(self):
    if self.dockDevices.isVisible(): self.dockDevices.hide()
    else: self.dockDevices.show()

  def toggleProfiles(self):
    if self.dockProfiles.isVisible(): self.dockProfiles.hide()
    else: self.dockProfiles.show()

  def toggleConnect(self):
    ret = False
    if self.buttonConnection.isChecked():
      for dev in self.devices:
        r = dev.connect()
        if r == True: ret = True
      if not ret:
        self.buttonConnection.setChecked(False)
      else:
        self.buttonRoasting.setEnabled(True)
    else:
      for dev in self.devices:
        dev.stop()
      self.buttonRoasting.setEnabled(False)
      self.buttonRoasting.setChecked(False)

  def toggleRoasting(self):
    if self.buttonRoasting.isChecked():
      self.timerStart = time.time()
      for dev in self.devices:
        for p in dev.profiles:
          p.time = [x-self.t for x in p.time]
      self.t = 0.
      self.button1C.setEnabled(True)
    else:
      self.roastProfile.comments.append([self.t, 'EOR'])
      filename, fltr = QFileDialog.getSaveFileNameAndFilter(parent=self, caption="Save Roast Profile", initialFilter="csv")
      if filename:
        self.save(filename)
      self.button1C.setEnabled(False)

  def toggle1C(self):
    if self.button1C.isChecked():
      self.roastProfile.comments.append([self.t, '1CS'])
    else:
      self.roastProfile.comments.append([self.t, '1CE'])
    self.graphT.update()
    self.graphDT.update()

  def recordComment(self):
    t = self.t
    text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter comment:')
    if ok:
      self.roastProfile.comments.append([t, text])
    self.graphT.update()
    self.graphDT.update()

  def secondsToClock(self, t):
    mnt = int(t / 60)
    sec = t - (mnt*60)
    if mnt < 10: smnt = '0%d' % mnt
    else: smnt = '%d' % mnt
    if sec < 10: ssec = '0%d' % sec
    else: ssec = '%d' % sec
    return '%s:%s' % (smnt, ssec)

  def updateTime(self):
    timeNow = time.time()
    timeElapsed = round(timeNow - self.timerStart)
    self.t = timeElapsed
    self.labelTime.setText(self.secondsToClock(self.t))
    stemp = ''
    for dev in self.devices:
      for p in dev.profiles:
        try:
          stemp += '%s: %.1f°C\t' % (p.label, p.temp[-1])
        except IndexError:
          pass
    self.labelTemp.setText(stemp)

  def loadDevice(self, name):
    mod = __import__(name, fromlist=['*'])
    cls = getattr(mod, name)
    gui = uic.loadUiType('%s/drivers/%s.ui' % (os.path.dirname(os.path.realpath(__file__)), name))[0]
    drv = cls(self, gui)
    self.devices.append(drv)

  def save(self, filename):
    fd = open(filename, 'w')
    for c in self.roastProfile.comments:
      fd.write('#%d, %s\n' % (c[0], c[1]))
    for p in self.roastProfile.profiles:
      for i in range(len(p.time)):
        fd.write('%d, %f\n' % (p.time[i], p.temp[i]))
    fd.close()
    
