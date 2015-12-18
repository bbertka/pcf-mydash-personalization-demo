# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('myDash'), _class="navbar-brand",_href="/", _id="web2py-logo")

response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

app = request.application
ctr = request.controller

if not session.SCREENNAME:
    screenname = 'Login'
    response.menu = [
        (T('About'), False, URL('init', 'about', 'index'), [])
    ]
    response.menu1 = [
     (T(screenname), False, '#', [
               (T('Help'), False, URL('init', 'help', 'index')),
               LI(_class="divider"),
                [CAT(I(_class='glyphicon glyphicon-log-in'), T(' Login')), False, URL('init', 'default', 'login')]
            ]) ]
else:
    screenname = session.SCREENNAME
    response.menu = [
        [CAT(I(_class='glyphicon glyphicon-home'),T(' Home')), False, URL('default', 'index')],
        [CAT(I(_class='fa  fa-search'),T(' Search')), False, URL('init', 'search', 'index')],
        [CAT(I(_class='fa  fa-twitter'),T(' Stream')), False, URL('init', 'twitterbot', 'index')],
       [CAT(I(_class='fa fa-lightbulb-o'),T(' Discover')), False, URL('init', 'recommended', 'index')],

    ]
    response.menu1 = [
    (CAT(IMG(_src=session.IMAGE, _class='size32'), " ", session.SCREENNAME), False, '#', [
               (T('About'), False, URL('init', 'about', 'index')),
               LI(_class="divider"),
            #  (T('Profile'), False, URL('init', 'profile', 'index')),
            # LI(_class="divider"),
                [CAT(I(_class='glyphicon glyphicon-log-out'), T(' Logout')), False, URL('init', 'default', 'logout')],

              ]) ]

if "auth" in locals(): auth.wikimenu()
