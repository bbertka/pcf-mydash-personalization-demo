#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import os, json


try:
    APP_KEY = os.getenv('APP_KEY')
    APP_SECRET = os.getenv('APP_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    APP_URI =json.loads(os.getenv("VCAP_APPLICATION"))['uris'][0]
    DIEGO_RECEPTOR = os.getenv('DIEGO_RECEPTOR')
except:
    APP_KEY ='N9Eu9N9iUX4MSHu8ryq8krrnH'
    APP_SECRET = 'h5FceeDBpCvDF99FiCyMiaGRefEeZc24pNlyEYG3EAtLNMXEzk'
    ACCESS_TOKEN = '2927712042-kpRDLAz0BEGt9tM6aRZqxdJW5REc1ufLbMTf5Yp'
    ACCESS_TOKEN_SECRET = 'wSZqg9lFSadjfMg6tvCbFD25F9HtqGqf8NpL9RfIuDALf'
    APP_URI = 'devbox'
    DIEGO_RECEPTOR = '52.11.65.152.xip.io'
