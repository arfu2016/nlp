"""
@Project   : CubeGirl
@Module    : intent_classification.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/20/17 1:06 AM
@Desc      : 
"""

# from .retrieve_template import retrieve_template

import string
from collections import Counter

import jieba
import jieba.analyse
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from Daka.chatbot.logic.text_table.word_vec.retrieve_template import \
    retrieve_tpl_from_file


def intent_counts(tpl_list):
    intent_fre = Counter()
    for tpl, intent in tpl_list:
        intent_fre[intent] += 1
    return intent_fre


def clean_sentence(st):
    intab = string.punctuation + '。，“”‘’（）：；？·—《》、'
    outtab = ' '
    table = str.maketrans(dict.fromkeys(intab, outtab))
    st1 = st.translate(table)
    tags = jieba.analyse.extract_tags(st1, topK=100,
            allowPOS=('eng', 'n', 'ns', 'nr', 'nt', 'nz', 'vn'))
    # allowPOS=('eng', 'n', 'v', 'ns', 'nr', 'nt', 'nz', 'vd', 'vn'))
    clean = ' '.join(tags)
    # 可以使用字符串或者列表
    return clean


def sentence_tokenization(tpl_list):
    # t_start = time.time()
    data_tokenized = [(clean_sentence(tpl), intent) for tpl, intent in tpl_list]
    # t_end = time.time()
    # elapsed_time = float(t_end - t_start)/60
    # print(elapsed_time)
    return data_tokenized


# nn_classes = 3
def one_hot_encode(x, nn_classes):
    """
    One hot encode a list of sample labels. Return a one-hot encoded vector for each label.
    : x: List of sample Labels
    : return: Numpy array of one-hot encoded labels
    """
    # TODO: Implement Function
    # n_values = np.max(x) + 1
    # return np.eye(n_values, dtype=int)[x]
    return np.eye(nn_classes)[x]


def neural_net_sentence_input(input_shape):
    """
    Return a Tensor for a batch of image input
    : image_shape: Shape of the images
    : return: Tensor for image input.
    """
    # TODO: Implement Function
    return tf.placeholder(tf.float32, [None, input_shape], name='x')


def neural_net_label_input(n_classes):
    """
    Return a Tensor for a batch of label input
    : n_classes: Number of classes
    : return: Tensor for label input.
    """
    # TODO: Implement Function
    return tf.placeholder(tf.float32, [None, n_classes], 'y')


def output(x_tensor, num_outputs):
    """
    Apply a output layer to x_tensor using weight and bias
    : x_tensor: A 2-D tensor where the first dimension is batch size.
    : num_outputs: The number of output that the new tensor should be.
    : return: A 2-D tensor where the second dimension is num_outputs.
    """
    # TODO: Implement Function
    return tf.layers.dense(x_tensor, num_outputs)


def neural_net(x, nn_classes):
    out = output(x, nn_classes)

    # TODO: return output
    return out


def train_validation(X_list, y_list):
    X_train, X_test, y_train, y_test = train_test_split(X_list, y_list,
                                                        test_size=0.33,
                                                        random_state=42)
    return [X_train, X_test, y_train, y_test]


def compute_vocab_size(templates):
    total_counts = Counter()
    for tpl in templates:
        for word in tpl.split(" "):
            total_counts[word] += 1
    # print(total_counts)
    '''
    total_counts2 = Counter()
    for term, cnt in total_counts.items():
        if cnt > 1:
           total_counts2[term] = cnt
    total_counts = total_counts2
    '''
    vocab = set(total_counts.keys())
    vocab_size = len(vocab)
    word2index = {}
    for i, word in enumerate(vocab):
        word2index[word] = i
    return [vocab, word2index]


def update_input_layer(reviews, vocab, vocab_size, word2index):
    """ Modify the global layer_0 to represent the vector form of review.
    The element at a given index of layer_0 should represent
    how many times the given word occurs in the review.
    Args:
        review(string) - the string of the review
    Returns:
        None
    """
    # global layer_0
    layer_0 = np.zeros((len(reviews), vocab_size))

    # clear out previous state, reset the layer to be all 0s
    # layer_0 *= 0

    # count how many times each word is used in the given review and store the results in layer_0
    for i in range(len(reviews)):
        for word in reviews[i].split(" "):
            if word in vocab:
            # layer_0[0][word2index[word]] += 1
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

def train_neural_network(session, optimizer,
                         feature_batch, label_batch):
    """
    Optimize the session on a batch of images and labels
    : session: Current TensorFlow session
    : optimizer: TensorFlow optimizer function
    : keep_probability: keep probability
    : feature_batch: Batch of Numpy image data
    : label_batch: Batch of Numpy label data
    """
    # TODO: Implement Function
    session.run(optimizer, feed_dict={
        x: feature_batch,
        y: label_batch})

def print_stats(session, feature_batch, label_batch, cost, accuracy,
                valid_features, valid_labels):
    """
    Print information about loss and validation accuracy
    : session: Current TensorFlow session
    : feature_batch: Batch of Numpy image data
    : label_batch: Batch of Numpy label data
    : cost: TensorFlow cost function
    : accuracy: TensorFlow accuracy function
    """
    # TODO: Implement Function
    loss = session.run(cost, feed_dict={
        x: feature_batch,
        y: label_batch})
    valid_acc = session.run(accuracy, feed_dict={
        x: valid_features,
        y: valid_labels})

    print('Loss: {:>2.4f} Validation Accuracy: {:.6f}'.format(
        loss, valid_acc))


if __name__ == "__main__":
    tpl_intent = retrieve_tpl_from_file('data/tpls.csv')
    tpl_intent = [(tpl, intent) for tpl, intent in tpl_intent
                  if intent != 1 and intent != 2]
    # print(intent_counts(tpl_intent))
    data = sentence_tokenization(tpl_intent)
    '''
    for tpl, intent in data:
        if intent == 3:
            print(tpl)
    '''
    templates = [tpl for tpl, intent in data]
    # print(len(templates))
    intentions = [intent for tpl, intent in data]
    intentions = intention_convert(intentions)
    # print(len(intentions))
    x_train, x_test, y_train, y_test = train_validation(templates, intentions)
    # print(x_train)
    # print(y_train)
    # print(x_test)
    # print(y_test)
    '''
    ws = pseg.cut('我想问 TEAM 的主场')
    print(list(ws))
    for tpl in templates:
        print(list(pseg.cut(tpl)))
    '''
    vocab_train, train_word2index = compute_vocab_size(x_train)
    vocab_size_train = len(vocab_train)
    # print(layer_0.shape)
    layer_0_train = update_input_layer(x_train, vocab_train, vocab_size_train,
                                       train_word2index)
    print('Training data shape:', layer_0_train.shape)
    # vocab_test, test_word2index = compute_vocab_size(x_test)
    # vocab_size_test = len(vocab_test)
    layer_0_test = update_input_layer(x_test, vocab_train, vocab_size_train,
                                       train_word2index)
    layer_1_train = one_hot_encode(y_train, 3)
    layer_1_test = one_hot_encode(y_test, 3)

    valid_features = layer_0_test
    valid_labels = layer_1_test

    # Remove previous weights, bias, inputs, etc..
    tf.reset_default_graph()

    # Inputs
    x = neural_net_sentence_input(vocab_size_train)
    y = neural_net_label_input(3)
    logits = neural_net(x, 3)
    logits = tf.identity(logits, name='logits')

    # Loss and Optimizer
    cost = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # Accuracy
    correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32),
                              name='accuracy')

    epochs = 1000
    # batch_size = 131

    with tf.Session() as sess:
        # Initializing the variables
        sess.run(tf.global_variables_initializer())

        # Training cycle
        for epoch in range(epochs):
            batch_i = 1
            batch_features = layer_0_train
            batch_labels = layer_1_train
            train_neural_network(sess, optimizer,
                                 batch_features, batch_labels)
            if (epoch+1) % 100 == 0:
                print(
                    'Epoch {:>2}, Batch {}:  '.format(epoch + 1, batch_i),
                    end='')
                print_stats(sess, batch_features, batch_labels, cost, accuracy, valid_features, valid_labels)
