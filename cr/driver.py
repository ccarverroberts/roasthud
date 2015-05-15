import threading


class Driver:
  def __init__(self, roastClient, configClass):
    self.roastClient = roastClient
    self.thread = None
    self.done = False

  def stop(self):
    self.done = True
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
    pass

  def disconnect(self):
    pass
