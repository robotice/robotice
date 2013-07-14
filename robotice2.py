import logging
import yaml
from daemonize import Daemonize
from time import sleep

from simple_monitor import send_data_all

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

name = config.get("name")

pid = "/tmp/robotice.pid"

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)
logger.propagate = False

fh = logging.FileHandler("/tmp/robotice.log", "w")
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]

statsd_connection = statsd.Connection(
    host='master2.htfs.info',
    port=8125 ,
    sample_rate=1,
    disabled = False
)

sender = statsd.Gauge('MyApplication', statsd_connection)

def main():
    while True:
        print "ahoj"
        logger.debug("test")
        send_data_all(conf, sender)
        sleep(2)
        print "ahoj2"

daemon = Daemonize(app="robotice", pid=pid, action=main, keep_fds=keep_fds) 
daemon.start()
