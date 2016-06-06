# coding: utf-8

'''
    時間帯ごとのツイート数を出力するプログラム by 野村
    引数に与えられたディレクトリ下のファイルをツイートデータとして扱い分析します．
'''

import re
import os
import csv
import sys

if len(sys.argv) < 2:
    print "Usage: >python TimeZone.py TweetDataDirectry"
    quit()

files = os.listdir(sys.argv[1])
rowList = []    # 出力データを格納するリスト
rowList.append([" ","0 to 3","3 to 6", "6 to 9","9 to 12","12 to 15","15 to 18","18 to 21","21 to 24"])

for file in files:
    with open(sys.argv[1] + "\\" + file, 'r') as tweetFile:
        fileName = os.path.basename(file)   # ファイルの名前をパスから切り出し
        path, ext = os.path.splitext(fileName)  # ベースネームと拡張子を取得

        tweetData = tweetFile.readline()
        timeZoneCount = [0] * 9 # アカウント名＋時間帯ごとのツイート数（0で初期化された要素数9のリスト）
        timeZoneCount[0] = fileName

        while tweetData:
            tweetTime = re.split(r'[\s,:]', tweetData)   # 空白，カンマ，コロンで切り分け
            try:
                tweetTimeHH = tweetTime[1]  # ツイートした時刻HH
                timeZone = int(tweetTimeHH) / 3 # 3時間毎に時間帯を分割
                timeZoneCount[timeZone + 1] += 1    # カウントアップ
            except:
                print "can't encode character"
            finally:
                tweetData = tweetFile.readline()

        print timeZoneCount
        rowList.append(timeZoneCount)

with open("TimeZoneResult.csv", "wb") as output:    # バイナリモードにしないと余計な改行が出る
    csvWriter = csv.writer(output)
    csvWriter.writerows(rowList)
