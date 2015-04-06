#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.1.13', 5850))
while 1:
  data = s.recv(1024)
  if data != b'':
    print(float(data))
s.close()

