"""
@Project   : CubeGirl
@Module    : syntactic_model.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/11/17 1:17 PM
@Desc      : 
"""

import os
import re
from pyltp import Segmentor, Postagger, Parser


def clean_sentence(st):
    in_tab = r'''[{}]'''
    out_tab = ' '
    clean = re.sub(in_tab, out_tab, st)
    return clean


def clean_templates(templates):
    return [clean_sentence(tpl) for tpl in templates]


class Syntactic(object):

    class_person = 'person_info'
    class_team = 'team_info'
    class_citiao = 'citiao'

    def __init__(self):
        LTP_DATA_DIR = '/home/deco/projects/ltp_data/ltp_data_v3.4.0'
        # ltp模型目录的路径
        cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
        # 分词模型路径，模型名称为`cws.model`
        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load(cws_model_path)  # 加载模型

        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
        # 词性标注模型路径，模型名称为`pos.model`
        self.postagger = Postagger()  # 初始化实例
        self.postagger.load(pos_model_path)  # 加载模型

        par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
        # 依存句法分析模型路径，模型名称为`parser.model`
        self.parser = Parser()  # 初始化实例
        self.parser.load(par_model_path)  # 加载模型

    def model_close(self):
        self.segmentor.release()  # 释放模型
        self.postagger.release()
        self.parser.release()

    def parse_many_templates(self, templates):
        words_list = [self.segmentor.segment(tpl) for tpl in templates]  # 分词
        postags_list = [self.postagger.postag(word) for word in words_list]
        # 词性标注
        arcs_list = [self.parser.parse(words, postags) for words, postags in
                     zip(words_list, postags_list)]
        return words_list, postags_list, arcs_list

    def parse_one_template(self, tplate):
        words = self.segmentor.segment(tplate)  # 分词
        postags = self.postagger.postag(words)  # 词性标注
        arcs = self.parser.parse(words, postags)
        # 句法分析
        return words, postags, arcs


class TemplatesInterpret(Syntactic):
    def __init__(self, templates):
        Syntactic.__init__(self)
        self.templates = templates

    def interpret(self):
        tpls_clean = clean_templates(self.templates)
        words_list, postags_list, arcs_list = \
            self.parse_many_templates(tpls_clean)
        # print([list(words) for words in words_list])
        # print([["%d:%s" % (arc.head, arc.relation) for arc in arcs]
        #        for arcs in arcs_list])
        categories = [self.rule(list(words_list[i]), arcs_list[i])
                      for i in range(len(words_list))]
        return categories

    def rule(self, words, arcs):
        """根据句法树编写的意图分类规则，需要具体实现"""


class OneTerm(object):
    def __init__(self, term, words, arcs):
        self.term = term
        self.words = words
        self.arcs = arcs

    def hed(self):
        arc_relations = [arc.relation for arc in self.arcs]
        si = arc_relations.index('HED')
        return self.words[si] == self.term


class TwoTerms(object):
    def __init__(self, term, words, arcs):
        self.term1 = term[0]
        self.term2 = term[1]
        self.words = words
        self.arcs = arcs

    def sbv(self):
        arc_heads = [arc.head for arc in self.arcs]
        arc_relations = [arc.relation for arc in self.arcs]
        arc_length = len(arc_relations)
        si = -1
        while True:
            try:
                si = arc_relations.index('SBV') + si + 1
                if self.words[si] == self.term1 and \
                        self.words[arc_heads[si]-1] == self.term2:
                    return True
                if si + 1 < arc_length:
                    arc_relations = arc_relations[si + 1:]
                else:
                    return False
            except ValueError:
                return False

    def vob(self):
        arc_heads = [arc.head for arc in self.arcs]
        arc_relations = [arc.relation for arc in self.arcs]
        arc_length = len(arc_relations)
        si = -1
        while True:
            try:
                si = arc_relations.index('VOB') + si + 1
                if self.words[si] == self.term2 and \
                        self.words[arc_heads[si] - 1] == self.term1:
                    return True
                if si + 1 < arc_length:
                    arc_relations = arc_relations[si + 1:]
                else:
                    return False
            except ValueError:
                return False
