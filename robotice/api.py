# -*- coding: utf-8 -*-

import logging
import Pyro4
from time import sleep

try:
    from robotice.conf.api import URI_PORT, URI_ID, HMAC_KEY, SERVER_IP
    from robotice.conf import RoboticeSettings
except Exception, e:
    raise e

################################################################################

Pyro4.config.HMAC_KEY = HMAC_KEY

################################################################################

"""
    start API
"""

LOOP_LIMIT = 30

def handle_noargs(*args, **kwargs):
    logger = logging.getLogger("robitce.api")

    
    print "START COMMAND"

    from robotice.api import RoboticeAPI

    i = 0

    daemon = None
    while i < LOOP_LIMIT:
        try:
            # try to connect to address (port/ip)
            daemon = Pyro4.Daemon(port=URI_PORT, host=SERVER_IP)
        except Exception, e:
            print(str({
                "error": e,
                "loop": "%s/%s" % (i, LOOP_LIMIT)
            }))
            i += 1
            sleep(3)

        if daemon:
            break

    if not daemon:
        logger.critical("Pyro connection has not been created!")
        return

    # Pyro4.socketutil.setReuseAddr(daemon.sock)
    uri = daemon.register(RoboticeAPI(), URI_ID)
    logger.info("Success connected to Pyro NameServer %s" % uri)
    try:
        daemon.requestLoop()
    finally:
        daemon.shutdown()

if __name__ == "__main__":

    handle_noargs()