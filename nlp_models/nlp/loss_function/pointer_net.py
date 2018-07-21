"""
@Project   : DuReader
@Module    : pointer_net.py
@Author    : Deco [deco@cubee.com]
@Created   : 7/20/18 11:25 AM
@Desc      : 
"""
"""
This module implements the Pointer Network for selecting answer spans, as described in:
https://openreview.net/pdf?id=B1-q5Pqxl
"""

import tensorflow as tf
import tensorflow.contrib as tc


def custom_dynamic_rnn(cell, inputs, inputs_len, initial_state=None):
    """
    Implements a dynamic rnn that can store scores in the pointer network,
    the reason why we implements this is that the raw_rnn or dynamic_rnn function in Tensorflow
    seem to require the hidden unit and memory unit has the same dimension, and we cannot
    store the scores directly in the hidden unit.
    Args:
        cell: RNN cell
        inputs: the input sequence to rnn
        inputs_len: valid length
        initial_state: initial_state of the cell
    Returns:
        outputs and state
    """
    batch_size = tf.shape(inputs)[0]
    max_time = tf.shape(inputs)[1]
    # 就是各个batch的输入的长度的最大值，不足这个长度的用0补足，叫做max_time

    inputs_ta = tf.TensorArray(dtype=tf.float32, size=max_time)
    inputs_ta = inputs_ta.unstack(tf.transpose(inputs, [1, 0, 2]))
    emit_ta = tf.TensorArray(dtype=tf.float32, dynamic_size=True, size=0)
    # 不指定初始化的具体值时，随机初始化？当reuse的时候，使用之前的emit_ta?
    t0 = tf.constant(0, dtype=tf.int32)
    if initial_state is not None:
        s0 = initial_state
    else:
        s0 = cell.zero_state(batch_size, dtype=tf.float32)
    f0 = tf.zeros([batch_size], dtype=tf.bool)

    def loop_fn(t, prev_s, emit_ta, finished):
        """
        the loop function of rnn
        """
        cur_x = inputs_ta.read(t)
        scores, cur_state = cell(cur_x, prev_s)

        # copy through
        scores = tf.where(finished, tf.zeros_like(scores), scores)

        if isinstance(cell, tc.rnn.LSTMCell):
            cur_c, cur_h = cur_state
            prev_c, prev_h = prev_s
            cur_state = tc.rnn.LSTMStateTuple(tf.where(finished, prev_c, cur_c),
                                              tf.where(finished, prev_h, cur_h))
        else:
            cur_state = tf.where(finished, prev_s, cur_state)

        emit_ta = emit_ta.write(t, scores)
        finished = tf.greater_equal(t + 1, inputs_len)
        return [t + 1, cur_state, emit_ta, finished]

    _, state, emit_ta, _ = tf.while_loop(
        cond=lambda _1, _2, _3, finished: tf.logical_not(tf.reduce_all(finished)),
        body=loop_fn,
        loop_vars=(t0, s0, emit_ta, f0),
        parallel_iterations=32,
        swap_memory=False)

    outputs = tf.transpose(emit_ta.stack(), [1, 0, 2])
    return outputs, state


def attend_pooling(pooling_vectors, ref_vector, hidden_size, scope=None):
    """
    Applies attend pooling to a set of vectors according to a reference vector.
    Args:
        pooling_vectors: the vectors to pool
        ref_vector: the reference vector
        hidden_size: the hidden size for attention function
        scope: score name
    Returns:
        the pooled vector
    """
    with tf.variable_scope(scope or 'attend_pooling'):
        U = tf.tanh(tc.layers.fully_connected(pooling_vectors, num_outputs=hidden_size,
                                              activation_fn=None, biases_initializer=None)
                    + tc.layers.fully_connected(tf.expand_dims(ref_vector, 1),
                                                num_outputs=hidden_size,
                                                activation_fn=None))
        logits = tc.layers.fully_connected(U, num_outputs=1, activation_fn=None)
        scores = tf.nn.softmax(logits, 1)
        pooled_vector = tf.reduce_sum(pooling_vectors * scores, axis=1)
    return pooled_vector


class PointerNetLSTMCell(tc.rnn.LSTMCell):
    """
    Implements the Pointer Network Cell
    """
    def __init__(self, num_units, context_to_point):
        super(PointerNetLSTMCell, self).__init__(num_units, state_is_tuple=True)
        self.context_to_point = context_to_point
        self.fc_context = tc.layers.fully_connected(self.context_to_point,
                                                    num_outputs=self._num_units,
                                                    activation_fn=None)

    def __call__(self, inputs, state, scope=None):
        (c_prev, m_prev) = state
        with tf.variable_scope(scope or type(self).__name__):
            U = tf.tanh(self.fc_context
                        + tf.expand_dims(tc.layers.fully_connected(m_prev,
                                                                   num_outputs=self._num_units,
                                                                   activation_fn=None),
                                         1))
            logits = tc.layers.fully_connected(U, num_outputs=1, activation_fn=None)
            scores = tf.nn.softmax(logits, 1)
            print('scores:', scores.get_shape())
            attended_context = tf.reduce_sum(self.context_to_point * scores, axis=1)
            lstm_out, lstm_state = super(PointerNetLSTMCell, self).__call__(attended_context, state)
            # attended_context作为input，目的是得到lstm_state
        print('tf.squeeze(scores, -1):', tf.squeeze(scores, -1).get_shape())
        return tf.squeeze(scores, -1), lstm_state
        # 最终返回的是scores, scores本来是三个维度，第一个维度是batch size，
        # 第二个维度是句子中词的个数，第三个维度把hidden units通过softmax
        # 变成了一个数字（也就是logistic regression）。表面上看，用了fake-input的lstm
        # 输出，实际上，通过重载lstm cell的__call__，最终的outputs和inputs根本没有关系
        # tf.squeeze是把三维变成了两维，因为第三维上只有一个数字(只有一列或者一行)


class PointerNetDecoder(object):
    """
    Implements the Pointer Network
    """
    def __init__(self, hidden_size):
        self.hidden_size = hidden_size

    def decode(self, passage_vectors, question_vectors, init_with_question=True):
        """
        Use Pointer Network to compute the probabilities of each position
        to be start and end of the answer
        Args:
            passage_vectors: the encoded passage vectors
            question_vectors: the encoded question vectors
            init_with_question: if set to be true,
                             we will use the question_vectors to init the state of Pointer Network
        Returns:
            the probs of evary position to be start and end of the answer
        """
        with tf.variable_scope('pn_decoder'):
            fake_inputs = tf.zeros([tf.shape(passage_vectors)[0], 2, 1])
            # not used?
            sequence_len = tf.tile([2], [tf.shape(passage_vectors)[0]])
            if init_with_question:
                random_attn_vector = tf.Variable(tf.random_normal([1, self.hidden_size]),
                                                 trainable=True, name="random_attn_vector")
                pooled_question_rep = tc.layers.fully_connected(
                    attend_pooling(question_vectors, random_attn_vector, self.hidden_size),
                    num_outputs=self.hidden_size, activation_fn=None
                )
                init_state = tc.rnn.LSTMStateTuple(pooled_question_rep, pooled_question_rep)
            else:
                init_state = None
            with tf.variable_scope('fw'):
                fw_cell = PointerNetLSTMCell(self.hidden_size, passage_vectors)
                # 把文档词向量矩阵传进去，得到的结果变瘦了，每个词只对应一个数字，本质上还是词向量矩阵
                # 普通lstm的输出维度是hidden units的个数，这里lstm的输出维度是passage中word的个数
                fw_outputs, _ = custom_dynamic_rnn(fw_cell, fake_inputs, sequence_len, init_state)
                # 因为传入的input是两步，结果也是两步，第一步是start的概率，第二步是end的概率
            with tf.variable_scope('bw'):
                bw_cell = PointerNetLSTMCell(self.hidden_size, passage_vectors)
                bw_outputs, _ = custom_dynamic_rnn(bw_cell, fake_inputs, sequence_len, init_state)
                # 因为传入的input是两步，结果也是两步，第一步是end的概率，第二步是start的概率
            # 又一次使用了bidirectional lstm，一个lstm从左到右，一个lstm从右到左
            start_prob = (fw_outputs[0:, 0, 0:] + bw_outputs[0:, 1, 0:]) / 2
            end_prob = (fw_outputs[0:, 1, 0:] + bw_outputs[0:, 0, 0:]) / 2
            # print('start_prob in pointer_net.py in layers in tensorflow2:',
            #       start_prob)
            # print('end_prob in pointer_net.py in layers in tensorflow2:',
            #       end_prob)
            # print('Compare start_prob == end_prob:', start_prob == end_prob)
            return start_prob, end_prob

    def decode2(self, passage_vectors, question_vectors, init_with_question=True):
        """
        Used for debugging
        Use Pointer Network to compute the probabilities of each position
        to be start and end of the answer
        Args:
            passage_vectors: the encoded passage vectors，加权过的词向量矩阵
            question_vectors: the encoded question vectors，词向量矩阵
            init_with_question: if set to be true,
                             we will use the question_vectors to init
                             the hidden state of Pointer Network
        Returns:
            the probs of every position to be start and end of the answer
        """
        with tf.variable_scope('pn_decoder2'):
            fake_inputs = tf.zeros([tf.shape(passage_vectors)[0], 2, 1])  # not used
            sequence_len = tf.tile([2], [tf.shape(passage_vectors)[0]])
            if init_with_question:
                random_attn_vector = tf.Variable(tf.random_normal([1, self.hidden_size]),
                                                 trainable=True, name="random_attn_vector")
                pooled_question_rep = tc.layers.fully_connected(
                    attend_pooling(question_vectors, random_attn_vector, self.hidden_size),
                    num_outputs=self.hidden_size, activation_fn=None
                )
                init_state = tc.rnn.LSTMStateTuple(pooled_question_rep, pooled_question_rep)
            else:
                init_state = None
            with tf.variable_scope('fw2'):
                fw_cell = PointerNetLSTMCell(self.hidden_size, passage_vectors)
                # 这个类的初始化其实不只需要以上两个参数，比如还需要weights，但weights
                # 的初始化在没有传参数的情况下是自动调用随机函数来进行的
                # 也是因为这种随机性，造成fw_cell和bw_cell的不同，也可以解释为什么
                # 刚开始的时候start_prob和end_prob不同，但又很接近
                # 在拟合数据的过程中，fw/weights和bw/weights会渐渐分化，所以
                # start_prob和end_prob差距会变大
                fw_outputs, _ = custom_dynamic_rnn(fw_cell, fake_inputs,
                                                   sequence_len, init_state)

            with tf.variable_scope('fw2', reuse=True):
                fw_cell1 = PointerNetLSTMCell(self.hidden_size, passage_vectors)
                # reuse PointerNetLSTMCell中的权重，作为新的初始化的权重?
                fw_outputs2, _ = custom_dynamic_rnn(fw_cell, fake_inputs,
                                                    sequence_len, init_state)
                # reuse fw_cell?
                # custom_dynamic_rnn的实现中也引入了随机性，而且这种随机性和第一个参数
                # fw_cell相关，所以，当第一个参数fw_cell变掉之后，custom_dynamic_rnn
                # 是没法reuse fw2中的weights的（？），只有当fw_cell依然是之前的fw_cell
                # 时，custom_dynamic_rnn的weights才能reuse

            with tf.variable_scope('bw2'):
                bw_cell = PointerNetLSTMCell(self.hidden_size, passage_vectors)
                bw_outputs, _ = custom_dynamic_rnn(bw_cell, fake_inputs,
                                                   sequence_len, init_state)
            start_prob = (fw_outputs[0:, 0, 0:] + bw_outputs[0:, 1, 0:]) / 2
            end_prob = (fw_outputs[0:, 1, 0:] + bw_outputs[0:, 0, 0:]) / 2
            # print('start_prob in pointer_net.py in layers in tensorflow2:',
            #       start_prob)
            # print('end_prob in pointer_net.py in layers in tensorflow2:',
            #       end_prob)
            # print('Compare start_prob == end_prob:', start_prob == end_prob)
            return fw_outputs[0:, 0, 0:], fw_outputs2[0:, 0, 0:], bw_outputs[0:, 0, 0:]
            # return fw_cell, bw_cell, fw_cell1
