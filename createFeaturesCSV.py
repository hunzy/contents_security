# coding: utf-8

'''
    全アカウントの特徴量を抽出したCSVデータを生成する

    フォーマット：

    アカウント名 + [特徴量のベクトル] + フラグ(電通生=1, 一般人=0)
    アカウント名 + [特徴量のベクトル] + フラグ(電通生=1, 一般人=0)
    アカウント名 + [特徴量のベクトル] + フラグ(電通生=1, 一般人=0)
    ...

'''

import os
from extract import extractFeatures

UEC_DIR    = 'uec_tweets/'
NOTUEC_DIR = 'notuec_tweets/'

extracter = extractFeatures() # 特徴抽出器

with open('featureData.csv', 'w') as csvfile:

    # 電通生のデータ作成
    users = os.listdir(UEC_DIR)

    #--- 最初にヘッダーを作成 ---
    _, names = extracter.get(os.path.join(UEC_DIR, users[0]))
    header = ['name'] + names + ['flag']
    csvfile.write(','.join(map(str, header)) + '\n')

    for user in users:
        print(user)
        tweetFilePath = os.path.join(UEC_DIR, user)
        features, names = extracter.get(tweetFilePath)
        data = [user] + features + [1]
        csvfile.write(','.join(map(str, data)) + '\n')


    # 非電通生のデータ作成
    users = os.listdir(NOTUEC_DIR)

    for user in users:
        print(user)
        tweetFilePath = os.path.join(NOTUEC_DIR, user)
        features, names = extracter.get(tweetFilePath)
        data = [user] + features + [0]
        csvfile.write(','.join(map(str, data)) + '\n')
