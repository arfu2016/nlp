"""
@Project   : CubeGirl
@Module    : ltp_basic.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/4/18 4:57 PM
@Desc      : 
"""
import os
from pyltp import (Segmentor,
                   Postagger,
                   Parser,
                   NamedEntityRecognizer,
                   SementicRoleLabeller)


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
    def __init__(self):
        ltp_data_dir = dirname(__file__, 6) + "/data/ltp_data_v3.4.0"
        # ltp模型目录的路径
        cws_model_path = os.path.join(ltp_data_dir, 'cws.model')
        # 分词模型路径，模型名称为`cws.model`
        ltp_word_dir = os.path.dirname(os.path.abspath(__file__))
        ltp_word_path = os.path.join(ltp_word_dir, 'data/dict_template')
        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load_with_lexicon(cws_model_path, ltp_word_path)

        pos_model_path = os.path.join(ltp_data_dir, 'pos.model')
        # 词性标注模型路径，模型名称为`pos.model`
        ltp_postag_path = os.path.join(ltp_word_dir, 'data/postags')
        self.postagger = Postagger()  # 初始化实例
        self.postagger.load_with_lexicon(pos_model_path, ltp_postag_path)

        ner_model_path = os.path.join(ltp_data_dir, 'ner.model')
        # 命名实体识别模型路径，模型名称为`pos.model`
        self.recognizer = NamedEntityRecognizer()  # 初始化实例
        self.recognizer.load(ner_model_path)  # 加载模型

        par_model_path = os.path.join(ltp_data_dir, 'parser.model')
        # 依存句法分析模型路径，模型名称为`parser.model`
        self.parser = Parser()  # 初始化实例
        self.parser.load(par_model_path)  # 加载模型

        srl_model_path = os.path.join(ltp_data_dir, 'pisrl.model')
        # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
        self.labeller = SementicRoleLabeller()  # 初始化实例
        self.labeller.load(srl_model_path)  # 加载模型

    def model_close(self):
        self.segmentor.release()  # 释放模型
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()
        self.labeller.release()


ltp_basic = Syntactic()
# Syntactic类的单例
