#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from collections import Counter
import codecs
import numpy as np

def to_vocabulary(corpus):
    """
    スペースで分かち書きされた文字列のリストを受け取り、
    単語の出現回数を数え上げる。
    [(単語,回数),(単語,回数)...]というリストを返す
    """
    words = []
    text = []
    for line in corpus:
        l = line.split()
        words.extend(l)
        text.append(l)

    v = Counter(words)
    return (v,text)

def vectorize(text,feat):

    """
    Term Frequency: 各行内での単語の出現頻度
    tf(t,d) = (ある単語tの行d内での出現回数)/(行d内の全ての単語の出現回数の和)
    """

    wv = np.zeros((len(text),len(feat)))
    tf = np.zeros((len(text),len(feat)))

    n = []

    i=0
    for line in text:
        v = Counter(line)
        for word in line:
            j = feat.index(word)
            wv[i,j] = v[word]

        nd = np.sum(wv[i])

        if nd != 0:
            tf[i] = wv[i] / nd
        i += 1


    """
    Inverse Document Frequency: 各単語が現れる行の数の割合
    idf(t) = log((全行数)/(ある単語tが出現する行の数))+1

    """

    df = np.apply_along_axis(np.count_nonzero,axis=0,arr=wv)
    idf = np.log(tf.shape[0]/df)+1

    """
    tfidf = tf*idf
    """

    tfidf = tf * idf

    return tfidf

def cosine_dist(wv):
    pass


# with codecs.open('dictionary/corpus_w.txt','r','utf-8') as f:
#     c = f.readlines()

c=["朝 昼 よる 猫","朝 庭 に 来る 小鳥","猫 と 庭 の 大きな 出来事"]

vocab,text = to_vocabulary(c)

""" word vectorのfeature """
feat = list(vocab.keys())

tfidf = vectorize(text,feat)

print(tfidf)
