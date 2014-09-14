# -*- coding: utf-8 -*-

import errno
from functools import wraps
import logging
import os
import signal
import tempfile

from robotice.conf import Settings, setup_app

logger = logging.getLogger(__name__)


class dotdict(dict):

    """ Dictionary with dot access """

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class RoboticeAPI(Settings):

    """
        API for comunication with Robotice

        this class expose all robotice.conf methods
    """

    def __init__(self, worker="reasoner", conf_dir="/srv/robotice/config",
                 worker_dir="/srv/robotice", *args, **kwargs):

        self.conf_dir = os.getenv("R_CONFIG_DIR", conf_dir)
        self.worker_dir = os.getenv("R_WORKER_DIR", worker_dir)

        if worker:
            self.setup_app(worker)

    def ping(self):
        return "pong"