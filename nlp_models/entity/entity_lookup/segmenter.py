"""
@Project   : CubeGirl
@Module    : segmenter.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/4/18 3:16 PM
@Desc      : 
"""
import os
import jieba


class SegmenterJieba:
    stop_words = ['的', '在', '中']

    def __init__(self):
        ltp_word_dir = os.path.dirname(os.path.abspath(__file__))
        jieba_word_path = os.path.join(ltp_word_dir, 'data/jieba_userdict.txt')
        jieba.load_userdict(jieba_word_path)

    def cut(self, st):
        words = [word for word in jieba.cut(st)
                 if word not in self.stop_words]
        return words


seg_jieba = SegmenterJieba()
