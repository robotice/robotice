import yaml

import statsd

from time import sleep

from sispm import run_action

actuator = {
    'type': 'sispm',
    'device': 0,
    'socket': 1
}

print actuator

run_action(actuator, 1)
