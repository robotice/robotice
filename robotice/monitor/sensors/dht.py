#!/usr/bin/python

import subprocess
import re
import sys

executable = "/srv/robotice/sensors/Adafruit_DHT"

def get_data(sensor):
    """
    Run the DHT program to get the humidity and temperature readings!
    """
    device = sensor.get('device', 0)
    type = sensor.get('type')
    port = sensor.get('port')

    output = subprocess.check_output([executable, str(type), str(port)])

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
            ('%s.temperature' % sensor.get("name"), None,),
            ('%s.humidity' % sensor.get("name"), None,)
        ]
    else:
        values = [
            ('%s.temperature' % sensor.get("name"), temp, ),
            ('%s.humidity' % sensor.get("name"), humidity, )
        ]
    return values
