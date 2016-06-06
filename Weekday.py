# coding: utf-8

'''
    曜日ごとのツイート数を出力するプログラム by 野村
    引数に与えられたディレクトリ下のファイルをツイートデータとして扱い分析します．
'''

import re
import os
import csv
import sys
import datetime

if len(sys.argv) < 2:
    print "Usage: >python TimeZone.py TweetDataDirectry"
    quit()

files = os.listdir(sys.argv[1])
rowList = []    # 出力データを格納するリスト
rowList.append([" ","Mon","Tue", "Wed","Thu","Fri","Sat","Sun"])

for file in files:
    with open(sys.argv[1] + "\\" + file, 'r') as tweetFile:
        fileName = os.path.basename(file)   # ファイルの名前をパスから切り出し
        path, ext = os.path.splitext(fileName)  # ベースネームと拡張子を取得

        tweetData = tweetFile.readline()
        weekdayCount = [0] * 8 # アカウント名＋曜日ごとのツイート数（0で初期化された要素数9のリスト）
        weekdayCount[0] = fileName

        while tweetData:
            tweetTime = re.split(r'[\s,:]', tweetData)   # 空白，カンマ，コロンで切り分け
            try:
                tweetDay = datetime.datetime.strptime(tweetTime[0], '%Y-%m-%d')  # ツイートした日付
                weekdayCount[datetime.date(tweetDay.year, tweetDay.month, tweetDay.day).isoweekday()] += 1    # カウントアップ
            except:
                print "can't encode character"
            finally:
                tweetData = tweetFile.readline()

        print weekdayCount
        rowList.append(weekdayCount)

with open("WeekdayResult.csv", "wb") as output:    # バイナリモードにしないと余計な改行が出る
    csvWriter = csv.writer(output)
    csvWriter.writerows(rowList)
