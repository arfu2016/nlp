"""
@Project   : CubeGirl
@Module    : tpl01_yesorno.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/25/18 2:50 PM
@Desc      : 
"""
from .class2_general import Class1Graph3, Class2Graph3
from .depy_relation import OneTerm, get_content_verb


class Balishifoushoufa(Class1Graph3):
    """'2011年11月12日，在英格兰1: 0战胜西班牙的友谊赛中，巴里是否首发出场了'"""
    question_template = 'YesornoQuestion'
    words_involved = {0: ('ANY', 'ATT'),
                      1: (['11月', '1月'], 'ATT'),
                      2: ('ANY', 'ADV'),
                      3: ('ANY', 'ADV'),
                      4: ('ANY', 'POB'),
                      5: ('ANY', 'ATT'),
                      6: ('ANY', 'VOB'),
                      7: ('ANY', 'ATT'),
                      8: (['中'], 'ADV'),
                      9: ('ANY', 'SBV'),
                      10: (['是否'], 'ADV'),
                      11: ('ANY', 'HED'),
                      12: ('ANY', 'COO')}
    relations_involved = [(11, 8), (11, 9), (11, 10), (11, 12), (11, 2),
                          (8, 7), (7, 5), (5, 3), (3, 4), (5, 6), (2, 1),
                          (2, 0)]
    targets_involved = [0, 1, 2, 4, 6, 9, 11, 12]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[0] = goal[0] + goal[1] + goal[2]
            goal[1] = goal[3] + 'vs' + goal[4]
            goal[2] = goal[5]
            goal[3] = goal[6] + goal[7]
            goal[4] = '描述'
            goal = goal[:5]
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['答案是']
        if results is not None:
            result = '; '.join(results)
        else:
            result = ''
        return ''.join(goal) + result


class JigeQiuyuanhuodeshijiebei(Class2Graph3):
    """因扎吉和库伊特中，几个球员获得过世界杯冠军"""
    question_template = 'Howmanycanjiashijiebei'
    words_involved = {0: ('ANY', ['ATT']), 1: ('ANY', ['COO']),
                      2: (['中'], ['ADV']),
                      3: (['几', '多少'], ['ATT']), 4: (['个'], ['ATT']),
                      5: ('ANY', ['SBV']), 6: ('ANY', ['HED']),
                      7: ('ANY', ['ATT']), 8: ('ANY', ['VOB'])}
    relations_involved = [(6, 2), (6, 5), (6, 8), (2, 0), (5, 4), (8, 7),
                          (0, 1), (4, 3)]
    # 目前要求必须是一棵树，而不能是多棵树
    targets_involved = [6, 7, 8]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[1] = goal[1] + goal[2]
            goal = goal[:3]
            goal.insert(0, '哪些')
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result
