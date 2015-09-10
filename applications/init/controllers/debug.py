# -*- coding: utf-8 -*-
# try something like
import os, requests, json

def index():
    #xd_admin = getspringxd()
    return dict(message=os.environ)

def getspringxd():
    return json.loads(os.environ['VCAP_SERVICES'])['p-spring-xd'][0]['credentials']['spring-xd-admin-uris'][0]
