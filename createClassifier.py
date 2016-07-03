# coding: utf-8

"""
得られた特徴量をもとに分類器を作成
5分割交差検証による評価を行う
"""

import pandas as pd
import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn import metrics
from sklearn import neighbors
from sklearn import naive_bayes as NB
from sklearn import cross_validation as CV
from sklearn import preprocessing
from sklearn.externals import joblib


# データの読み込み
df = pd.read_csv('featureData.csv')

data   = df[df.columns[1:-1]].as_matrix()
data   = preprocessing.normalize(data) # 正規化
data_name = df.columns[1:-1]
target = df.flag.as_matrix()

# # 訓練データとテストデータに分ける
data_train, data_test, target_train, target_test = CV.train_test_split(data, target)

# clf = tree.DecisionTreeClassifier()
# clf = svm.LinearSVC()
# clf = neighbors.KNeighborsClassifier()
clf = NB.GaussianNB()
clf.fit(data_train, target_train)
target_predict = clf.predict(data_test)

print( metrics.confusion_matrix(target_test, target_predict) )
print( metrics.accuracy_score(target_test, target_predict) ) # 正解率

scores = CV.cross_val_score(clf, data, target, cv=5)
print( scores )         # クロスバリデーションの配列
print( scores.mean() )  # クロスバリデーションの平均

# 分類器の保存
joblib.dump(clf, 'clf.pkl')