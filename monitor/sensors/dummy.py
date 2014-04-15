#!/usr/bin/python

import random

def get_data(sensor):
    """
    Just get some random data
    """

    data = []

    data.append(("dummy.%s.random_1" % sensor.get('device'), random.randint(10, 20),))
    data.append(("dummy.%s.random_2" % sensor.get('device'), random.randint(10, 20),))

    return data
