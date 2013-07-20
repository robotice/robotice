import yaml

import statsd

import time

from sispm import run_action

actuator = {
    'type': 'sispm',
    'device': 0,
    'socket': 1
}

print actuator

run_action(actuator, 1)

time.sleep(2)

run_action(actuator, 1)
