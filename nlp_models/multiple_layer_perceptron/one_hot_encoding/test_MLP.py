"""
@Project   : CubeGirl
@Module    : test_MLP.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/27/17 1:26 AM
@Desc      : 
"""

import jieba
import jieba.analyse
import string
import pickle
import numpy as np
import os


def clean_sentence(st):
    """
    分词及词性标注
    :param st: string
    :return: string
    """
    intab = string.punctuation + '。，“”‘’（）：；？·—《》、'
    outtab = ' '
    table = str.maketrans(dict.fromkeys(intab, outtab))
    st1 = st.translate(table)
    tags = jieba.analyse.extract_tags(st1, topK=100,
                                      allowPOS=[
                                          'eng', 'n', 'ns', 'nr', 'nt', 'nz',
                                          'vn'])
    # 'v', 'vg', 'vd', 'vn'
    # 'a', 'ad', 'an', 'Ag'
    # 'd', 'dg'
    clean = ' '.join(tags)
    # 把列表换成字符串， 与英文格式一致
    return clean


def sentence_tokenization(tpl_list):
    """
    模板转换为token序列
    :param tpl_list: list
    :return: list
    """
    data_tokenized = [clean_sentence(tpl) for tpl in tpl_list]
    return data_tokenized


def update_input_layer(reviews, word2index):
    """
    构造模型的输入层
    :param reviews: list
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


class IntentClassify:
    set_threshold = 0.85
    file_dir = os.path.dirname(os.path.abspath(__file__))
    # file_name = os.path.join(file_dir, 'data/MLP_model180326.pkl')
    file_name = os.path.join(file_dir, 'data/syntac_model180326.pkl')
    con_dict = {0: 3, 1: 4, 2: 6}

    def __init__(self):
        with open(self.file_name, 'rb') as f:
            model_word = pickle.load(f)
            self.model = model_word['model']
            self.train_word2index = model_word['w2i']

    def input_compute(self, tpl_list):
        """
        从模板计算意图类别
        """
        templates = sentence_tokenization(tpl_list)
        # 从性能考虑的话，在test中，可以利用词性而不是句法来选取待分析的特征词

        x_test = templates
        # y_test = None
        layer_0_test = update_input_layer(x_test, self.train_word2index)
        predictions = self.model.predict_proba(layer_0_test).tolist()
        indexes = np.argmax(predictions, axis=1).tolist()
        values = [prediction[index] for prediction, index
                  in zip(predictions, indexes)]
        indexes = [self.con_dict[intent] for intent in indexes]
        indexes0 = indexes[:]
        for i in range(len(values)):
            if values[i] < self.set_threshold:
                indexes[i] = None
        return indexes0, values, indexes


intent_classifier = IntentClassify()


def wrapper(func, *args, **kwargs):
    """
    一个装饰器，用来把有参数的函数转换为没有参数的函数
    :param func: func
    :param args: list
    :param kwargs: dict
    :return: func
    """
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


if __name__ == "__main__":

    tpl_test = ['{PERSON}喜欢什么车', '{PERSON}是不是个好球员', '{PERSON}的故事',
                '{PERSON}的八卦', '我想了解{TEAM}', '我想知道{TEAM}的情况',
                '问一下{TEAM}的教练是谁', '{TEAM}的{PERSON}', '{TEAM}的历史',
                '{TEAM}的故事', '你知道什么', '你好', '谢谢', '再见', '小美',
                '爱球', '今天天气怎么样']
    ori_class, intent_prob, intent_class = \
        intent_classifier.input_compute(tpl_test)

    print('The original predicted intentions of the input templates:\n',
          ori_class)
    print('The probabilities of predicted intentions:\n', intent_prob)
    print('If the threshold for probabilities is set to {:.2f},'.format(
        intent_classifier.set_threshold))
    print('the predicted intentions of the input templates:\n', intent_class,
          '\n')

    import timeit
    iterations = 10
    wrapped_time = wrapper(intent_classifier.input_compute, tpl_test)
    print('Time cost:',
          timeit.timeit(wrapped_time, number=iterations) / iterations)
