"""
@Project   : CubeGirl
@Module    : depy_expression.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/19/17 2:45 PM
@Desc      : 图结构表达式的基类
"""
from collections import defaultdict
from copy import deepcopy


def isnode(x):
    return isinstance(x, int)


def isedge(x):
    return isinstance(x, tuple)


class Expression(object):

    def __init__(self):
        """
        Creates a new graph with a single solitary blank node.
        """
        self.nodes = []  # list of list，it is adjacency list
        # nodes' index represents variable, constant vertex has no index
        self.head = self._add_node()

    def _add_node(self):
        """
        Adds a blank node to the graph and returns its index (a unique
        identifier).
        """
        i = len(self.nodes)
        self.nodes.append([])
        return i

    def get_head(self):
        """
        Returns the index (the unique identifier) of the head node.
        """
        return self.head

    def merge(self, other):
        """
        Given other Expression, it joins their graphs preserving every
        node and every edge intact except for the ``head`` nodes.
        The ``head`` nodes are merged into a single node that is the new
        ``head`` and shares all the edges of the previous heads.
        current expression与other expression的head是相同的，要合二为一
        """
        translation = defaultdict(self._add_node)
        # 在defaultdict的value中自动补上len(self.nodes)
        # 任何key的默认value都是len(self.nodes)，在调用该key时自动生成
        translation[other.head] = self.head
        # 要可合并的other的head节点与当前head节点的对应关系
        # head is changed
        for node in other.iter_nodes():
            for relation, dest in other.iter_edges(node):
                xs = self.nodes[translation[node]]
                # 各个新的节点的用于存放对应关系的list
                # 如果node是other.head，translation[node]就是新的head
                # 如果node是other中的非head的节点，自动生成value值
                if isnode(dest):  # 是变量节点，不是常量节点
                    dest = translation[dest]
                    # 如果是变量节点，要转换成新的index
                    # 如果是常量节点，直接用原来的string就行
                xs.append((relation, dest))
                # 要把other.head上的连接都迁到新的head上，同时把旧的head删掉，
                # 把other上节点的index改掉

    def decapitate(self, relation, reverse=False):
        """
        Creates a new blank node and makes it the ``head`` of the
        Expression. Then it adds an edge (a ``relation``) linking the
        the new head to the old one. So in a single operation a
        node and an edge are added.
        If ``reverse`` is ``True`` then the ``relation`` links the old head to
        the new head instead of the opposite (some relations are not
        commutative).
        """
        oldhead = self.head
        self.head = self._add_node()
        if reverse:
            self.nodes[oldhead].append((relation, self.head))
        else:
            self.nodes[self.head].append((relation, oldhead))
            # nodes list中包含两个元素的tuple或者list，分别储存边和指向的点

    def add_data(self, relation, value):
        """
        Adds a ``relation`` to some constant ``value`` to the ``head`` of the
        Expression.
        ``value`` is recommended be of type:
        - ``unicode``
        - ``str`` and can be decoded using the default encoding (settings.py)
        - A custom class that implements a ``__unicode__`` method.
        - It can *NEVER* be an ``int``.

        You should not use this to relate nodes in the graph, only to add
        data fields to a node.
        To relate nodes in a graph use a combination of merge and decapitate.
        """
        assert not isnode(value)
        self.nodes[self.head].append((relation, value))
        # value通常是个string，表示是常量，不是变量

    def iter_nodes(self):
        """
        Iterates the indexes (the unique identifiers) of the Expression nodes.
        """
        return range(len(self.nodes))

    def iter_edges(self, node):
        """
        Iterates over the pairs: ``(relation, index)`` which are the neighbors
        of ``node`` in the expression graph, where:
        - ``node`` is the index of the node (the unique identifier).
        - ``relation`` is the label of the edge between the nodes
        - ``index`` is the index of the neighbor (the unique identifier).
        """
        return iter(self.nodes[node])
        # 某一个node的连接，是一个list或者tuple，所以可以作为iter的参数

    def __add__(self, other):
        """
        Merges ``self`` and ``other`` in a new Expression instance.
        Ie, ``self`` and ``other`` are not modified.
        """
        new = deepcopy(self)
        new.merge(other)
        return new

    def __iadd__(self, other):
        """
        Merges ``self`` and ``other`` into ``self``
        ``other`` is not modified but the original data in ``self`` is lost.
        """
        self.merge(other)
        return self

    def __len__(self):
        """
        Amount of nodes in the graph.
        """
        return len(self.nodes)

    def len_edges(self):
        cnt = 0
        # cnt = len(self.nodes)
        for node in self.nodes:
            cnt += len(node)
        return cnt
