#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cloudstorageの準備
googleからサンプルプログラムを他のディレクトリにcloneしておき、
python-docs-samples/appengine/standard/storage/appengine-client/lib
の中身(cloudstorageとGoogleAppEngineCloudStorageClient)をこのプロジェクトの
libにコピー

ローカルでのテスト
virtualenv env
source ./env/bin/activate
dev_appserver.py app.yaml

デプロイ

gcloud app deploy
gcloud app browse

"""

from __future__ import unicode_literals
from __future__ import print_function


import os
import logging
import pickle
from flask import Flask,render_template, request

import cloudstorage
from google.appengine.api import app_identity

cloudstorage.set_default_retry_params(
    cloudstorage.RetryParams(
        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15
        ))

BUCKET_NAME = app_identity.get_default_gcs_bucket_name()

from corpusenactor.echo import Echo


app = Flask(__name__)

MAIN_LOG_DISPLAY_LEN = 10
MAIN_LOG_PRESERVE_LEN = 100
LOG_FILENAME = '/'+BUCKET_NAME+"/main_log"



@app.route('/',methods=['POST','GET'])
def index():

    lines = []

    if request.method == 'POST':
        text = request.form['text']

        ce = Echo("chatbot/chatbot.yaml")
        reply = ce.reply(text)

        # cloudstorage.delete(LOG_FILENAME)

        """
        cloudstorageにファイルがあれば読み込む
        """
        stats = cloudstorage.listbucket(LOG_FILENAME)
        for stat in stats:
            with cloudstorage.open(LOG_FILENAME) as f:
                lines = pickle.load(f)

        lines.append({"speaker":"user","text":text})
        lines.append({"speaker":"bot","text":reply})
        lines = lines[-MAIN_LOG_PRESERVE_LEN:]

        write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)
        with cloudstorage.open(LOG_FILENAME,'w',content_type='text/plain',
            retry_params=write_retry_params) as f:
            pickle.dump(lines, f)

    return render_template("index.html",lines=lines[-MAIN_LOG_DISPLAY_LEN:])




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
