# -*- coding: utf-8 -*-

SERVER_IP = "10.10.10.122"
HMAC_KEY = "d2d00896183011e28eb950e5493b2d90"
URI_ID = "24142d22-1f57-11e2-9012-50e5493b2d90"
URI_PORT = 33333

try:
    from settings_local import *
except ImportError:
    pass