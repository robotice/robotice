#!/usr/bin/python

import random

def get_data(sensor):
    """
    Just get some random data
    """

    data = []

    data.append(("%s.%s.random1" % (sensor.get('device'), sensor.get('name')), random.randint(10, 20),))
    data.append(("%s.%s.random2" % (sensor.get('device'), sensor.get('name')), random.randint(10, 20),))

    return data
