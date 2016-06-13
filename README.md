# コンテンツセキュリティ特論

## classification.py の使い方

特徴量データが含まれるcsvフォルダをこのディレクトリに移動

以下の情報を書いた、config.pyを作成する
```
#coding: utf-8

import tweepy

CONSUMER_KEY = 'XXX' ←自分のキーを用いる
CONSUMER_SECRET = 'XXX'
ACCESS_TOKEN = 'XXX'
ACCESS_SECRET = 'XXX'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
```

実行すると分類精度などが出る。
追加で色々分析したい場合は、以下の用にipythonで実行する。
```
ipython -i classification.py
```

## 必要なライブラリ

* numpy
* scipy
* tweepy
* scikit-learn
* pandas