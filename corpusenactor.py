"""
CorpusEnactorクラス
"""

import os
import yaml
import codecs
import pickle
from collections import Counter
import numpy as np

from tinysegmenter import TinySegmenter
Segmenter = TinySegmenter()

TFIDF_CACHE = "cache/tfidf.npz"
FEAT_CACHE = "cache/feat.pikle"


class CorpusEnactor:
    """
    ログ型チャットボット
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
            data = np.load(TFIDF_CACHE,fix_imports=True)
            self.corpus_df = data['corpus_df']
            self.corpus_tfidf = data['corpus_tfidf']

        if os.path.isfile(FEAT_CACHE):
            with open(FEAT_CACHE,'rb') as f:
                self.feat = pickle.load(f)

        else:
            self.to_vocabulary()
            self.corpus_to_tfidf()

            np.savez(TFIDF_CACHE,
                corpus_df=self.corpus_df,
                corpus_tfidf=self.corpus_tfidf
                )

            with open(FEAT_CACHE,'wb') as f:
                pickle.dump(self.feat,f)


    def to_vocabulary(self):
        """
        corpusの発言部分を分かち書きし、単語リストを生成してself.featに格納。
        """


        words = []
        text = []
        for line in self.corpus:
            """ corpusの一列目は発言者名。二列目の発言内容のみ処理する """
            line = line.split()[1]
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



        wv = np.zeros((len(self.corpus),len(self.feat)),dtype=np.float32)
        tf = np.zeros((len(self.corpus),len(self.feat)),dtype=np.float32)

        """
        Term Frequency: 各行内での単語の出現頻度
        tf(t,d) = (ある単語tの行d内での出現回数)/(行d内の全ての単語の出現回数の和)
        """

        i=0
        for line in self.corpus_splitted:
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
        新たに入力されたり生成されたセリフspeechについても、corpusと
        同じくtfidfベクターを生成する。
        speechはcorpusに全く現れない単語だけの場合がある。
        この場合tfidfは計算できないため、Falseを返す

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
            Falseを返す
            """
            return False


        """ tfidf """

        tf = wv / nd
        idf = np.log(tf.shape[0]/self.corpus_df)+1
        tfidf = tf*idf

        return tfidf

    def retrieve(self,ct,vt):
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

    def reply(user_speech):

        user_tfidf = self.speech_to_tfidf(user_speech)
        if user_tfidf:
            """
            コーパス中で最も似ていた行を探す
            """
            pos = self.retrieve(self.corpus_tfidf,user_tfidf)
            pos = pos[0]
            if pos != len(self.corpus):
                """
                コーパス中で最も似ていた行の、次の行を返答として返す。
                コーパスはカンマ区切りテキスト形式で、
                一列目は名前、二列目は発言内容である。二列目を返答として返す
                """
                reply = self.corpus[pos+1]
                return reply.split(',')[1]

        return __class__.__name__+": reply not found"


def main():
    ce = CorpusEnactor('chatbot/chatbot.yaml')
    print("feat=",ce.feat)
    print("tfidf=",ce.corpus_tfidf)
    v = ce.speech_to_tfidf("うんうん。眠り袋")
    results = ce.retrieve(ce.corpus_tfidf,v)[:6]

    for r in results:
        print(r,ce.corpus[r])


if __name__ == '__main__':
    main()
