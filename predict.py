# coding: utf-8

'''
    電通生かどうかを推定する

    推定結果、特徴量の値をJSON形式で出力する
'''

import os
import re
import sys
import time
import json
import datetime
import numpy as np
from extract import extractFeatures
from sklearn.externals import joblib


tweetFilePath = sys.argv[1]

# 特徴量の抽出
extracter = extractFeatures()
features, names = extracter.get(tweetFilePath)

# 分類器で推定
clf  = joblib.load('clf.pkl')
flag = clf.predict( np.array(features).reshape((1,-1)) )[0]

# 結果を辞書型に変換
result = {}
result['screen_name'] = os.path.basename(tweetFilePath)
result['flag'] = flag
for name, feature in zip(names, features):
    result[name] = feature

# JSON形式で出力
jsonstring = json.dumps(result, default=str, indent=2)
print(jsonstring)

