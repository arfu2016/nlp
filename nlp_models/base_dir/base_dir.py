"""
@Project   : text-classification-cnn-rnn
@Module    : data_explore.py
@Author    : Deco [deco@cubee.com]
@Created   : 5/22/18 11:13 AM
@Desc      : 
"""

import os
import sys

base_dir = os.path.dirname(os.path.dirname(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from data.prepare import load_raw
