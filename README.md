# コンテンツセキュリティ特論
Twitterのアカウントから、その人が電通生かどうかを判定するシステムを構築する

## プログラム概要

* predict.py: ツイートデータから電通生かどうかを判定する
* extract.py: ツイートデータから特徴量を抽出するクラス
* createFeaturesCSV.py: 特徴量のCSVデータを作成する（分類器生成に使用）
* createClassfier.py: 特徴量データから分類器を生成する

## 使い方
1. 同ディレクトリに以下のデータを用意する
	* uec_tweets/ (電通生のツイートデータ)
	* notuec_tweets/ (非電通生のツイートデータ)
2. createFeaturesCSV.pyを実行 (featureData.csvが生成される)
3. createClassfier.pyを実行 (clf.pklが生成される)
4. 推定したいユーザのツイートデータを引数とし、predict.pyを実行
5. 推定結果がJSON形式で出力される

## 実行環境
python3.5.1 (anaconda3-4.0.0)

### 実行環境の作り方(Mac, Linux版)
以下のコマンドを実行（.bash_profileの部分は適宜読み替える）

```
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$ 
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

pythonの環境を入れたいディレクトリに移動し、以下を実行

```
$ pyenv install anaconda3-4.0.0
... しばし待つ
$ pyenv rehash
$ pyenv local anaconda3-4.0.0
```

pyenv versionを実行し、anaconda3-4.0.0が表示されれば完成

### 実行環境の作り方(Windows版)
分からん

