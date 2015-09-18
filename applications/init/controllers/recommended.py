# -*- coding: utf-8 -*-
# try something like
from bs4 import BeautifulSoup
import requests
import json

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def index():
    response.title = 'Discover'
    if not session.NEWS:
        session.NEWS = news()
    form = display_form()
    return dict(message=session.NEWS, form=form)


def display_form():
    form = SQLFORM(db.news, formstyle='table3cols', buttons = [TAG.button('Re-calculate',_type="submit", _class="btn btn-success btn-default")])
    if form.process().accepted:
        session.NEWS = news()
        redirect('/discover')
    elif form.errors:
        response.flash = 'Form has Errors'
    else:
        pass
    return form


def news():
    stories = []
    for subject, count in session.TOP20:
        hits = query(subject)
        if hits:
            for hit in hits:
                stories.append(hit)
    return stories


def query(subject):
        url = "http://hn.algolia.com/api/v1/search_by_date?query=%s" % subject
        hits = []
        try:
                r = requests.get(url, headers=HEADER)
                for hit in r.json()['hits']:
                    try:
                        title, link = hit['title'], hit['url']
                        if title and link:
                            link = A(B(title),_class='user-homepage-link', _href=link)
                            hits.append( (hit['created_at'].split('T')[0], link, hit['_highlightResult']['url']['matchedWords']) )
                    except Exception as e:
                        continue
        except Exception as e:
                hits = None
        return hits
