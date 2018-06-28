"""
@Project   : CubeGirl
@Module    : intent_MLP.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/22/17 7:00 PM
@Desc      : 句子的特征词提取时考虑句法结构
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import pickle
import random
from collections import Counter

import os
import re
from pyltp import Segmentor, Postagger, Parser

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

from .load_template import load_tpl_from_csv

seaborn.set()  # For pretty plots
random.seed(0)  # 为了可追踪的随机性，固定随机种子


def clean_sentence(st):
    """
    数据预处理
    :param st: string
    :return: string
    """
    in_tab = r'''[{}]'''
    out_tab = ' '
    # out_tab = 'p'
    clean = re.sub(in_tab, out_tab, st)
    return clean


def train_validation(x_list, y_list):
    xx_train, xx_test, yy_train, yy_test = \
        train_test_split(x_list, y_list, test_size=0.33, random_state=0)
    return [xx_train, xx_test, yy_train, yy_test]


def compute_vocab(templates_c):
    """
    计算训练集中的词汇集合，给每个词汇分配在向量中的具体位置
    :param templates_c: list
    :return: list
    """
    total_counts = Counter()
    for tpl in templates_c:
        for word in tpl.split(" "):
            total_counts[word] += 1
    vocab = list(total_counts.keys())
    word2index = {}
    for i, word in enumerate(vocab):
        word2index[word] = i
    return word2index


def update_input_layer(reviews, word2index):
    """
    构造模型的输入层
    :param reviews: list
    :param vocab: list
    :param word2index: dict
    :return: np.ndarray
    """
    vocab_size = len(word2index)
    layer_0 = np.zeros((len(reviews), vocab_size))
    for i in range(len(reviews)):
        for word in reviews[i].split(" "):
            if word in word2index:
                layer_0[i][word2index[word]] = 1
    return layer_0


def intention_convert(intentions_i):
    """
    变换意图的标注
    :param intentions_i: list
    :return: list
    """
    intent_convert = {3: 0, 4: 1, 6: 2}
    return [intent_convert[intent] for intent in intentions_i]


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
        parse_result = [self.parse_one_template(tplate)
                        for tplate in templates]
        words_list, postags_list, arcs_list = zip(*parse_result)
        return words_list, postags_list, arcs_list

    def parse_one_template(self, tplate):
        question_clean = clean_sentence(tplate)
        words = self.segmentor.segment(question_clean)  # 分词
        postags = self.postagger.postag(words)  # 词性标注
        arcs = self.parser.parse(words, postags)
        # 句法分析
        return words, postags, arcs


class Components(object):
    def __init__(self, words, arcs):
        self.words = words
        self.arcs = arcs

    def get_next(self, word):
        arc_heads = [arc.head for arc in self.arcs]
        try:
            wi = self.words.index(word)
            return self.words[arc_heads[wi]-1]
        except ValueError:
            return None

    def get_head(self):
        arc_relations = [arc.relation for arc in self.arcs]
        si = arc_relations.index('HED')
        return self.words[si]

    def get_sbv(self):
        arc_heads = [arc.head for arc in self.arcs]
        arc_relations = [arc.relation for arc in self.arcs]
        arc_length = len(arc_relations)
        si = -1
        while True:
            try:
                si = arc_relations.index('SBV') + si + 1
                if self.words[arc_heads[si]-1] == self.get_head():
                    return self.words[si]
                if si + 1 < arc_length:
                    arc_relations = arc_relations[si + 1:]
                else:
                    return None
            except ValueError:
                return None

    def get_vob(self):
        arc_heads = [arc.head for arc in self.arcs]
        arc_relations = [arc.relation for arc in self.arcs]
        arc_length = len(arc_relations)
        si = -1
        while True:
            try:
                si = arc_relations.index('VOB') + si + 1
                if self.words[arc_heads[si] - 1] == self.get_head():
                    return self.words[si]
                if si + 1 < arc_length:
                    arc_relations = arc_relations[si + 1:]
                else:
                    return None
            except ValueError:
                return None


def key_words(words_list, postags_list, arcs_list):
    key_list = []
    question = ['什么', '谁', '多', '哪', '多少', '几']
    pos_list = ['n', 'nh', 'ni', 'nl', 'ns', 'nt', 'nz', 'v', 'a', 'd', 'm',
                'q', 'r', 'ws']
    for i in range(len(words_list)):
        words = list(words_list[i])
        postags = list(postags_list[i])
        words_useful = [words[i] for i in range(len(words)) if postags[i] in
                        pos_list]
        arcs = arcs_list[i]
        syn = Components(words, arcs)
        head = syn.get_head()
        sbv = syn.get_sbv()
        vob = syn.get_vob()
        inters = list(set(question).intersection(set(words)))
        next_words = [syn.get_next(inter) for inter in inters]
        next_words = [word for word in next_words if word is not None]
        next_next = [syn.get_next(word) for word in next_words]
        next_next = [word for word in next_next if word is not None]
        k_words = list({'PERSON', 'TEAM', 'CITIAO'}.intersection(set(words)))
        k_words.extend(inters)
        k_words.extend(next_words)
        k_words.extend(next_next)
        if head:
            k_words.append(head)
        if sbv:
            k_words.append(sbv)
        if vob:
            k_words.append(vob)
        k_words = list(set(k_words).intersection(set(words_useful)))
        # k_words = list(set(k_words))
        # print(k_words)
        key_list.append(' '.join(k_words))
    return key_list


def random_compliment(tpl_intent):
    tpl_intent = list(tpl_intent)
    person_ti = [(tpl, intent) for tpl, intent in tpl_intent if intent == 0]
    team_ti = [(tpl, intent) for tpl, intent in tpl_intent if intent == 1]
    citiao_ti = [(tpl, intent) for tpl, intent in tpl_intent if intent == 2]

    team_ti = [random.choice(team_ti) for _ in range(len(person_ti))]
    citiao_ti = [random.choice(citiao_ti) for _ in range(len(person_ti))]
    # 具有随机性

    person_ti.extend(team_ti)
    person_ti.extend(citiao_ti)
    tpl_intent = person_ti
    return tpl_intent


def select_words():
    judge_threshold = 0.85
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_dir, 'data/tpls.csv')

    tpl_intent = load_tpl_from_csv(file_name)
    tpl_intent = [(tpl, intent) for tpl, intent in tpl_intent
                  if intent == 3 or intent == 4 or intent == 6]

    print('原始数据：')
    for tpl, intent in tpl_intent:
        print(tpl, intent)

    templates, intentions = zip(*tpl_intent)
    intentions = intention_convert(intentions)
    word_lists0, postags_list0, arcs_list0 = \
        Syntactic().parse_many_templates(templates)
    templates = key_words(word_lists0, postags_list0, arcs_list0)

    intent_count = Counter()
    for intent in intentions:
        intent_count[intent] += 1
    print('intent_count:', intent_count)

    x_train, x_test, y_train, y_test = train_validation(templates, intentions)
    train_random = random_compliment(zip(x_train, y_train))
    x_train, y_train = zip(*train_random)
    test_random = random_compliment(zip(x_test, y_test))
    x_test, y_test = zip(*test_random)

    train_word2index = compute_vocab(x_train)
    layer_0_train = update_input_layer(x_train, train_word2index)
    clf1 = MLPClassifier(hidden_layer_sizes=64, activation='relu', alpha=0.01,
                         max_iter=1000, random_state=0)
    clf1.fit(layer_0_train, y_train)

    model_word = {'model': clf1, 'w2i': train_word2index}

    # save the model to disk
    file_pkl = os.path.join(file_dir, 'data/syntac_model180326.pkl')
    with open(file_pkl, 'wb') as f:
        pickle.dump(model_word, f)

    clf = clf1
    # _, x_test, _, y_test = train_validation(templates, intentions)
    layer_0_test = update_input_layer(x_test, train_word2index)
    print('Accuracy of the validation data:',
          clf.score(layer_0_test, y_test), '\n')

    predictions = clf.predict_proba(layer_0_test).tolist()
    indexes = np.argmax(predictions, axis=1).tolist()
    values = [prediction[index] for prediction, index
              in zip(predictions, indexes)]
    wrong = [values[i] for i in range(len(values)) if indexes[i] != y_test[i]]
    print('The predicted probabilities of wrongly classified samples:\n',
          wrong, '\n')
    test_total = len(x_test)
    wrong_number_still = len([ele for ele in wrong if ele >= judge_threshold])
    print('If the threshold for probabilities is set to {:.2f},'.format(
        judge_threshold))
    print('Accuracy of classified validation data:',
          (test_total - wrong_number_still) / test_total)
    print('Proportion of unclassified validation data:',
          (len(wrong) - wrong_number_still) / test_total)

    test_true_labels = y_test
    test_eff_predict_labels = indexes
    labels_list = [0, 1, 2]
    conf_mat = confusion_matrix(test_true_labels, test_eff_predict_labels,
                                labels=labels_list)
    conf_mat = conf_mat / conf_mat.astype(np.float).sum(axis=1)
    conf_df = pd.DataFrame(conf_mat * 100, index=labels_list,
                           columns=labels_list)
    fig, ax = plt.subplots(figsize=(8, 6))
    seaborn.heatmap(conf_df, annot=True, ax=ax)
    plt.show()
    # the vertical labels are true labels,
    # and the horizontal labels are predicted labels

    # fig.savefig('data/confusion_matrix.png', bbox_inches='tight',
    #             pad_inches=0, dpi=500, format='png')
