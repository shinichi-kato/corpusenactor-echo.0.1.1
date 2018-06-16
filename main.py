#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CorpusEnactor.Echo-0.1.1 UI

"""

from __future__ import unicode_literals
from __future__ import print_function


import os
import logging
import pickle
import json
from flask import Flask,render_template, request, jsonify

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
    """
    cloudstorageにファイルがあれば読み込む
    """
    try:
        with cloudstorage.open(LOG_FILENAME) as f:
            lines = pickle.load(f)

    except cloudstorage.NotFoundError as e:
        lines.append({'side':'left','speech':'Info: CouldStorage is Empty.'})

    return render_template("index.html",
        lines=lines[-MAIN_LOG_DISPLAY_LEN:],
        MAIN_LOG_DISPLAY_LEN=MAIN_LOG_DISPLAY_LEN)


@app.route('/ajax',methods=['POST'])
def ajax_request():
    data = json.loads(request.data)

    lines=[]

    """  ログファイルを読み込む  """
    try:
        with cloudstorage.open(LOG_FILENAME) as f:
            lines = pickle.load(f)
    except cloudstorage.NotFoundError as e:
        # lines.append({'side':'left','speech':e.message})
        pass

    cmd = data['command']

    if cmd == 'dump':
        return jsonify(log=lines)

    else:
        speech = data['speech']

        ce = Echo("chatbot/chatbot.yaml")
        reply = ce.reply(speech)

        if reply is False:
            reply = "not found"

        lines.append({"side":"right","speech":speech})
        lines.append({"side":"left","speech":reply})

        lines = lines[-MAIN_LOG_PRESERVE_LEN:]
        write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)

        with cloudstorage.open(LOG_FILENAME,'w',
            retry_params=write_retry_params) as f:
            pickle.dump(lines, f)

        return jsonify(log=[{'side':'left','speech':reply,'delay':len(reply)*0.1}])



@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
