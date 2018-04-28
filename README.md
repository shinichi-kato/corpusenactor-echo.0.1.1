# CorpusEnactor_Echo-0.1.1
テキスト検索手法を使ったシンプルなチャットボット
====
## Description
チャットボットは会話のパターンを模倣することでユーザと会話をするプログラムです。そのパターンの一つに
「会話ログの再現」があり、その中で最もシンプルなものはユーザから入力された発言と最も似た行を会話ログの
中から検索し、その行の次の行を返答として返す、というものです。 CorpusEnactor.Echo は検索の手法として
検索サイトなどで標準的に使われる TFIDF-cos類似度 を用いてチャットボットを実装します。
version 0.2.0では計算データとログをcloudstorage上に保持するように変更しました。

## Getting Started

CorpusEnactor.Echo は Google Application Engine 標準環境で動作するよう設計されています。
以下に開発環境設定、ダウンロード、ローカルでのテストからデプロイまでの手順を示します。

### Prerequisites

Googld Cloud Platformのアカウントを取得してください。ローカルでアプリケーションをテストするのに必要な
Google Cloud SDKを https://cloud.google.com/sdk/downloads?hl=ja からダウンロードし、インストールしてください。


またローカルにはAnacondaを https://www.anaconda.com/download/ から取得し、インストールしてください。
pythonのバージョンは2系、3系どちらでもOKです。以下のコマンドでGAE(Google AppEngine)用の環境を作成します。

```
conda create -n gaestd anaconda numpy=1.6 python=2.7
source activate gaestd
```

### Installing

このソースコードを展開したディレクトリに移動し、以下のコマンドを実行してください。これは初回のみ実行します。

```
pip install -r requirements.txt
pip install --upgrade google-cloud-storage
pip install GoogleAppEngineCloudStorageClient -t lib/
gcloud init
```



### Running the tests

ローカルでテストするには、gaestd環境に入った状態(コマンドライン先頭に(gaestd)と表示されます。)で、ソースコードを置いたディレクトリにて

```
dev_appserver.py .
```
としてください。ブラウザで http://localhost:8000 を開くとローカル開発用のダッシュボード画面が表示されます。 画面中の default をクリックするか http://localhost:8080 を開くとアプリケーションがローカルで動作しているのを確認できます。

## Deployment

```
gcloud app deploy
gcloud app browse
```

## Built with
Tinesegmenter (http://chasen.org/~taku/software/TinySegmenter/)を利用しています。

## Author

* *加藤真一,Ph.D.* (http://www.ycf.nanet.co.jp/~skato/muno/)


## Licence

This project is licensed under the MIT License - see [MIT_Licence] (https://ja.osdn.net/projects/opensource/wiki/licenses%2FMIT_license) file for details

## Acknowledgements

* 藤野博, Ph. D.
* 金子弘行, Ph. D.
