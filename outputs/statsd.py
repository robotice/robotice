#!/usr/bin/python

DEMO_STATSD = {
    'HOST': 'master2.htfs.info',
    'PORT': 8125
}

def send_statsd_data(data):
    """
    Send all metrics to statsd server
    """
    for datum in data:
        pass