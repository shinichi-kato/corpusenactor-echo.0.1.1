#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ローカルでのテスト
virtualenv env
source ./env/bin/activate
dev_appserver app.yaml

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
from flask import Flask,render_template, request

from corpusenactor import CorpusEnactor


app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text = request.form['text']
    else:
        text = ""

    ce = CorpusEnactor("chatbot/chatbot.yaml")

    reply = ce.reply("test")

    return render_template("index.html",result=result)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
