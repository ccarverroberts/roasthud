

class Driver:
  def __init__(self, roastClient):
    self.roastClient = roastClient
    self.done = False

  def stop(self):
    self.done = True
    self.disconnect()

  def main(self):
    pass

  def loop(self):
    while not self.done:
      self.main()

  def connect(self):
    pass

  def disconnect(self):
    pass
