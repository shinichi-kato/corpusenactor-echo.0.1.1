#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from collections import Counter


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

with open('dictionary/corpus_w.txt','r') as f:
    c = f.readlines()

v = to_vocabulary(c)
print(v)
