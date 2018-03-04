# -*- coding: utf-8 -*-

"""
CorpusEnactor.Echoクラス
"""
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import yaml
import codecs
import pickle
from collections import Counter
import numpy as np

import cloudstorage
from google.appengine.api import app_identity

from tinysegmenter import TinySegmenter
Segmenter = TinySegmenter()

TFIDF_CACHE = "cache/tfidf.npz"
FEAT_CACHE = "cache/feat.pickle"


class Echo:
    """
    テキスト検索手法を用いた基本的なチャットボット

    チャットボットでよく用いられる応答方法の一つとして、ユーザの入力に似た文をログの中で検索し、
    最も似た文の次の行を返答として返す、というアルゴリズムがある。この動作の狙いは
    「ログ（またはコーパス）を再演する」
    ことである。CorpusEnactor.Echoクラスではユーザの入力文字列に似ている行を見つける最も
    オーソドックスな計算方法であるtfidf-cos類似度を用いた実装を行う。

    なお、このクラスはGoogle App Engine スタンダード環境でデプロイ可能な設計とする。

    コーパス（会話ログ）
    会話ログはタブ区切りテキスト形式で、一列目が名前、二列目は発言内容である。
    先頭が#の行はコメントとみなす

    """

    def __init__(self,setting):
        """
        setting: yaml形式の設定ファイル

        self.name: チャットボットの名前
        self.corpus_path: 会話ログのソース

        """
        with codecs.open(setting,"r",'utf-8') as f:
            data = yaml.safe_load(f.read())

        self.name = data['name']


        with codecs.open(data['corpus_path'],'r','utf-8') as f:
            self.corpus = f.readlines()
            """ コメント行の除去 """
            self.corpus = [x for x in self.corpus if not x.startswith('#')]


        if os.path.isfile(TFIDF_CACHE):
            if sys.version_info.major == 2:
                data = np.load(TFIDF_CACHE)
            else:
                data = np.load(TFIDF_CACHE,fix_imports=True)
            self.corpus_df = data['corpus_df']
            self.corpus_tfidf = data['corpus_tfidf']

        if os.path.isfile(FEAT_CACHE):
            with open(FEAT_CACHE,'rb') as f:
                self.feat = pickle.load(f)

        else:
            self.corpus_to_tfidf()

            np.savez(TFIDF_CACHE,
                corpus_df=self.corpus_df,
                corpus_tfidf=self.corpus_tfidf
                )

            with open(FEAT_CACHE,'wb') as f:
                pickle.dump(self.feat,f)



    def corpus_to_tfidf(self):
        """
        テキスト検索をするため、corpusをtfidf行列に変換する。
        検索にはdfも必要になるため格納しておく。
        """

        """
        前処理：
        corpusの発言部分を分かち書きし、単語リストを生成してself.featに格納する。
        corpusを分かち書きしたリストのリストに変換し、corpus_splittedに格納する。
        """

        words = []
        corpus_splitted = []
        for line in self.corpus:
            """ corpusの一列目は発言者名。二列目の発言内容のみ処理する """
            line = line.split()[1]
            l = Segmenter.segment(line)
            words.extend(l)
            corpus_splitted.append(l)

        v = Counter(words)

        self.feat = list(v.keys())


        """
        Term Frequency: 各行内での単語の出現頻度
        tf(t,d) = (ある単語tの行d内での出現回数)/(行d内の全ての単語の出現回数の和)
        """


        wv = np.zeros((len(self.corpus),len(self.feat)),dtype=np.float32)
        tf = np.zeros((len(self.corpus),len(self.feat)),dtype=np.float32)

        i=0
        for line in corpus_splitted:
            v = Counter(line)
            for word,count in v.items():
                j = self.feat.index(word)
                wv[i,j] = count

            tf[i] = wv[i] / np.sum(wv[i])
            i+=1


        """
        Inverse Document Frequency: 各単語が現れる行の数の割合
        df(t) = ある単語tが出現する行の数
        idf(t) = log((全行数)/ df(t) )+1
        """
        df = np.apply_along_axis(np.count_nonzero,axis=0,arr=wv)
        idf = np.log(tf.shape[0]/df) + 1

        tfidf = tf*idf

        self.corpus_df = df
        self.corpus_tfidf = tfidf


    def speech_to_tfidf(self,speech):
        """
        与えられた文字列speechをcorpusと同じ方法でtfidfベクターに変換する。
        ただしspeechはcorpusに全く現れない単語だけの場合がある。
        この場合tfidfは計算できないため、Noneを返す

        """

        """ 分かち書き """
        speech = Segmenter.segment(speech)


        """ tf """
        wv = np.zeros((len(self.feat)))
        tf = np.zeros((len(self.feat)))

        v = Counter(speech)
        for word,count in v.items():
            if word in self.feat:
                j = self.feat.index(word)
                """
                self.featに含まれない言葉がユーザ発言に含まれる場合、
                現状無視しているが、相手に聞き返すなどの対処がほしい
                """
                wv[j] = count

        nd = np.sum(wv)
        if nd == 0:
            """
            corpusと何も一致しない文字列の場合
            Noneを返す
            """
            return None


        """ tfidf """

        tf = wv / nd
        idf = np.log(tf.shape[0]/self.corpus_df)+1
        tfidf = tf*idf

        return tfidf

    def retrieve(self,ct,vt):
        """
        corpusのtfidfとspeechのtdidfでcos類似度ベクターを生成し、
        ベクターの成分は類似度で、それを降順に並び替えたindexリストを返す

        cos類似度 = ct・vt / |ct||vt|
        """
        inner = np.inner(ct,vt)
        norm_ct = np.apply_along_axis(np.linalg.norm,axis=1,arr=ct)
        norm_vt = np.linalg.norm(vt)

        cossim = inner / (norm_ct*norm_vt)

        return np.argsort(cossim, axis=0)[::-1]

    def reply(self,user_speech):

        user_tfidf = self.speech_to_tfidf(user_speech)
        if user_tfidf is not None:
            """
            コーパス中で最も似ていた行を探す
            """
            pos = self.retrieve(self.corpus_tfidf,user_tfidf)
            pos = pos[0]
            if pos < len(self.corpus):
                """
                コーパス中で最も似ていた行の、次の行を返答として返す。
                コーパスはカンマ区切りテキスト形式で、
                一列目は名前、二列目は発言内容である。二列目を返答として返す
                """
                reply = self.corpus[pos+1]

                return reply.split('\t')[1]


        return self.__class__.__name__+": reply not found"


def main():
    ce = CorpusEnactor('chatbot/chatbot.yaml')
    # print("feat=",ce.feat)
    # print("tfidf=",ce.corpus_tfidf)
    # v = ce.speech_to_tfidf("動物園へ行こう")
    # print("v=",v)
    # results = ce.retrieve(ce.corpus_tfidf,v)[:6]
    #
    # for r in results:
    #     print(r,ce.corpus[r])
    print(ce.reply("動物園へ行こう"))


if __name__ == '__main__':
    main()
