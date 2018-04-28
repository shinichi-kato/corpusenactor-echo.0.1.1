# -*- coding: utf-8 -*-
"""
tfidf visualizer
"""
import matplotlib
import matplotlib.pyplot as plt
from corpusenactor.echo import Echo

ce = Echo('chatbot/chatbot.yaml',nocache=True)

ce.corpus_to_tfidf()
plt.imshow(ce.copus_tfidf)
plt.show()



"""
transpost->convolve->transpose
"""
