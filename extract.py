# coding: utf-8

'''
    各特徴のベクトルを算出するプログラム
    引数に与えられたファイルをツイートデータとして扱い分析します．

    入力：ツイートデータファイルのパス

    ReplyRT
    出力：['アカウント名', 'リプライ数', '＠ツイート数']

    TimeZone
    出力：['アカウント名', '0-3時のツイート数', '3-6', '6-9', '9-12', '12-15', '15-18', '18-21', '21-24']

    Weekday
    出力：['アカウント名', '月曜日のツイート数', '火', '水', '木', '金', '土', '日']

    Character
    出力：['アカウント名', '平均文字数', '絵文字の数', '特徴語の数']
'''

import codecs
import os
import re
import sys
import time
import datetime

class extractFeatures(object):
    def __init__(self):
        pass

    '''
        全ての特徴量を返す
    '''
    def get(self, tweetFilePath):
        with codecs.open(tweetFilePath, 'r', 'utf-8') as tweetFile:
            self.tweetLines = tweetFile.readlines()

        cvec = self.calcCharacterVec(tweetFilePath)
        rvec = self.calcReplyRTVec(tweetFilePath)
        wvec = self.calcWeekdayVec(tweetFilePath)
        tvec = self.calcTimeZoneVec(tweetFilePath)
        fvec = self.calcFFVec(tweetFilePath)

        featureVector = cvec[1:]+rvec[1:]+wvec[1:]+tvec[1:]+fvec[1:]
        featureName   = ['textMean', 'emoticon', 'featureWord', 'replay', 'retweet',
                         'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun',
                         '0-3', '3-6', '6-9', '9-12', '12-15', '15-18', '18-21', '21-24',
                         'follow_art', 'follow_phys', 'follow_ofc']

        return [featureVector, featureName]

    '''
        リプライ，リツイート数
    '''
    def calcReplyRTVec(self, tweetFilePath):
        accountName = os.path.basename(tweetFilePath)   # ファイルの名前をパスから切り出してアカウント名とする

        repRT_Count = [0] * 3 # アカウント名，リプライ数，リツイート数
        repRT_Count[0] = accountName

        for tweet in self.tweetLines:
            if ",@" in tweet:
                #print tweet.decode('utf-8')
                repRT_Count[1] += 1
            if ",RT @" in tweet:
                repRT_Count[2] += 1

        return repRT_Count


    '''
        時間帯
    '''
    def calcTimeZoneVec(self, tweetFilePath):
        fileName = os.path.basename(tweetFilePath)   # ファイルの名前をパスから切り出し
        timeZoneCount = [0] * 9 # アカウント名＋時間帯ごとのツイート数（0で初期化された要素数9のリスト）
        timeZoneCount[0] = fileName

        for tweet in self.tweetLines:
            tweetTime = re.split(r'[\s,:]', tweet)   # 空白，カンマ，コロンで切り分け
            try:
                tweetTimeHH = tweetTime[1]  # ツイートした時刻HH
                timeZone = int(tweetTimeHH) // 3 # 3時間毎に時間帯を分割
                timeZoneCount[timeZone + 1] += 1    # カウントアップ
            except:
                continue

        return timeZoneCount


    '''
        曜日
    '''
    def calcWeekdayVec(self, tweetFilePath):
        fileName = os.path.basename(tweetFilePath)   # ファイルの名前をパスから切り出し

        weekdayCount = [0] * 8 # アカウント名＋曜日ごとのツイート数（0で初期化された要素数8のリスト）
        weekdayCount[0] = fileName

        for tweet in self.tweetLines:
            tweetTime = re.split(r'[\s,:]', tweet)   # 空白，カンマ，コロンで切り分け
            try:
                tweetDay = datetime.datetime.strptime(tweetTime[0], '%Y-%m-%d')  # ツイートした日付
                weekdayCount[datetime.date(tweetDay.year, tweetDay.month, tweetDay.day).isoweekday()] += 1    # カウントアップ
            except:
                continue

        return weekdayCount


    '''
        文字特徴量
    '''
    def calcCharacterVec(self, tweetFilePath):
        emoticon_matcher = re.compile('[\U0001F004-\U0001F64F]')
        rep_link = re.compile('(@\w+ |https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)') # リプライとURLを省く
        feature_words = ['調布','寝る','研究','情報','大学','死ぬ','京王',
                        'ゲーム','バイト','アニメ','先生','オタク','電通大',
                        '電気通信大学','ライブ','学生','授業','レポート','実験','漫画'] # 本当は形態素解析が必要

        fileName = os.path.basename(tweetFilePath)   # ファイルの名前をパスから切り出し

        characterCount = [0] * 4 # アカウント名＋平均文字数＋絵文字の数＋特徴語の数

        total_chars = 0
        total_lines = 0
        total_emoticon = 0
        total_feature_words = 0

        for tweet in self.tweetLines:
            #print(tweet)
            try:
                text = tweet.rstrip().split(',')[1]
                text = rep_link.sub('', text)
            except Exception as e:
                continue

            total_chars += len(text)
            total_lines += 1
            total_emoticon += len(emoticon_matcher.findall(text))

            for word in feature_words: # 特徴語の数を数える
                total_feature_words += text.count(word)

        characterCount = [fileName, total_chars//total_lines, total_emoticon, total_feature_words]
        return characterCount


    """
        フォロー・フォロワー
    """
    def calcFFVec(self, tweetFilePath):
        import art_followers
        import phisi_followers
        import official_followers

        accountName = os.path.basename(tweetFilePath)   # ファイルの名前をパスから切り出してアカウント名とする
        ffVec = [0] * 4

        artFollowerList = art_followers.accounts    # 文化系サークルアカウントのフォロワー
        physFollowerList = phisi_followers.accounts # 体育系サークルアカウントのフォロワー
        ofcFollowerList = official_followers.accounts   # 公式アカウントのフォロワー

        artCount = artFollowerList.count(accountName)
        physCount = physFollowerList.count(accountName)
        ofcCount = ofcFollowerList.count(accountName)

        ffVec = [ accountName, artCount, physCount, ofcCount]
        return ffVec


if __name__ == "__main__":
    """
        テスト
    """
    tweetFilePath = sys.argv[1]
    ext = extractFeatures()

    features, names = ext.get(tweetFilePath)

    print(features)
    print(names)
