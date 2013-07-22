from yaml import load
from time import sleep

from celery.execute import send_task

from tasks.planner import get_model
from tasks.monitor import get_data

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

sensor = {}

result = get_model.apply_async(sensor)
print result.get()
#		result = send_task('task.add', [3, 3])
#		print result.get()
#		result = add.delay(4, 4)


#daemon = Daemonize(app="robotice", pid=pid, action=main, keep_fds=keep_fds) 
#daemon.start()
