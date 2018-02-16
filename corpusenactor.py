"""
CorpusEnactorクラス
"""

import os
import yaml
import codecs
import pickle
import numpy as np

from tinysegmenter import TinySegmenter
Segmenter = tinysegmenter.TinySegmenter()

TFIDF_CACHE ="cache/tfidf.pickle"


class CorpusEnactor:
    """
    ログ型チャットボット
    """

    def __init__(setting):
        """
        setting: yaml形式の設定ファイル

        self.name: チャットボットの名前
        self.corpus: 会話ログのソース
        self.feat: 会話ログに現れる単語のリスト

        """
        with codecs.open(setting,"r",'utf-8') as f:
            data = yaml.safe_load(f.read())

        self.name = data['name']

        with codecs.open(data['corpus_path'],'r','utf-8') as f:
            self.corpus = f.readlines()


        if os.path.isfile(TFIDF_CACHE):
            with open(TFIDF_CACHE,'rb') as f:
                self.corpus = pickle.load(f)
        else:


    def to_vocabulary(self):
        """
        corpusを分かち書きし、単語リストを生成してself.featに格納。
        """


        words = []
        text = []
        for line in self.corpus:
            l = Segmenter.segment(line)
            words.extend(l)
            text.append(l)

        v = Counter(words)

        self.feat = list(v.keys())
        self.corpus_splitted = text


    def corpus_to_tfidf(self):
        """
        corpusからテキスト検索をするため、各行のtfidfベクターを
        予め計算しておき、tfidf行列にしておく。
        あとの計算でdfも必要になるため、ここでselfに格納しておく。
        """

        wv = np.zeros((len(self.corpus),len(self.feat)))
        tf = np.zeros((len(self.corpus),len(self.feat)))

        """
        Term Frequency: 各行内での単語の出現頻度
        tf(t,d) = (ある単語tの行d内での出現回数)/(行d内の全ての単語の出現回数の和)
        """

        i=0
        for line in self.corpus_splitted:
            v = Counter(line)
            for word,count in v:
                j = feat.index(word)
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
        新たに入力されたり生成されたセリフspeechについても、corpusと
        同じくtfidfベクターを生成する。
        speechはcorpusに全く現れない単語だけの場合がある。
        この場合tfidfは計算できないため、Falseを返す

        """

        """ 分かち書き """
        speech = Segmenter.segment(speech)


        """ tf """
        wv = np.zeros(1,len(self.feat))
        tf = np.zeros(1,len(self.feat))

        v = Counter(speech)
        for word,count in v:
            j = feat.index(word)
            wv[j] = count

        nd = np.sum(wv)
        if nd == 0:
            """
            corpusと何も一致しない文字列の場合
            Falseを返す
            """
            return False


        """ tfidf """

        tf = wv / nd
        idf = np.log(tf.shape[0]/self.df)+1
        tfidf = tf*idf

        return tfidf

    def retrieve(ct,vt):
        """
        corpusのtfidfとspeechのtdidfでcos類似度ベクターを生成し、
        降順でindexリストを返す

        cos類似度 = ct・vt / |ct||vt|
        """
        inner = np.inner(ct,vt)
        norm_ct = np.linalg.norm(ct,axis=1)
        norm_vt = np.linalg.norm(vt)

        cossim = inner / (norm_ct*norm_vt)

        return np.argsort(cossim, axis=0)[::-1]

        
