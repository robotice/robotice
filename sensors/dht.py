#!/usr/bin/python

import subprocess
import re
import sys

executable = "/srv/robotice/sensors/Adafruit_DHT"

def get_dht_data(sensor):
    """
    Run the DHT program to get the humidity and temperature readings!
    """
    device = sensor.get('device'), 0)
    version = sensor.get('version')
    port = sensor.get('port'))

    output = subprocess.check_output([executable, str(version), str(port)]);

    matches = re.search("Temp =\s+([0-9.]+)", output)
    if (not matches):
       temp = None
    else:
        temp = float(matches.group(1))

    matches = re.search("Hum =\s+([0-9.]+)", output)
    if (not matches):
        humidity = None
    else:
        humidity = float(matches.group(1))

    if temp == None or humidity == None:
        values = [
            ['dht.%s.temperature' % device, None],
            ['dht.%s.humidity' % device, None]
        ]
    else:
        values = [
            ['dht.%s.temperature' % device, temp],
            ['dht.%s.humidity' % device, humidity]
        ]
    return values
