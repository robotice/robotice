"""
raven.contrib.celery
~~~~~~~~~~~~~~~~~~~~

>>> class CeleryClient(CeleryMixin, Client):
>>>     def send_encoded(self, *args, **kwargs):
>>>         "Errors through celery"
>>>         self.send_raw.delay(*args, **kwargs)

>>> @task(routing_key='sentry')
>>> def send_raw(*args, **kwargs):
>>>     return super(client, self).send_encoded(*args, **kwargs)

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import logging
from celery.signals import after_setup_logger, task_failure

LOG = logging.getLogger(__name__)

"""register_signal and register_logger_signal if RAVEN DSN is specified in main conf
   and raven lib is installed
"""

RAVEN = False

try:
    from conf import DSN
    RAVEN = True
except Exception, e:
    pass

if DSN:
    try:
        from raven.handlers.logging import SentryHandler
        from raven import Client
    except ImportError, e:
        raise Exception(
            "You have set DSN, but missing raven lib - maybe pip install raven will fix this issue")

try:

    client = Client(DSN)

    register_signal(client)
    register_logger_signal(client)

except Exception, e:
    client = None
    raise e


class CeleryFilter(logging.Filter):

    def filter(self, record):
        # Context is fixed in Celery 3.x so use internal flag instead
        extra_data = getattr(record, 'data', {})
        if not isinstance(extra_data, dict):
            return record.funcName != '_log_error'
        # Fallback to funcName for Celery 2.5
        return extra_data.get('internal', record.funcName != '_log_error')


def register_signal(client):
    def process_failure_signal(sender, task_id, args, kwargs, **kw):
        # This signal is fired inside the stack so let raven do its magic
        client.captureException(
            extra={
                'task_id': task_id,
                'task': sender,
                'args': args,
                'kwargs': kwargs,
            })

    task_failure.connect(process_failure_signal, weak=False)


def register_logger_signal(client, logger=None):
    filter_ = CeleryFilter()

    if logger is None:
        logger = logging.getLogger()
        handler = SentryHandler(client)
        handler.setLevel(logging.ERROR)
        handler.addFilter(filter_)

    def process_logger_event(sender, logger, loglevel, logfile, format,
                             colorize, **kw):
        # Attempt to find an existing SentryHandler, and if it exists ensure
        # that the CeleryFilter is installed.
        # If one is found, we do not attempt to install another one.
        for h in logger.handlers:
            if type(h) == SentryHandler:
                h.addFilter(filter_)
                return False

        logger.addHandler(handler)

    after_setup_logger.connect(process_logger_event, weak=False)
