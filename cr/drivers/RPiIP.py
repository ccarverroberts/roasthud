from cr.driver import Driver as BaseDriver
from cr.profile import Profile, RoastProfile
from PyQt4.QtGui import QDialog
import socket


class RPiIP(BaseDriver):
  def __init__(self, roastClient, configClass):
    BaseDriver.__init__(self, roastClient, configClass)
    self.roastClient = roastClient
    self.IPaddress = '0.0.0.0'
    self.IPport = 5850
    self.configForm = QDialog()
    self.configForm.setModal(True)
    self.configUI = configClass()
    self.configUI.setupUi(self.configForm)
    self.configUI.buttonOK.clicked.connect(self.updateConfig)
    self.configUI.buttonCancel.clicked.connect(lambda e: self.configForm.hide())
    self.configForm.show()
    # register 1 profile (only 1 temperature sensor supported for now)
    p = self.roastClient.roastProfile.createProfile()
    self.profiles.append(p)
    self.roastClient.dockProfiles.visibilityToggled(True)
    

  def connect(self):
    print('Attempting connection to', self.IPaddress, ':', self.IPport)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(5)
    try:
      self.sock.connect((self.IPaddress, int(self.IPport)))
      self.loop()
      self.connected = True
    except (OSError, socket.timeout, socket.error) as e:
      print('Cannot connect to %s:%s. %s.' % (self.IPaddress, self.IPport, e))
      return False
    return True

  def disconnect(self):
    if self.connected:
      self.sock.shutdown(socket.SHUT_RD)
      self.sock.close()
      self.sock = None
      self.connected = False

  def main(self):
    datab = self.sock.recv(64)
    data = datab.decode("utf-8")
    if data != '':
      try:
        aT = float(data)
        self.profiles[0].setT(self.roastClient.t, aT)
        self.roastClient.graphT.update()
        self.roastClient.graphDT.update()
      except ValueError:
        pass

  def showConfig(self):
    self.configForm.show()

  def updateConfig(self, e):
    self.IPaddress = self.configUI.textIP.text()
    self.IPport = self.configUI.textPort.text()
    self.configForm.hide()


