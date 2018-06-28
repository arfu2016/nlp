"""
@Project   : CubeGirl
@Module    : current_template.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/6/17 4:16 PM
@Desc      : 
"""


import os
import re
from pyltp import Segmentor, Postagger, Parser

from Daka.chatbot.logic.text_table.common.retrieve_template import \
    retrieve_tpl_from_file


def clean_sentence(st):

    in_tab = r'''[{}]'''
    out_tab = ' '
    # out_tab = 'p'
    clean = re.sub(in_tab, out_tab, st)
    return clean


def sentence_tokenization(tpl_list):
    data_tokenize = [(clean_sentence(tpl), intent) for tpl, intent in tpl_list]
    return data_tokenize


def parse_many_templates(templates):
    LTP_DATA_DIR = '/home/deco/projects/ltp_data/ltp_data_v3.4.0'
    # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    words = [segmentor.segment(tpl) for tpl in templates]  # 分词
    # for word in words:
    #     print('\t'.join(word))
    segmentor.release()  # 释放模型

    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = [postagger.postag(word) for word in words]  # 词性标注
    # for postag in postags:
    #     print('\t'.join(postag))
    postagger.release()  # 释放模型

    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
    # 依存句法分析模型路径，模型名称为`parser.model`
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = [parser.parse(word, postag) for word, postag in zip(words, postags)]
    # 句法分析
    # for arc_s in arcs:
    #     print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arc_s))
    parser.release()  # 释放模型

    class1 = 'person_info'
    class2 = 'team_info'
    class3 = 'citiao'
    categories = []
    for i in range(len(words)):
        word = words[i]
        word = list(word)
        # print(word)
        if 'PERSON' in word and '喜欢' in word:
            pi = word.index('PERSON')
            if arcs[i][pi].relation == 'SBV':
                categories.append(class3)
            elif arcs[i][pi].relation == 'VOB':
                categories.append(class1)
            else:
                categories.append(None)
        else:
            categories.append(None)
    return list(words), categories


def parse_one_template(tplate, segmentor, postagger, parser):
    words = segmentor.segment(tplate)  # 分词
    postags = postagger.postag(words)  # 词性标注
    arcs = parser.parse(words, postags)
    # 句法分析
    return words, postags, arcs


if __name__ == '__main__':

    tpl_intent = retrieve_tpl_from_file('data/tpls.csv')
    tpl_intent = [(tpl, intent) for tpl, intent in tpl_intent
                  if intent != 1 and intent != 2]
    # data = sentence_tokenization(tpl_intent[:3])
    data = sentence_tokenization(tpl_intent)

    # templates = [tpl.lower() for tpl, intent in data]
    templates = [tpl for tpl, intent in data]
    intentions = [intent for tpl, intent in data]

    # print("Some of templates and intentions:")
    # for tpl, intent in data:
    #     print(tpl, intent)

    # parse_many_templates(templates)

    LTP_DATA_DIR = '/home/deco/projects/ltp_data/ltp_data_v3.4.0'
    # ltp模型目录的路径
    cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    # 分词模型路径，模型名称为`cws.model`
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    # 词性标注模型路径，模型名称为`pos.model`
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
    # 依存句法分析模型路径，模型名称为`parser.model`
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型

    temp = '我不知道该问啥'
    # '我不知道该问啥'

    # ' PERSON 喜欢什么车' citiao
    # ' TEAM 的 PERSON 喜欢什么车'
    # '球员 PERSON 喜欢什么车'
    # '我的偶像 PERSON 喜欢什么车'
    # ' PERSON 喜欢干什么'

    # '我喜欢 PERSON ' person_info
    # '我喜欢球员 PERSON '
    # '我喜欢 TEAM 的 PERSON '
    # '我喜欢 TEAM PERSON '
    # '我喜欢老将 PERSON '
    # '我老板喜欢球员 PERSON '

    words, postags, arcs = parse_one_template(temp, segmentor, postagger,
                                              parser)

    segmentor.release()  # 释放模型
    postagger.release()
    parser.release()  # 释放模型
    # print('\t'.join(words))
    # print('\t'.join(postags))
    # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    class1 = 'person_info'
    class2 = 'team_info'
    class3 = 'citiao'
    category = None
    words = list(words)
    if 'PERSON' in words and '喜欢' in words:
        pi = words.index('PERSON')
        if arcs[pi].relation == 'SBV':
            category = class3
        elif arcs[pi].relation == 'VOB':
            category = class1
    print('\t'.join(words), ':', category)

    temp2 = [' PERSON 喜欢什么车', ' TEAM 的 PERSON 喜欢什么车',
             '球员 PERSON 喜欢什么车', '我的偶像 PERSON 喜欢什么车',
             ' PERSON 喜欢干什么', '我喜欢 PERSON ', '我喜欢球员 PERSON ',
             '我喜欢 TEAM 的 PERSON ', '我喜欢 TEAM PERSON ',
             '我喜欢老将 PERSON ', '我老板喜欢球员 PERSON ']
    words_list, categories_list = parse_many_templates(temp2)

    for words, category in zip(words_list, categories_list):
        # print(words, category)
        print('\t'.join(words), ':', category)
