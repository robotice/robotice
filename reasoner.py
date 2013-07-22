
import logging
import yaml
import statsd

from daemonize import Daemonize
from time import sleep

from celery.execute import send_task

from tasks.monitor import get_data

pid = "/tmp/robotice.pid"

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)
logger.propagate = False

fh = logging.FileHandler("/tmp/robotice.log", "w")
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def main():

    config_file = open("/srv/robotice/config.yml", "r")
    config = yaml.load(config_file)

    logger.debug(config)

    statsd_connection = statsd.Connection(
        host='master2.htfs.info',
        port=8125,
        sample_rate=1,
        disabled = False
    )
    sender = statsd.Gauge('robotice_prod.%s' % config.get('name').replace('.', '_'), statsd_connection)

    logger.debug(sender)

    sensor = {}

    while True:

		result = get_data.apply_async(sensor)
		print result.get()
#		result = send_task('task.add', [3, 3])
#		print result.get()
#		result = add.delay(4, 4)

        sleep(2)



#daemon = Daemonize(app="robotice", pid=pid, action=main, keep_fds=keep_fds) 
#daemon.start()