"""
@Project   : CubeGirl
@Module    : tree_construct.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/14/17 11:37 AM
@Desc      : 
"""

import json
import re
from collections import defaultdict

from Daka.chatbot.logic.text_table.common.syntactic_model import Syntactic

words, postags, arcs = Syntactic().parse_one_template('我喜欢 PERSON ')
# '郑智喜欢什么车'

words = list(words)
print(words)
arcs_head = [arc.head-1 for arc in arcs]
print(arcs_head)
arcs_relation = [arc.relation for arc in arcs]
print(arcs_relation)
print(["%d:%s" % (arc.head, arc.relation) for arc in arcs])

# tree_info = dict()
# for i in range(len(words)):
#     word = words[i]
#     head = arcs_head[i]
#     try:
#         tree_info[head].append(i)
#     except KeyError:
#         tree_info[head] = [i]
#
# print(tree_info)

tree_info = defaultdict(list)
for i in range(len(words)):
    head = arcs_head[i]
    tree_info[head].append(i)

print(tree_info)


def tree():
    return defaultdict(tree)


def dicts(t):
    return {k: dicts(t[k]) for k in t}


# tree_parse = tree()
# print(dicts(tree_parse))
#
# s = arcs_head[tree_info[-1][0]]
# print(s)
# root = tree_info[s][0]
# print(root)
# first = tree_info[root][0]
# tree_parse[words[root]][words[first]]
# # tree_parse[words[root]][words[first]] = tree()
# second = tree_info[root][1]
# third = tree_info[second][0]
# tree_parse[words[root]][words[second]][words[third]]
# # tree_parse[words[root]][words[second]][words[third]] = tree()
# print(tree_parse)
# print(dicts(tree_parse))


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


edges = [[i, arc.head-1] for i, arc in enumerate(arcs)]
print(edges)

tree_parse = construct_trees(edges)
tree_parse = tree_parse[0]


def dicts2(t):
    return {arcs_relation[k]: dicts2(t[k]) for k in t}


tree_parse = dicts2(tree_parse)

# 用json.dumps()和eval()可以实现depth first search的效果
print(json.dumps(construct_trees(edges), indent=4))
print(json.dumps(tree_parse, indent=4))
print(json.dumps(tree_parse))
a = json.dumps(tree_parse)
print(type(a))

b = re.sub('{}|[:"]', '', a)
print(b)
c = re.sub(',', ' ', b)
print(c)
d = re.sub('{', '(', c)
print(d)
e = re.sub('}', ')', d)
print(e)
f = re.sub('\s+', ' ', e)
print(f)
g = re.sub(r''' \)''', ')', f)
print(g)
