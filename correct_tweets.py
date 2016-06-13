#coding: utf-8

"""
アカウントリストに含まれるユーザの
最新1000件のツイートを取得して保存
"""

import os
import sys
import time
import codecs
import tweepy
from config import auth
from datetime import timedelta

api = tweepy.API(auth)
ACCOUNT_LIST = 'not_uec_students.csv'
SAVE_DIR     = 'notuec_tweets/'

def save_user_tweets(screen_name):
    """
    指定したユーザの最新ツイート上位1000件を取得して保存（RE,RT含む）
    """
    waiting_time = 6
    pagination   = [1,2,3,4,5]

    fw = open(os.path.join(SAVE_DIR, screen_name), 'w')
    for page in pagination:
        print('{} page{}'.format(screen_name, page))
        _s = time.time()

        tweets = api.user_timeline(screen_name, count=200, page=page)
        for tweet in tweets:
            created_at = tweet.created_at + timedelta(hours=9)    # 世界標準時から日本時間に
            created_at = created_at.strftime('%Y-%m-%d %H:%M:%S') # 日付文字列に変換
            text = tweet.text.replace('\n', '\t').encode('utf-8')
            fw.write('{},{}\n'.format(created_at, text))

        _e = time.time()
        _cycle = _e - _s 
        if _cycle < waiting_time: # リクエストを5.5秒に一回のペースに保つ
            time.sleep(waiting_time - _cycle)

    fw.close()

if __name__ == '__main__':
    fr = open(ACCOUNT_LIST, 'r')

    for i, line in enumerate(fr.readlines()):
        screen_name = line.rstrip()
        print('{} {}'.format(i, screen_name)) # 進捗確認

        user = api.get_user(screen_name)
        if user.protected == True or user.statuses_count < 1000:
            continue
        else:
            save_user_tweets(screen_name)
