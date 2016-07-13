# coding: utf-8

'''
    電通生かどうかを推定する

    推定結果、特徴量の値をJSON形式で出力する
'''

import os
import re
import sys
import time
import math
import json
import datetime
import numpy as np
from scipy.spatial import distance
from extract import extractFeatures
from sklearn.externals import joblib

def sim(x1, x2):
    """
        ベクトルの2点間の(コサイン)距離を返す
    """
    #return np.linalg.norm(x1-x2)
    return distance.cosine(x1, x2)

def sigmoid(x, a=1):
    """
        シグモイド関数（aはゲイン）
    """
    return 1 / (1 + math.exp(-a*x))


# ファイル読み込み
tweetFilePath = sys.argv[1]

# 特徴量の抽出
extracter = extractFeatures()
features, names = extracter.get(tweetFilePath)

# 分類器で推定
clf  = joblib.load('clf.pkl')
flag = clf.predict( np.array(features).reshape((1,-1)) )[0]

# 電通生度合いを判定
means       = np.load('means.npz') # 平均ベクトルの読み込み
uec_mean    = means['uec']      # 電通生の平均ベクトル
notuec_mean = means['notuec']   # 非電通生の平均ベクトル
target      = np.array(features)
d1 = sim(target, uec_mean)      # 電通生との距離計算
d2 = sim(target, notuec_mean)   # 非電通生との距離計算
level = sigmoid(d2-d1, a=20)    # 電通生度合いを計算
level = int(level*100)          # パーセンテージに変換

# 結果を辞書型に変換
result = {}
result['screen_name'] = os.path.basename(tweetFilePath)
result['flag'] = flag
result['level'] = level
for name, feature in zip(names, features):
    result[name] = feature

# JSON形式で出力
jsonstring = json.dumps(result, default=str, indent=2)
print(jsonstring)

