import threading
from cr.profile import Profile


class Driver:
  def __init__(self, roastClient, configClass):
    self.roastClient = roastClient
    self.thread = None
    self.done = False
    self.profiles = []
    self.connected = False

  def stop(self):
    self.done = True
    if self.thread != None:
      self.thread.join()
    self.disconnect()
    self.thread = None

  def main(self):
    pass

  def loop(self):
    self.thread = threading.Thread(target=self._loop)
    self.thread.start()

  def _loop(self):
    while not self.done:
      self.main()

  def connect(self):
    return False

  def disconnect(self):
    pass
