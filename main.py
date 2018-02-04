# -*- coding: utf-8 -*-
"""
ローカルでのテスト
virtualenv env
source ./env/bin/activate
dev_appserver app.yaml

"""

import logging

from flask import Flask,render_template, request


app = Flask(__name__)

import re
RE_KATAKANA_WORD = re.compile(ur'([ァ-ー]+)')
RE_KANJI_WORD = re.compile(ur'([一-龥]+)')
RE_SEPARATOR = re.compile(ur'([,\.、。，]+)')
RE_INSERT_SPACE_R = re.compile(ur'(的|装置|用)'}
RE_INSERT_SPACE_R_AFTER_KANJI = re.compile(
    ur'[一-龥](である|でも|なの|こそ|です|から|まで|とか|など|で|を|の|が|も|や|は)'
)

def pseudoSegmenter(text):
    """ 精度を考慮しない分かち書き """
    text = RE_KATAKANA_WORD.sub(r' \1 ',text)
    text = RE_KANJI_WORD.sub(r' \1 ',text)
    text = RE_INSERT_SPACE_R_AFTER_KANJI.sub(r'\1 ',text)
    text = RE_INSERT_SPACE_R(r'\1 ',text)
    text = RE_SEPARATOR.sub(r' \1 ',text)

    return text



@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        text = request.form['text']
    else:
        text = ""

    result = pseudoSegmenter(text)

    return render_template("index.html",result=result)




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
