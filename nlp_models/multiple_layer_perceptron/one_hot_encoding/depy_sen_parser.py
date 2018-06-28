"""
@Project   : CubeGirl
@Module    : depy_sen_parser.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/24/18 1:07 PM
@Desc      : 句法分析的single instance
"""
import os
import jieba
from pyltp import Segmentor, Postagger, Parser


def dirname(path, up):
    """
    根据路径字符串，返回指定层数的上一级路径
    :param path: 路径字符串
    :param up: int，指定层数
    :return: 路径字符串
    """
    for i in range(up):
        path = os.path.dirname(path)
    return path


class SyntacticJieba:
    """Base class to construct parse trees"""

    stopWords = ['的', '在', '中']

    def __init__(self):
        ltp_data_dir = dirname(__file__, 6) + "/data/ltp_data_v3.4.0"
        # ltp模型目录的路径
        ltp_word_dir = os.path.dirname(os.path.abspath(__file__))
        jieba_word_path = os.path.join(ltp_word_dir, 'data/jieba_userdict.txt')
        jieba.load_userdict(jieba_word_path)

        pos_model_path = os.path.join(ltp_data_dir, 'pos.model')
        # 词性标注模型路径，模型名称为`pos.model`
        ltp_postag_path = os.path.join(ltp_word_dir, 'data/postags')
        self.postagger = Postagger()  # 初始化实例
        # self.postagger.load(pos_model_path)  # 加载模型
        self.postagger.load_with_lexicon(pos_model_path, ltp_postag_path)

        par_model_path = os.path.join(ltp_data_dir, 'parser.model')
        # 依存句法分析模型路径，模型名称为`parser.model`
        self.parser = Parser()  # 初始化实例
        self.parser.load(par_model_path)  # 加载模型

    def model_close(self):
        self.postagger.release()
        self.parser.release()

    def cut_jieba(self, st):
        filter_seg = filter(
            lambda x: x not in self.stopWords and len(x.strip()) > 0,
            jieba.cut(st))
        return list(filter_seg)

    def parse_many_templates(self, templates):
        words_list = [self.cut_jieba(tpl) for tpl in templates]  # 分词
        postags_list = [self.postagger.postag(word) for word in words_list]
        # 词性标注
        arcs_list = [self.parser.parse(words, postags) for words, postags in
                     zip(words_list, postags_list)]
        return words_list, postags_list, arcs_list

    def parse_one_template(self, tplate):
        words = self.cut_jieba(tplate)  # 分词
        postags = self.postagger.postag(words)  # 词性标注
        arcs = self.parser.parse(words, postags)
        # 句法分析
        return words, postags, arcs


sen_parser = SyntacticJieba()
# Syntactic类的单例
