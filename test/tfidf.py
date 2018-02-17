#-*- coding: utf-8 -*-
#

import numpy as np
import scipy.sparse as sparse
from sklearn.feature_extraction.text import TfidfVectorizer

import matplotlib.pyplot as plt

def draw_heatmap(data):
    plt.imshow(data, cmap='hot',interpolation='nearest')
    plt.show()


data = [
  "The scottish fold family we rescued . We are so happy to be",
  "I found ubuntu 14.04 trusty 32bit is executable on VAIO H30B",
  "hello ! there ! I am researcher of chatbot in japan",
  "How much ram do you have?",
  "It seems it comes with 256-MB DDR1 synchronous DRAM (SDRAM) at 333 MHz",
  "Do you have all the specs for this computer?",

]

tv = TfidfVectorizer()
wv = tv.fit_transform(data)
cv = np.zeros(wv.shape)

# print tv.vocabulary_
# print tv.idf_

print "original wv: ",wv.shape

w=sparse.vstack([wv[-1],wv,wv[0]])

w = w.T
w=w.todense()
print "sizeof w=",w.shape
# draw_heatmap(wv)

K = np.array([0.5,1,0])

for i in range(cv.shape[1]):
    ww=np.squeeze(np.asarray(w[i]))
    cv[:,i] = np.convolve(ww,K,mode='valid').transpose()

draw_heatmap(cv)

def log
