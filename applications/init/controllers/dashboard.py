# -*- coding: utf-8 -*-
# try something like

from twython import Twython
import os, json, sys
from collections import Counter
from textblob import TextBlob
import requests
import myglobals


def index():
    if not session.SCREENNAME:
        redirect('/')
    response.title = 'Dashboard'
    tweets = []
    try:
        twitter = Twython(myglobals.APP_KEY, myglobals.APP_SECRET, session.USER_OAUTH_TOKEN, session.USER_OAUTH_TOKEN_SECRET)
        timeline = twitter.get_user_timeline(screen_name=session.SCREENNAME, count=20)
        tweets = []
        for data in timeline:
            created = data['created_at'].split('+')[0].strip().split(' ')
            short = created[0]+'-'+created[1]+'-'+created[2]
            user = "@"+data['user']['screen_name']
            url = ''
            text = data['text']+' '+url
            image = data['user']['profile_image_url']
            if text.split(' @')[0]=='RT':
                user = text.strip('RT').split(':')[0]
                text = text.split(':')[1]
                image = data['retweeted_status']['user']['profile_image_url']
                if data['retweeted_status']['entities']['urls']:
                    url = data['retweeted_status']['entities']['urls'][0]['url']
            session.HOMEPAGE = 'https://twitter.com/%s' % user.split('@')[1]
            userlink = A(B(user),_class='user-homepage-link', _href=session.HOMEPAGE)
            textdiv = DIV(userlink, P(text, _class="tweet-text"), A(_href=url, _class='user-homepage-link'))
            tuple1 = (IMG(_src=image, _class="twitter-timeline-user-image"), textdiv)
            tweet = [ tuple1 ]
            tweets.append(tweet)
    except Exception as e:
            tweets = e

    return dict(message=twitter.show_user(screen_name=session.SCREENNAME), timeline=tweets)


def metrics():
    BUBBLE_STATS = bubblestats()
    twitter = Twython(myglobals.APP_KEY, myglobals.APP_SECRET, session.USER_OAUTH_TOKEN, session.USER_OAUTH_TOKEN_SECRET)
    timeline = twitter.get_user_timeline(screen_name=session.SCREENNAME, count=500)
    hashtags = []
    for data in timeline:
        hashtags = [ tag['text'].encode('utf-8').lower() for tag in data['entities']['hashtags'] ]
        BUBBLE_STATS.update( trends=hashtags )
    url = 'http://0.0.0.0/init/default/metrics'
    return json.dumps({"name":"hashtags","links":[{"rel":"self","href": url}],"counts": BUBBLE_STATS.trend_count })


def sentiment():
    PIE_STATS = piestats()
    twitter = Twython(myglobals.APP_KEY, myglobals.APP_SECRET, session.USER_OAUTH_TOKEN, session.USER_OAUTH_TOKEN_SECRET)
    timeline = twitter.get_user_timeline(screen_name=session.SCREENNAME, count=500)
    for data in timeline:
        value = 'Neutral'
        sentiment = TextBlob(data['text']).sentiment.polarity
        if sentiment < 0:
            value = 'Bad'
        elif sentiment > 0:
            value = 'Good'
        PIE_STATS.update( sentiment=[value] )
    url = 'http://0.0.0.0:/init/default/sentiment'
    return json.dumps({"name":"sentiment","links":[{"rel":"self","href": url}],"counts": PIE_STATS.sentiment_count })

#---------------------------------------------------------------
#
# bubblestats: keeps track of the tag count in the bubble chart
#
#---------------------------------------------------------------
class bubblestats:
        def __init__(self):
                self.trend_raw = []
                self.trend_count = Counter()
        def update(self, trends=[]):
                # this keeps track of the size of the bubble chart
                if len(self.trend_raw) >= 10000:
                        self.trend_raw = []
                        self.trend_count = Counter()
                else:
                        self.trend_raw.extend(trends)
                        self.trend_count = Counter( self.trend_raw )
                        top20 = self.trend_count.most_common(20)
                        self.trend_raw = []
                        for tag, num in top20:
                            for i in range(0, num):
                                self.trend_raw.append(tag)
                        self.trend_count = Counter( self.trend_raw )
                        session.TRACK = [tag.lower() for tag, num in top20 ]
                        session.TOP20 = top20


        def add(self, trends=[]):
                # this lets the bubble chart grow bigger
                self.trend_count = Counter(trends) + self.trend_count


class piestats:
        def __init__(self):
                self.sentiment_raw = []
                self.sentiment_count = Counter()

        def update(self, sentiment=[]):
                # this keeps track of the size of the pie chart
                if len(self.sentiment_raw) >= sys.maxint:
                        self.sentiment_raw = []
                        self.sentiment_count = Counter()
                else:
                        self.sentiment_raw.extend(sentiment)
                        self.sentiment_count = Counter( self.sentiment_raw )
                        self.sentiment_count.most_common()
        def add(self, sentiment=[]):
                self.sentiment_count = Counter(sentiment) + self.sentiment_count
