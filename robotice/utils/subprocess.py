
from __future__ import absolute_import

import logging

from subprocess import Popen, PIPE

logger = logging.getLogger(__name__)

def call_command(cmd, verbosity="ERROR"):
  """
  simple wrapper for call command
  """

  p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)

  output, err = p.communicate("get output")

  rc = p.returncode

  if not rc == 0:
    raise Exception("{0} ==> command: {1}".format(err, " ".join(cmd)))

  return output