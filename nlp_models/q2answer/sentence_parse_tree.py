"""
@Project   : CubeGirl
@Module    : sentence_parse_tree.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/2/18 10:23 AM
@Desc      : 句子分词及句法分析的结果
"""
from .depy_sen_parser import sen_parser
from .depy_tools import clean_sentence

sen = '哪些球员效力于女王公园巡游者'
# '{PERSON}俱乐部队友入选英格兰国家队有哪些'
# 梅西俱乐部的队友入选西班牙国家队的有哪些
# 哪家俱乐部既培养了英格兰国脚，也培养了西班牙国脚
# 哪些人既和大卫路易斯有矛盾，也和迭戈科斯塔有矛盾

# 罗纳尔多俱乐部的队友入选西班牙国家队的有哪些
# 罗纳尔多俱乐部队友入选西班牙国家队有哪些

# C罗俱乐部的队友入选西班牙国家队的有哪些：可以为名字被分词器分成两半的球员
# 专门做一个该类问题的模板；或者在分词前就把C罗替换成person，
# 然后进一步替换成克里斯蒂亚诺罗纳尔多

# 梅西俱乐部的队友入选西班牙国家队的有哪些：人数×国家队数
# 哪家俱乐部既培养了英格兰国脚，也培养了西班牙国脚：国家队数×国家队数
# 哪些人既和大卫路易斯有矛盾，也和迭戈科斯塔有矛盾：人数×人数，但表格数据稀疏


def test():
    st = clean_sentence(sen)
    words, postags, arcs = sen_parser.parse_one_template(st)
    print('test() in sentence_parse_tree.py')
    print('Syntactic analysis for "{}":'.format(sen))
    print('words:', list(words))
    print('postags in test() in sentence_parse_tree.py:', list(postags))
    print('arcs:', [(arc.head, arc.relation) for arc in arcs], '\n')
