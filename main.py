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

from collections import Counter
import logging

import tinysegmenter
segmenter = tinysegmenter.TinySegmenter()


from flask import Flask,render_template, request


app = Flask(__name__)

def to_vocabulary(text):
    """
    スペースで分かち書きされた文字列のリストを受け取り、
    単語の出現回数を数え上げる。
    [(単語,回数),(単語,回数)...]というリストを返す
    """
    t = []
    for line in text:
        t.extend(line.split())
    v = Counter(t)
    return v.items()


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text = request.form['text']
    else:
        text = ""

    result = '|'.join(segmenter.segment(text))


    return render_template("index.html",result=result)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
