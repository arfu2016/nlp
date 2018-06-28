"""
@Project   : CubeGirl
@Module    : depy_sen_parser.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/24/18 1:07 PM
@Desc      : single instance of sentence parser
问题的重要特征：分词结果，词性分析结果，句法分析结果
词法分析：词性分析，词干(word stemming for English)提取等
"""
import os
from pyltp import Segmentor, Postagger, Parser
from .depy_tools import clean_sentence


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


class Syntactic:
    """Base class to construct parse trees"""

    stop_words = ('的', '中', '了', '已经', '所属', '也', '还', '名',
                  '个', '次', '过', '啊', '呀', '呢', '于')
    # 在充当动词：哈里马奎尔第一次代表国家队出场在什么时候
    # 所属球队：不再作为分词文件中的一个词

    def __init__(self):
        ltp_data_dir = dirname(__file__, 6) + "/data/ltp_data_v3.4.0"
        # ltp模型目录的路径
        cws_model_path = os.path.join(ltp_data_dir, 'cws.model')
        # 分词模型路径，模型名称为`cws.model`
        ltp_word_dir = os.path.dirname(os.path.abspath(__file__))
        ltp_word_path = os.path.join(ltp_word_dir, 'dict_template')
        self.segmentor = Segmentor()  # 初始化实例
        # self.segmentor.load(cws_model_path)  # 加载普通模型
        self.segmentor.load_with_lexicon(cws_model_path, ltp_word_path)

        pos_model_path = os.path.join(ltp_data_dir, 'pos.model')
        # 词性标注模型路径，模型名称为`pos.model`
        ltp_postag_path = os.path.join(ltp_word_dir, 'postags')
        self.postagger = Postagger()  # 初始化实例
        # self.postagger.load(pos_model_path)  # 加载普通模型
        self.postagger.load_with_lexicon(pos_model_path, ltp_postag_path)

        par_model_path = os.path.join(ltp_data_dir, 'parser.model')
        # 依存句法分析模型路径，模型名称为`parser.model`
        self.parser = Parser()  # 初始化实例
        self.parser.load(par_model_path)  # 加载模型

    def model_close(self):
        self.segmentor.release()  # 释放模型
        self.postagger.release()
        self.parser.release()

    def parse_one_template(self, tplate):
        question_clean = clean_sentence(tplate)
        words = self.segmentor.segment(question_clean)  # 分词
        words = [word for word in words if word not in self.stop_words]
        postags = list(self.postagger.postag(words))  # 词性标注
        arcs = list(self.parser.parse(words, postags))
        # 句法分析
        return words, postags, arcs

    def parse_many_templates(self, templates):
        parse_result = [self.parse_one_template(tplate)
                        for tplate in templates]
        words_list, postags_list, arcs_list = zip(*parse_result)
        return words_list, postags_list, arcs_list


sen_parser = Syntactic()
# Syntactic类的单例
