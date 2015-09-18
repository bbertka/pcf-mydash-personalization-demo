# -*- coding: utf-8 -*-
# try something like
import os, json, sys
import myglobals
import requests


def index():
    if not session.SCREENNAME:
        redirect('/')
    if not session.TRACK:
        redirect('/')
    sentiment = "http://ltc-%s.%s/sentiment.html" % (session.SCREENNAME, myglobals.DIEGO_RECEPTOR )
    bubbles = "http://ltc-%s.%s/bubbles.html" % (session.SCREENNAME, myglobals.DIEGO_RECEPTOR )
    response.title = "Stream"

    if not session.BOT:
        createBot()
        session.BOT = showBot()
    return dict(message = session.BOT,bubbles=bubbles, sentiment=sentiment )


def showBot():
    headers = {'Authorization':'Basic YmJlcnRrYTprYXJtYTE5NzY='}
    r = requests.get("http://receptor.%s/v1/desired_lrps/ltc-%s"% ( myglobals.DIEGO_RECEPTOR, session.SCREENNAME.lower() ), headers=headers)
    return dict(message=r.content)

def createBot():
    if not session.SCREENNAME:
        redirect('/')
    query= {
        "metrics_guid": "ltc-%s" % session.SCREENNAME.lower(), 
        "domain": "lattice", 
        "disk_mb": 0, 
        "monitor": {
            "run": {
                "path": "/tmp/healthcheck", 
                "args": [
                    "-timeout", 
                    "1s", 
                    "-port", 
                    "8080"
                ], 
                "resource_limits": {}, 
                "user": "vcap", 
                "log_source": "HEALTH"
            }
        }, 
        "start_timeout": 0, 
        "setup": {
            "download": {
                "to": "/tmp", 
                "cache_key": "", 
                "from": "http://file_server.service.dc1.consul:8080/v1/static/healthcheck.tgz", 
                "user": "vcap"
            }
        }, 
        "log_source": "APP", 
        "routes": {
            "cf-router": [
                {
                    "hostnames": [
                        "ltc-%s.%s" % (session.SCREENNAME.lower(), myglobals.DIEGO_RECEPTOR ), 
                        "ltc-%s-8080.%s" % (session.SCREENNAME.lower(), myglobals.DIEGO_RECEPTOR )
                    ], 
                    "port": 8080
                }
            ]
        }, 
        "log_guid": "ltc-%s" % session.SCREENNAME.lower(), 
        "ports": [
            8080
        ], 
        "memory_mb": 128, 
        "instances": 1, 
        "cpu_weight": 100, 
        "env": [
            {
                "name": "HOME", 
                "value": "/"
            }, 
            {
                "name": "APP_KEY", 
                "value": "%s" % myglobals.APP_KEY
            }, 
            {
                "name": "APP_SECRET", 
                "value": "%s" % myglobals.APP_SECRET
            }, 
            {
                "name": "OAUTH_TOKEN_SECRET",
                "value": "%s" % session.USER_OAUTH_TOKEN_SECRET
            }, 
            {
                "name": "MAX_CHART_SIZE",
                "value": "500"
            }, 
            {
                "name": "INCLUDE_TWITTER_HASH", 
                "value": "%s" % ','.join(session.TRACK)
            }, 
            {
                "name": "PROCESS_GUID", 
                "value": "ltc-%s" % session.SCREENNAME.lower()
            }, 
            {
                "name": "PATH", 
                "value": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            }, 
            {
                "name": "OAUTH_TOKEN", 
                "value": "%s" % session.USER_OAUTH_TOKEN
            }, 
            {
                "name": "VCAP_APP_PORT", 
                "value": "8080"
            }, 
            {
                "name": "PORT", 
                "value": "8080"
            }
        ], 
        "action": {
            "run": {
                "path": "/bin/sh", 
                "args": [
                    "-c", 
                    "python -u bot.py"
                ], 
                "resource_limits": {}, 
                "user": "vcap", 
                "dir": "/ltc-twitter-sentiment-demo"
            }
        }, 
        "process_guid": "ltc-%s" % session.SCREENNAME.lower(), 
        "rootfs": "docker:///bbertka/ltc-twitter-sentiment-demo-img#latest"
    }
    headers = {'Authorization':'Basic YmJlcnRrYTprYXJtYTE5NzY='}
    r = requests.post("http://receptor.%s/v1/desired_lrps" % myglobals.DIEGO_RECEPTOR, data=json.dumps(query), headers=headers)
    return r.content
