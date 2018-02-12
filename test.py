#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import tinysegmenter
segmenter = tinysegmenter.TinySegmenter()
print("|".join(segmenter.segment('形態素解析をテストする')))
