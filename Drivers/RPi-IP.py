from BaseDriver import BaseDriver
import socket, time



class Driver(BaseDriver):
  def __init__(self, roastClient):
    BaseDriver.__init__(self, roastClient)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.IPaddress = '0.0.0.0'
    self.IPport = 5850

  def connect(self):
    print('Attempting connection to', self.IPaddress, ':', self.IPport)
    self.sock.settimeout(5)
    try:
      self.sock.connect((self.IPaddress, self.IPport))
      self.roastClient.connectEvent()
    except (OSError, socket.timeout, socket.error):
      print('Cannot connect to %s:%s.' % (self.IPaddress, self.IPport))
      self.roastClient.disconnectEvent()
      return

  def disconnect(self):
    self.sock.close()

  def main(self):
    datab = self.sock.recv(64)
    data = datab.decode("utf-8")
    if data != '':
      try:
        aT = float(data)
        self.roastClient.dataQueue.put(aT)
      except ValueError:
        pass



