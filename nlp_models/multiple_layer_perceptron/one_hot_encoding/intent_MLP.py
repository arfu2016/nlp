"""
@Project   : CubeGirl
@Module    : intent_MLP.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/22/17 7:00 PM
@Desc      : 用jieba进行句子的特征词提取
"""

import os
import pickle
import string
from collections import Counter

import jieba
import jieba.analyse
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from .load_template import load_tpl_from_csv


def clean_sentence(st):
    """
    分词及词性标注
    :param st: string
    :return: string
    """
    intab = string.punctuation + '。，“”‘’（）：；？·—《》、'
    outtab = ' '
    table = str.maketrans(dict.fromkeys(intab, outtab))
    # str.maketrans做的相当于ord的事情，把字符转成对应的unicode编码
    st1 = st.translate(table)
    tags = jieba.analyse.extract_tags(st1, topK=100,
                                      allowPOS=(
                                          'eng', 'n', 'ns', 'nr', 'nt', 'nz',
                                          'vn'))
    # 一方面，用tf-idf提取句中关键词，另一方面，只取句中的英文和名词
    clean = ' '.join(tags)
    # 把列表换成字符串， 与英文格式一致
    return clean


def sentence_tokenization(tpl_list):
    """把中文数据英文化"""
    data_tokenized = [(clean_sentence(tpl), intent)
                      for tpl, intent in tpl_list]
    return data_tokenized


def train_val_split(x_list, y_list):
    x_train, x_test, y_train, y_test = train_test_split(x_list, y_list,
                                                        test_size=0.33,
                                                        random_state=0)
    # test_size是test比例，random_state是做随机分配的种子
    train_and_test = [x_train, x_test, y_train, y_test]
    return train_and_test


def compute_vocab(templates):
    """
    计算训练集中的词汇集合，给每个词汇分配在向量中的具体位置
    :param templates: list
    :return: dict
    """
    total_counts = Counter()
    for tpl in templates:
        for word in tpl.split(" "):
            total_counts[word] += 1
    vocab = list(total_counts.keys())
    word2index = {word: i for i, word in enumerate(vocab)}
    return word2index


def update_input_layer(reviews, word2index):
    """
    构造模型的输入层
    :param reviews: list, list of sentences
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


def intention_convert(intentions):
    """
    变换意图的标注
    :param intentions: list
    :return: list
    """
    mapping = {3: 0, 4: 1, 6: 2}
    intent_s = [mapping[intent] for intent in intentions]
    return intent_s


def select_words():
    judge_threshold = 0.85
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_dir, 'data/tpls.csv')

    tpl_intent = load_tpl_from_csv(file_name)
    tpl_intent = [(tpl, intent) for tpl, intent in tpl_intent
                  if intent == 3 or intent == 4 or intent == 6]

    # for tpl, intent in tpl_intent:
    #     print(tpl, intent)

    data = sentence_tokenization(tpl_intent)
    templates, intentions = zip(*data)
    intentions = intention_convert(intentions)
    x_train, x_test, y_train, y_test = train_val_split(templates, intentions)
    train_word2index = compute_vocab(x_train)
    layer_0_train = update_input_layer(x_train, train_word2index)
    clf1 = MLPClassifier(hidden_layer_sizes=64, activation='relu', alpha=0.01,
                         max_iter=1000, random_state=0)
    # 64 hidden units, alpha is learning rate, at most 1000 epochs
    # a single batch, random_state is for initialization of weights
    clf1.fit(layer_0_train, y_train)
    model_word = {'model': clf1, 'w2i': train_word2index}

    # save the model to disk
    file_pkl = os.path.join(file_dir, 'data/MLP_model180326.pkl')
    with open(file_pkl, 'wb') as f:
        pickle.dump(model_word, f)

    # load the model from disk
    # with open(filename, 'rb') as f:
    #     model_word = pickle.load(f)

    clf = clf1
    # _, x_test, _, y_test = train_val_split(templates, intentions)
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
