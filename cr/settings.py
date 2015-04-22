
import os, sys


class Settings:
  def __init__(self, qapp):
    sdir = self.settingsLocation('cleanroast')
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
