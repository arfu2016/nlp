"""
@Project   : CubeGirl
@Module    : class4_syntac.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/15/18 2:23 PM
@Desc      : 句法的graph expression
"""
from .depy_dsl import HasProperty, ArelationB
from .depy_words_tpl import SyntacTpl


class Class1Graph(SyntacTpl):
    """
    Graph template for questions like "ATT的HED"
    Ex: "梅西的身高", "角球的定义"
    如果不想使用graph expression模板，而想直接调用sparql，可以在类中实现
    get_sparql_function(self, targets)
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        target是一个二维的表格
        行是抽取的各个词
        第一列是"翻译"过后的词的原文（不带引号的），
        第二列是sparql中词前边的动词，第三列是对应的
        sparql中用来代表该词的关系
        :param target:
        :return:
        """
        target1_n = '"{}"'.format(target[0][0])
        target1_v = target[0][1]
        target2_v = target[1][2]

        thing = HasProperty(target1_n, target1_v)
        goal = ArelationB(thing, target2_v)
        return goal
