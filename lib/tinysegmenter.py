#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TinySegmenter 0.1 -- Super compact Japanese tokenizer in Javascript
(c) 2008 Taku Kudo <taku@chasen.org>
TinySegmenter is freely distributable under the terms of a new BSD licence.
For details, see http://chasen.org/~taku/software/TinySegmenter/LICENCE.txt
"""

import re

try:
    xrange
except NameError:
    xrange = range       # for Python3

class TinySegmenter(object):
    default_model = {u'BC1':{u'II':-1369,u'IO':1532,u'KK':-1817,u'NO':579,u'OH':1274,u'ON':657,u'OO':-616},u'BC2':{u'AA':-17066,u'IH':-520,u'II':-613,u'KH':919,u'KI':-40,u'KK':-3853,u'NN':-1340,u'OI':92},u'BC3':{u'IK':200,u'IO':39,u'OH':-131},u'BIAS':1188,u'BP1':{u'BB':-41,u'BO':-446,u'OB':95,u'OO':-152,u'UO':5088},u'BP2':{u'OB':3939,u'UO':2344},u'BQ1':{u'BIH':-1344,u'BKK':-1776,u'BNH':604,u'BOI':-130,u'OOI':6100,u'UAA':1380},u'BQ2':{u'BHI':-43,u'BHO':-132,u'BIH':-590,u'BKI':-130,u'OHH':-44,u'OHI':48,u'UII':-3873,u'UKK':-7809},u'BQ3':{u'BHH':-5785,u'BII':-3004,u'BIM':-3041,u'BNH':739,u'BOI':596,u'BOK':1064,u'OHI':134,u'OII':38,u'OKI':-43},u'BQ4':{u'BHH':-2571,u'BII':-3474,u'BIO':286,u'BNN':-8814,u'OHO':-487,u'OKK':87},u'BW1':{u'ある':2518,u'い、':-4517,u'いた':1243,u'いな':1413,u'うん':1510,u'えっ':3648,u'かっ':-491,u'きた':871,u'この':-1013,u'した':1558,u'その':-3700,u'それ':506,u'たち':-1277,u'っち':807,u'って':-1449,u'っと':1236,u'てい':1859,u'てき':683,u'ない':442,u'にし':837,u'まあ':2083,u'んだ':3321,u'んで':401,u'んな':-556,u'イヴ':683,u'コロ':-1111,u'シュ':2569,u'ロム':1497,u'大丈':-589,u'宝箱':2062},u'BW2':{u'あー':-3228,u'いい':812,u'いう':-4883,u'いて':-1302,u'いる':1282,u'え、':1399,u'える':-501,u'がら':-3193,u'くな':-1477,u'けど':2388,u'こと':-194,u'しい':-1780,u'した':528,u'して':64,u'しょ':-42,u'する':1005,u'たい':-178,u'だね':-1325,u'だよ':1917,u'てい':2055,u'ては':-1248,u'てる':-4458,u'です':-3341,u'に、':-131,u'ねー':-4907,u'ゃあ':-4427,u'よう':-1234,u'んか':-467,u'んだ':5054,u'んな':-4968,u'ーん':-132},u'BW3':{u'、ど':-1566,u'あ、':-1124,u'ある':969,u'いE1':-626,u'いい':3450,u'いう':-3216,u'いる':3511,u'おい':-875,u'けど':499,u'こと':437,u'しま':43,u'すね':-1216,u'だね':1536,u'だよ':313,u'った':-776,u'っと':-442,u'です':88,u'ない':1532,u'ん、':-2369,u'んだ':3297,u'んで':3094,u'ヘル':-695,u'与え':-1493},u'TC1':{u'ANH':-978,u'IHI':-189,u'KKI':1000,u'NHH':2150,u'OAA':330,u'OHI':-413,u'OII':-1354},u'TC2':{u'HHO':-964,u'HIO':-2937,u'IIK':337,u'IIO':-2176,u'KII':104,u'KKK':-1246,u'KKO':-1610,u'NIO':1463,u'OHH':-496,u'OHO':1435,u'OIO':270},u'TC3':{u'HHH':150,u'HHI':-86,u'HHO':-43,u'HIH':280,u'HII':-1612,u'IIH':-521,u'IOI':355,u'KIH':-508,u'KIO':-1149},u'TC4':{u'HHI':784,u'HIH':230,u'HIO':-47,u'IHH':-269,u'III':315,u'IOH':546,u'IOO':-107,u'KII':-278,u'KKK':892,u'OHH':-541,u'OII':914,u'OOO':151},u'TQ1':{u'BHHI':-235,u'BHIH':-658,u'BHII':47,u'BIHI':534,u'BIIH':818,u'BIII':393,u'BKIH':-3713,u'BOOH':2643,u'BOOK':1042,u'OHHI':257,u'OIHH':-935,u'OIHI':-1526,u'OIIH':-537,u'OIII':-97,u'OIOH':4155,u'OKIH':5335,u'OKII':879,u'OKIK':2347},u'TQ2':{u'BHHH':1380,u'BHHI':-43,u'BHHO':-149,u'BHOK':-1365,u'BIII':250,u'BOHH':-141,u'BOII':-265,u'OAII':-389,u'OHHH':-585,u'OIIO':-624,u'OKKI':-44},u'TQ3':{u'BAII':-1756,u'BHHO':-603,u'BHIH':367,u'BHII':1082,u'BIHH':-1250,u'BIHI':-368,u'BIIH':-3054,u'BIII':320,u'BIIO':-1394,u'BINH':87,u'BIOO':-700,u'BKKK':2694,u'BNHH':1737,u'BNHI':735,u'BOHH':-1352,u'BOII':-1034,u'BOKK':-2342,u'BOOI':5343,u'OAII':1350,u'OHHH':-3196,u'OHIH':-4795,u'OIHI':295,u'OIIH':242,u'OIII':-132,u'OIIK':1926,u'OIKK':134,u'OKII':1443,u'OKKK':-1286,u'OKKO':-44,u'OOHH':1118},u'TQ4':{u'BHHI':-887,u'BHII':-153,u'BIHH':-1077,u'BIIH':-460,u'BIII':958,u'BIIO':-1305,u'BIKK':-3204,u'BKKI':-4563,u'OHHI':1381,u'OIHH':2136,u'OIII':-1485,u'OIIK':270,u'OKII':1375,u'OKKK':-3574},u'TW1':{u'B1イヴ':2681,u'B1ネオ':2741,u'なみに':-863,u'ます。':-5031},u'TW2':{u'てこと':-876,u'として':-174,u'ゃあ、':-1661},u'TW3':{u'ていう':-2238},u'TW4':{u'とのこ':-922},u'UC1':{u'A':-1385,u'H':1007,u'N':149,u'O':1157},u'UC2':{u'A':1161,u'H':-620,u'N':57},u'UC3':{u'H':958,u'I':-228,u'N':44,u'O':5493},u'UC4':{u'H':753,u'I':250,u'K':-878,u'O':1763},u'UC5':{u'I':338,u'K':803,u'O':-156},u'UC6':{u'H':-168,u'I':-45,u'K':-623,u'N':303,u'O':351},u'UP1':{u'O':-193},u'UP2':{},u'UP3':{u'O':2532},u'UQ1':{u'BI':-315,u'BK':-2204,u'BN':449,u'OH':-188,u'OI':316,u'OO':220,u'UK':880},u'UQ2':{u'BK':-691,u'BN':490,u'BO':1046,u'OA':-771,u'OH':-986,u'OI':540,u'OK':372,u'OO':2922,u'UO':-6323},u'UQ3':{u'BH':-1477,u'BI':-429,u'BN':4482,u'BO':1807,u'OA':7327,u'OK':1005},u'UW1':{u'4':-796,u'B1':2389,u'G':-5712,u'L':-1656,u'『':-445,u'』':2954,u'あ':-587,u'お':-1163,u'こ':71,u'じ':-149,u'た':455,u'だ':230,u'っ':-469,u'て':756,u'と':-60,u'な':381,u'の':2327,u'も':-352,u'ゃ':44,u'よ':1310,u'れ':49,u'わ':1108,u'を':-777,u'ん':146,u'ア':-1682,u'シ':1158,u'ド':-1713,u'ネ':135,u'マ':362,u'ム':-594,u'ュ':-804,u'ン':-1601,u'ー':-1958,u'人':-346,u'何':2109,u'前':132,u'引':-314,u'Ｇ':4626,u'Ｍ':-1116,u'～':-3902},u'UW2':{u'M':-4821,u'…':1481,u'、':-2136,u'。':420,u'『':2370,u'い':192,u'う':96,u'か':43,u'が':916,u'く':-141,u'け':-57,u'こ':-287,u'し':-747,u'せ':514,u'そ':-622,u'た':2910,u'だ':1253,u'ち':-1411,u'つ':-778,u'て':4254,u'で':1380,u'と':496,u'ど':-880,u'な':-355,u'に':2817,u'の':3334,u'は':3595,u'み':-3389,u'め':-428,u'も':512,u'ゃ':-1414,u'よ':508,u'ら':-378,u'り':-2108,u'れ':687,u'わ':-1204,u'を':2162,u'ん':95,u'イ':408,u'ク':-2892,u'ド':-848,u'ム':1486,u'ン':-628,u'ヴ':1149,u'ー':-1019,u'人':515,u'何':3200,u'早':-308,u'見':-937,u'（':2099,u'）':2785,u'＊':-1938,u'～':-10099},u'UW3':{u'0':-2863,u'1':-678,u'4':1205,u'、':328,u'あ':402,u'い':-260,u'え':-942,u'お':1156,u'か':1148,u'が':4080,u'き':-1713,u'く':-799,u'け':-323,u'こ':-313,u'す':1057,u'ず':-226,u'せ':225,u'た':2161,u'だ':1666,u'ち':-2610,u'っ':-2793,u'て':5025,u'で':1080,u'と':1801,u'ど':-982,u'な':1262,u'に':4381,u'ね':3377,u'の':6111,u'は':5262,u'ま':-1137,u'み':-1792,u'め':-1589,u'も':1752,u'ゃ':-906,u'よ':3527,u'ら':-1349,u'り':-1344,u'る':-1682,u'れ':228,u'ろ':-591,u'わ':-645,u'を':6840,u'オ':1059,u'ク':-42,u'ト':5799,u'ド':-133,u'モ':176,u'ル':1357,u'ン':-1648,u'人':998,u'今':270,u'何':4004,u'使':-1344,u'同':791,u'宝':1564,u'感':-1301,u'様':-834},u'UW4':{u'、':2936,u'。':1187,u'』':-657,u'い':-1251,u'う':-1095,u'え':-572,u'が':1572,u'き':-334,u'く':-558,u'け':-751,u'こ':373,u'し':-440,u'す':-242,u'せ':-1229,u'そ':291,u'た':1847,u'だ':403,u'ち':-2273,u'っ':-661,u'つ':-1663,u'て':1685,u'で':902,u'と':1180,u'な':1520,u'に':1026,u'ね':1897,u'の':1833,u'は':1335,u'ま':258,u'め':-319,u'も':678,u'ゃ':-1225,u'ょ':-2300,u'よ':1304,u'ら':-1281,u'り':-3998,u'る':-1231,u'れ':-810,u'ろ':-2060,u'を':138,u'ん':-1760,u'ウ':714,u'ュ':-1961,u'ン':-182,u'ー':1404,u'出':-549,u'後':909,u'連':-308,u'（':-494,u'？':1382,u'～':-268},u'UW5':{u'E1':633,u'あ':1213,u'う':1469,u'こ':-198,u'し':-41,u'す':2875,u'ず':-666,u'そ':-185,u'ち':-852,u'っ':897,u'と':-385,u'な':-772,u'に':-252,u'め':810,u'も':527,u'ゃ':2466,u'ら':1049,u'る':784,u'れ':756,u'を':-586,u'ん':-43,u'ッ':484,u'ド':-362,u'ー':1008},u'UW6':{u'、':-561,u'』':-279,u'い':-214,u'う':-273,u'え':1226,u'か':161,u'が':478,u'く':-904,u'さ':-135,u'す':-997,u'ち':450,u'っ':481,u'な':258,u'に':113,u'ね':-441,u'の':-191,u'は':-682,u'よ':93,u'り':439,u'る':-471,u'シ':1115,u'ョ':-658,u'ロ':1043,u'ー':44,u'？':1110}}
    patterns = {
        u"[一二三四五六七八九十百千万億兆]":u"M",
        u"[一-龠々〆ヵヶ]":u"H",
        u"[ぁ-ん]":u"I",
        u"[ァ-ヴーｱ-ﾝﾞｰ]":u"K",
        u"[a-zA-Zａ-ｚＡ-Ｚ]":u"A",
        u"[0-9０-９]":u"N"
    };

    def __init__(self, model = None):
        self.model = model or self.default_model;

        chartype = [];
        for pattern, label in self.patterns.items():
            chartype.append([re.compile(pattern), label])
        self.chartype = chartype

    def getctype(self, str):
        for pattern, label in self.chartype:
            if pattern.match(str):
                return label
        return u"O"

    def segment(self, input):
        if not input:
            return []

        m = self.model
        result = []
        seg = [u"B3",u"B2",u"B1"]
        ctype = [u"O",u"O",u"O"]
        for ch in input:
            seg.append(ch)
            ctype.append(self.getctype(ch))
        seg.append(u"E1")
        seg.append(u"E2")
        seg.append(u"E3")
        ctype.append(u"O")
        ctype.append(u"O")
        ctype.append(u"O")
        word = seg[3]
        p1 = u"U"
        p2 = u"U"
        p3 = u"U"

        for i in xrange(4, len(seg)-3):
            score = m["BIAS"]
            w1 = seg[i-3]
            w2 = seg[i-2]
            w3 = seg[i-1]
            w4 = seg[i]
            w5 = seg[i+1]
            w6 = seg[i+2]
            c1 = ctype[i-3]
            c2 = ctype[i-2]
            c3 = ctype[i-1]
            c4 = ctype[i]
            c5 = ctype[i+1]
            c6 = ctype[i+2]
            score += m[u'UP1'].get(p1,0)
            score += m[u'UP2'].get(p2,0)
            score += m[u'UP3'].get(p3,0)
            score += m[u'BP1'].get(p1 + p2,0)
            score += m[u'BP2'].get(p2 + p3,0)
            score += m[u'UW1'].get(w1,0)
            score += m[u'UW2'].get(w2,0)
            score += m[u'UW3'].get(w3,0)
            score += m[u'UW4'].get(w4,0)
            score += m[u'UW5'].get(w5,0)
            score += m[u'UW6'].get(w6,0)
            score += m[u'BW1'].get(w2 + w3,0)
            score += m[u'BW2'].get(w3 + w4,0)
            score += m[u'BW3'].get(w4 + w5,0)
            score += m[u'TW1'].get(w1 + w2 + w3,0)
            score += m[u'TW2'].get(w2 + w3 + w4,0)
            score += m[u'TW3'].get(w3 + w4 + w5,0)
            score += m[u'TW4'].get(w4 + w5 + w6,0)
            score += m[u'UC1'].get(c1,0)
            score += m[u'UC2'].get(c2,0)
            score += m[u'UC3'].get(c3,0)
            score += m[u'UC4'].get(c4,0)
            score += m[u'UC5'].get(c5,0)
            score += m[u'UC6'].get(c6,0)
            score += m[u'BC1'].get(c2 + c3,0)
            score += m[u'BC2'].get(c3 + c4,0)
            score += m[u'BC3'].get(c4 + c5,0)
            score += m[u'TC1'].get(c1 + c2 + c3,0)
            score += m[u'TC2'].get(c2 + c3 + c4,0)
            score += m[u'TC3'].get(c3 + c4 + c5,0)
            score += m[u'TC4'].get(c4 + c5 + c6,0)
            score += m[u'UQ1'].get(p1 + c1,0)
            score += m[u'UQ2'].get(p2 + c2,0)
            score += m[u'UQ3'].get(p3 + c3,0)
            score += m[u'BQ1'].get(p2 + c2 + c3,0)
            score += m[u'BQ2'].get(p2 + c3 + c4,0)
            score += m[u'BQ3'].get(p3 + c2 + c3,0)
            score += m[u'BQ4'].get(p3 + c3 + c4,0)
            score += m[u'TQ1'].get(p2 + c1 + c2 + c3,0)
            score += m[u'TQ2'].get(p2 + c2 + c3 + c4,0)
            score += m[u'TQ3'].get(p3 + c1 + c2 + c3,0)
            score += m[u'TQ4'].get(p3 + c2 + c3 + c4,0)
            p = u"O"
            if score > 0:
                result.append(word)
                word = u""
                p = u"B"
            p1, p2, p3 = p2, p3, p
            word += seg[i]
        result.append(word)
        return result
