import logging
import yaml
import statsd

from time import sleep

from simple_monitor import send_data_all

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

print config


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

sender = statsd.Raw('robotice_prod.%s' % config.get('name').replace('.', '_'), statsd_connection)

send_data_all(config, sender)
