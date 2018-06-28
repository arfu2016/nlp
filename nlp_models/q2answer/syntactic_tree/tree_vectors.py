"""
@Project   : CubeGirl
@Module    : tree_vectors.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/15/17 9:55 AM
@Desc      : 
"""

import json
import re
from collections import defaultdict

from pydtk.dtk import DT
from pydtk.operation import fast_shuffled_convolution
from pydtk.tree import Tree

from Daka.chatbot.logic.text_table.common.syntactic_model \
    import clean_templates, Syntactic


def construct_trees(edges):
    """Given a list of edges [child, parent], return trees. """
    trees = defaultdict(dict)

    for child, parent in edges:
        trees[parent][child] = trees[child]

    # Find roots
    children, parents = zip(*edges)
    roots = set(parents).difference(children)

    # return {root: trees[root] for root in roots}
    return [trees[root] for root in roots]


def dicts2(t, arcs_relation):
    return {arcs_relation[k]: dicts2(t[k], arcs_relation) for k in t}


def tree2syntac(arcs):
    arcs_head = [arc.head - 1 for arc in arcs]
    arcs_relation = [arc.relation for arc in arcs]
    edges = [[i, arc_head] for i, arc_head in enumerate(arcs_head)]
    tree_parse = construct_trees(edges)
    tree_parse = tree_parse[0]
    tree_parse = dicts2(tree_parse, arcs_relation)
    a = json.dumps(tree_parse)
    b = re.sub('{}|[:"]', '', a)
    c = re.sub(',', ' ', b)
    d = re.sub('{', '(', c)
    e = re.sub('}', ')', d)
    f = re.sub('\s+', ' ', e)
    g = re.sub(r''' \)''', ')', f)
    return g


def trees2syns(templates):
    tpls_clean = clean_templates(templates)
    _, _, arcs_list = \
        Syntactic().parse_many_templates(tpls_clean)
    return [tree2syntac(arcs) for arcs in arcs_list]


def tree2vec(t_string):
    tree = Tree(string=t_string)
    dtCalculator = DT(dimension=128, LAMBDA=0.6,
                      operation=fast_shuffled_convolution)
    distributedTree = dtCalculator.dt(tree)
    return distributedTree


if __name__ == '__main__':
    temp = ['{PERSON}喜欢什么车', '{TEAM}的{PERSON}喜欢开什么车',
            '球员{PERSON}喜欢什么车', '{PERSON}喜欢干什么',
            '我的偶像{PERSON}喜欢什么车', '我喜欢{PERSON}', '我喜欢球员{PERSON}',
            '我喜欢{TEAM}的{PERSON}', '我喜欢{TEAM}{PERSON}',
            '我喜欢老将{PERSON}', '我老板喜欢球员{PERSON}']
    tree_strings = trees2syns(temp)
    for tree in tree_strings:
        print(tree)
    tree_vecs = [tree2vec(tree) for tree in tree_strings]
    for tree_vec in tree_vecs:
        print(tree_vec)
