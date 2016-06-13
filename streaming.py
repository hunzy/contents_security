#coding: utf-8

"""
日本語のアカウントを適当に集める
"""

import re
import sys
import tweepy
from config import auth
from datetime import timedelta

class Listener(tweepy.StreamListener):
    count = 0
    def on_status(self, status):
        status.created_at += timedelta(hours=9)#世界標準時から日本時間に

        if status.author.lang == u'ja':
            print status.author.screen_name
            self.count += 1
            if self.count == 300:
                sys.exit()
        return True
     
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True
     
    def on_timeout(self):
        print('Timeout...')
        return True
 
listener = Listener()
stream = tweepy.Stream(auth, listener)

#stream.userstream()
#stream.filter(track=[u'電通大'])
stream.sample()
