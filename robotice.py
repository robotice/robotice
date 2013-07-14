import logging
from daemonize import Daemonize
from time import sleep
from simple_monitor import send_data_all

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

name = config.get("name")

pid = "/tmp/%s.pid" %name
logger = logging.getLogger("%s" %name)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler("/tmp/%s.log" %name, "w")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

def main():
    while True:
        print "ahoj"
        logger.debug("test")
        #send_data_all(logger,conf,sender)
        sleep(2)
        print "ahoj2"

daemon = Daemonize(app="%s" %name, pid=pid, action=main,keep_fds=keep_fds) 
daemon.start()
