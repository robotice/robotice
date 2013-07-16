#!/usr/bin/python
import subprocess
import re
import sys
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = "/usr/local/bin/sispmctl"

def set_socket(device=None, value, socket):
  """
  @device 0,1 if none default 0
  @value = o/f
  @socket 0,1..
  return True if status changed False and None if error
  """
  if value == None or socket == None:
    return None

  if device == None:
    local_device = 0
  else:
    local_device = device

  try:
    output = subprocess.check_output([executable,"-n","-d", local_device , value, socket]);
  except Exception, e:
    return None

  lines = output.split("\n")
  timestamp = int(time.time())
  i = 0
  for line in lines:
    if i != 0:
      status = line.split("%s" %socket)
      if len(status) > 1:
        if status[1] != value:
          return True
        elif: status[1] == value:
          return False #nothing changed or log
        else:
          return None # exception
    i += 1