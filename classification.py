# coding: utf-8

"""
得られた特徴量をもとに分類器を作成
5分割交差検証による評価を行う
"""

import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn import cluster
from sklearn import svm
from sklearn import tree
from sklearn import metrics
from sklearn import neighbors
from sklearn import naive_bayes as NB
from sklearn import cross_validation as CV
from sklearn.feature_selection import RFE

# データの読み込み
df1_uec = pd.read_csv('csv/repRT_uec.csv')
df2_uec = pd.read_csv('csv/TimeZoneResult_uec.csv')
df3_uec = pd.read_csv('csv/WeekdayResult_uec.csv')
df4_uec = pd.read_csv('csv/follows_uec.csv')
df5_uec = pd.read_csv('csv/characters_uec.csv')

uec = pd.merge(df1_uec, df2_uec, on='name')
uec = pd.merge(uec, df3_uec, on='name')
uec = pd.merge(uec, df4_uec, on='name')
uec = pd.merge(uec, df5_uec, on='name')

df1_notuec = pd.read_csv('csv/repRT_notuec.csv')
df2_notuec = pd.read_csv('csv/TimeZoneResult_notuec.csv')
df3_notuec = pd.read_csv('csv/WeekdayResult_notuec.csv')
df4_notuec = pd.read_csv('csv/follows_notuec.csv')
df5_notuec = pd.read_csv('csv/characters_notuec.csv')

notuec = pd.merge(df1_notuec, df2_notuec, on='name')
notuec = pd.merge(notuec, df3_notuec, on='name')
notuec = pd.merge(notuec, df4_notuec, on='name')
notuec = pd.merge(notuec, df5_notuec, on='name')

all_users = pd.concat([uec, notuec], axis=0) # 縦に結合
all_users.index = range(len(all_users))      # インデックスを整える
is_uec    = np.ones(len(uec))
is_notuec = np.zeros(len(notuec))

data   = all_users[all_users.columns[1:]].as_matrix()
data_name = uec.columns[1:]
target = np.hstack((is_uec, is_notuec))

# # 訓練データとテストデータに分ける
data_train, data_test, target_train, target_test = CV.train_test_split(data, target)

# clf = neighbors.KNeighborsClassifier()
# clf = tree.DecisionTreeClassifier()
# clf = svm.LinearSVC()
clf = NB.GaussianNB()
clf.fit(data_train, target_train)
target_predict = clf.predict(data_test)

print('--- Confusion Matrix ---')
print( metrics.confusion_matrix(target_test, target_predict) )

print('--- Accuracy ---')
print( metrics.accuracy_score(target_test, target_predict) ) # 正解率

print('--- Cross-Validation Score ---')
scores = CV.cross_val_score(clf, data, target, cv=5)
print( scores )         # クロスバリデーションの配列
print( scores.mean() )  # クロスバリデーションの平均

