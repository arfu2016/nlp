"""
@Project   : CubeGirl
@Module    : intent_svm.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/22/17 1:07 AM
@Desc      : 
"""

import string
from collections import Counter

import jieba
import jieba.analyse
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from Daka.chatbot.logic.text_table.word_vec.retrieve_template import \
    retrieve_tpl_from_file


def clean_sentence(st):
    intab = string.punctuation + '。，“”‘’（）：；？·—《》、'
    outtab = ' '
    table = str.maketrans(dict.fromkeys(intab, outtab))
    st1 = st.translate(table)
    tags = jieba.analyse.extract_tags(st1, topK=100,
                          allowPOS=('eng', 'n', 'ns', 'nr', 'nt', 'nz', 'vn'))
    clean = ' '.join(tags)
    # 把列表换成字符串
    return clean


def sentence_tokenization(tpl_list):
    data_tokenized = [(clean_sentence(tpl), intent)
                      for tpl, intent in tpl_list]
    return data_tokenized


def train_validation(X_list, y_list):
    X_train, X_test, y_train, y_test = train_test_split(X_list, y_list,
                                                        test_size=0.33,
                                                        random_state=6)
    return [X_train, X_test, y_train, y_test]


def compute_vocab(templates):
    total_counts = Counter()
    for tpl in templates:
        for word in tpl.split(" "):
            total_counts[word] += 1
    vocab = set(total_counts.keys())
    word2index = {}
    for i, word in enumerate(vocab):
        word2index[word] = i
    return [vocab, word2index]


def update_input_layer(reviews, vocab, vocab_size, word2index):
    layer_0 = np.zeros((len(reviews), vocab_size))
    for i in range(len(reviews)):
        for word in reviews[i].split(" "):
            if word in vocab:
                layer_0[i][word2index[word]] = 1
    return layer_0


def intention_convert(intentions):
    intentions2 = []
    for intention in intentions:
        if intention == 3:
            intentions2.append(0)
        elif intention == 4:
            intentions2.append(1)
        else:
            intentions2.append(2)
    return intentions2


if __name__ == "__main__":
    judge_threshold = 0.85
    n_classes = 3
    tpl_intent = retrieve_tpl_from_file('data/tpls.csv')
    tpl_intent = [(tpl, intent) for tpl, intent in tpl_intent
                  if intent != 1 and intent != 2]
    data = sentence_tokenization(tpl_intent)
    templates = [tpl for tpl, intent in data]
    intentions = [intent for tpl, intent in data]
    intentions = intention_convert(intentions)
    x_train, x_test, y_train, y_test = train_validation(templates, intentions)
    vocab_train, train_word2index = compute_vocab(x_train)
    vocab_size_train = len(vocab_train)
    layer_0_train = update_input_layer(x_train, vocab_train, vocab_size_train,
                                       train_word2index)
    layer_0_test = update_input_layer(x_test, vocab_train, vocab_size_train,
                                      train_word2index)
    # svcreg = SVC(decision_function_shape='ovo')
    svcreg = SVC(decision_function_shape='ovr')
    svcreg.fit(layer_0_train, y_train)
    print('Accuracy of the validation data:',
          svcreg.score(layer_0_test, y_test), '\n')
