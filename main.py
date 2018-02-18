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
import codecs
from flask import Flask,render_template, request

from corpusenactor import CorpusEnactor


app = Flask(__name__)

MAIN_LOG = "chatbot/log.yaml"
MAIN_LOG_DISPLAY_LEN = 10
MAIN_LOG_PRESERVE_LEN = 100


@app.route('/',methods=['POST','GET'])
def index():

    lines = []

    if os.path.isfile(MAIN_LOG):
        with codecs.open(MAIN_LOG,"r",'utf-8') as f:
            lines = yaml.load(f)

    if request.method == 'POST':
        text = request.form['text']

        ce = CorpusEnactor("chatbot/chatbot.yaml")
        reply = ce.reply(text)

        lines.append(text)
        lines.append(reply)

        try:
            with codecs.open(MAIN_LOG,'w','utf-8')
                fcntl.flock(f,fcntl.LOCK_EX)
                f.write(yaml.dump(lines,default_flow_style=False))
                fcntl.flock(f,fcntl.LOCK_UN)


        except OSError:
            return render_template('retry.html')


    return render_template("index.html",reply=reply,text=text)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
