# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import os
import cloudstorage as gcs

from google.appengine.api import app_identity

retry_params = gcs.RetryParams(
  initial_delay = 0.2,
  max_delay = 5.0,
  backoff_factor = 2,
  max_retry_perios=15
)
gcs.set_default_retry_params(retry_params)

def get_bucket_name
