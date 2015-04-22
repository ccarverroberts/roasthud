# external dependencies
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DeviceListPage(QWizardPage):
  def __init__(self):
    super(DeviceListPage, self).__init__()
    self.setTitle("Select Device Driver")
    self.setSubTitle("Please select the device driver that matches your device.")


class DeviceWizard(QWizard):
  def __init__(self):
    super(DeviceWizard, self).__init__()
    pageIntro = QWizardPage()
    pageIntro.setTitle("Add Temperature Device")
    self.addPage(pageIntro)
    pageDeviceList = DeviceListPage()
    self.addPage(pageDeviceList)
