#!/usr/bin/env python
# coding: utf-8
import webapp2
import os
import logging
from google.appengine.ext.webapp import util
from lib import twitterlib
from lib import photolink
from models import PhotoLink, AccessToken
from google.appengine.api import taskqueue
from string import Template
import time
import calendar
import datetime


def restore_api(access_token):
    try:
        ctok, csec = open('./oauth_consumer').read().split()
        auth = twitterlib.TwitterOAuth(ctok, csec, use_https=True)
        # set access token
        atok,asec = access_token.access_token, access_token.access_token_secret
        auth.setAccessToken(atok, asec)

        api = twitterlib.API(auth, version=1.1)
        return api
    except Exception, e:
        logging.error(e)
        raise e

def twtime(created_at):
    unix_time = calendar.timegm(time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))
    unix_time += 32400 # GMT -> JST
    ut = time.localtime(unix_time)
    return time.strftime('%Y%m%d', ut)


def today(fmt='%04d%02d%02d'):
    x = datetime.datetime.today() + datetime.timedelta(hours=9)
    return fmt % (x.year, x.month, x.day)

class TweetHandler(webapp2.RequestHandler):
    def get(self):
        atok = self.getaccesstoken()
        try:
            api = restore_api(atok)
            param = self.analyze(atok, api)
            status = self.apply_template(param)
            api.statuses.update(status = status)
            logging.info('success tweet for %s' % param['screen_name'])
        except Exception, e:
            logging.error(e)

    def analyze(self, atok, api):
        screen_name = api.account.verify_credentials().screen_name

        t = today()
        n = 0
        for status in api.statuses.user_timeline(count = 200, include_rts = True):
            if t == twtime(status.created_at):
                n += 1
        n = n if n < 200 else '%d+' % n

        param = {
            'count': n,
            'screen_name': screen_name,
            'link': self.getphotolink(),
        }
        return param
    
    def getaccesstoken(self):
        for atk in AccessToken.all():
            return atk
    def getphotolink(self):
        for lnk in PhotoLink.all():
            return lnk.link

    def apply_template(self, param):
        tmpl = u'@${screen_name}さんは今日${count}回つぶやきました。${link} #nekofier'
        #tmpl = unicode(open('templates/tweet').read())
        tmpl = Template(tmpl)
        return tmpl.substitute(**param)

        
class UpdateLinkHandler(webapp2.RequestHandler):
    def get(self):
        try:
            url = photolink.get()
            lnk = PhotoLink.all().get()
            lnk.link = url
            lnk.put()
        except Exception, e:
            logging.error(e)

           
app = webapp2.WSGIApplication([
    ('/batch/tweet', TweetHandler),
    ('/batch/updatelink', UpdateLinkHandler),
    ],
    debug=True)
