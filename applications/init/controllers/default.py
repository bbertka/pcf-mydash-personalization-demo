from twython import Twython
import json, os
import requests

import myglobals



# try something like
def index():
    if session.SCREENNAME:
        redirect('/dashboard')
    #session.clear()
    response.title = 'myDash'
    response.subtitle = 'Personalized Analytics'
    #form, tauth = display_form()
    form, tauth = twitter_button()
    return dict(form=form, message="Welcome!", tauth=tauth)

def twitter_button():
    #session.clear()
    form=FORM(TABLE(TR("",INPUT(_type="submit",_class="btn-twitter", _value=""))))
    tauth = None
    if form.process().accepted:
        tauth = get_api_keys(form.vars.screenname, form.vars.password)
        redirect(tauth['auth_url'])
    elif form.errors:
        response.flash = 'Form has Errors'
    else:
        pass
    return form, tauth


def display_form():
    form = SQLFORM(db.twitter, formstyle='table3cols', buttons = [TAG.button('Submit',_type="submit", _class="btn btn-success btn-default")])
    tauth = None
    if form.process().accepted:
        session.SCREENNAME = form.vars.screenname
        tauth = get_api_keys(form.vars.screenname, form.vars.password)
        redirect(tauth['auth_url'])
    elif form.errors:
        response.flash = 'Form has Errors'
    else:
        pass
    return form, tauth

def get_api_keys(screenname, password):
    twitter = Twython(myglobals.APP_KEY, myglobals.APP_SECRET)
    tauth = twitter.get_authentication_tokens(callback_url=('http://%s/login' % myglobals.APP_URI) )
    session.OAUTH_TOKEN = tauth['oauth_token']
    session.OAUTH_TOKEN_SECRET = tauth['oauth_token_secret']
    return tauth

def login():
    if session.SCREENNAME:
        redirect('/dashboard')
    try:
        response.title = 'Dashboard'
        oauth_verifier = request.vars['oauth_verifier']
        twitter = Twython(myglobals.APP_KEY, myglobals.APP_SECRET, session.OAUTH_TOKEN, session.OAUTH_TOKEN_SECRET)
        tokens = twitter.get_authorized_tokens(oauth_verifier)
        session.USER_OAUTH_TOKEN = tokens['oauth_token']
        session.USER_OAUTH_TOKEN_SECRET = tokens['oauth_token_secret']
        session.SCREENNAME = tokens['screen_name']
        twitter = Twython(myglobals.APP_KEY, myglobals.APP_SECRET, session.USER_OAUTH_TOKEN, session.USER_OAUTH_TOKEN_SECRET)
        #timeline = twitter.get_home_timeline()
        session.PROFILE = twitter.show_user(screen_name=session.SCREENNAME)
        session.IMAGE = session.PROFILE['profile_image_url']
        session.JSON = tokens
        follow_user()

        redirect('/')
    except Exception as e:
        redirect('/')


def follow_user():
    t = Twython(myglobals.APP_KEY, myglobals.APP_SECRET, myglobals.ACCESS_TOKEN, myglobals.ACCESS_TOKEN_SECRET)
    t.create_friendship(screen_name=session.SCREENNAME)


def logout():
    #deleteBot()
    session.clear()
    redirect('/')

def user():
    return dict(form=auth())

def deleteBot():
    headers = {'Authorization':'Basic YmJlcnRrYTprYXJtYTE5NzY='}
    r = requests.delete("http://receptor.%s/v1/desired_lrps/ltc-%s" % (myglobals.DIEGO_RECEPTOR, session.SCREENNAME.lower() ), headers=headers)
    return dict(message=r.content)
