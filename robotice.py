#!/usr/bin/env python

"""
Robotice daemon
based on http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
"""

import sys, time

from daemon import Daemon

from sensors.dht import get_dht_data
from outputs.statsd import send_statsd_data

DUMMY_SENSOR = {
    'version': 2302,
    'port': 4
}

class Robotice(Daemon):
    def run(self):
        while True:
            data = get_dht_data(DUMMY_SENSOR)
            send_statsd_data(data)
            time.sleep(2)
            print 'sleeep...'
 
if __name__ == "__main__":
    daemon = Robotice('/tmp/robotice.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
