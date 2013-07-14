import logging
from daemonize import Daemonize
from time import sleep

pid = "/tmp/robtice.pid"
logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/tmp/robotice.log", "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

def main():
    while True:
        print "ahoj"
        logger.debug("test")
        sleep(2)
        print "ahoj2"

daemon = Daemonize(app="robotice", pid=pid, action=main,keep_fds=keep_fds) 
daemon.start()
