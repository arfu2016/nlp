"""
@Project   : CubeGirl
@Module    : tpl2_general.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/12/18 1:13 PM
@Desc      : 泛化能力比较强的模板
"""

from .class2_general import \
    Class2Graph1, Class3Graph1, Class4Graph1, \
    Class4Graph2, Class4Graph3, Class1Graph, Class3Graph2, \
    Class2Graph3, Class3Graph3, Class5Graph2, Class3Graph5
from .depy_relation import OneTerm, relation, get_content_verb


class AttAttHedTree2(Class2Graph1):
    """莱因克尔在什么比赛中上演帽子戏法；xx在什么xx中做xx"""
    template_name = 'AttAttHedTree2'
    words_involved = {0: ('ANY', 'SBV'), 1: (['在'], 'ADV'), 2: ('ANY', 'ATT'),
                      3: ('ANY', 'ATT'), 4: (['中'], 'POB'), 5: ('ANY', 'HED'),
                      6: ('ANY', 'VOB')}
    # 6条边，模板略大，如果速度偏慢的话，可以更小一些
    relations_involved = [(5, 0), (5, 1), (5, 6), (1, 4), (4, 3), (3, 2)]
    targets_involved = [0, 6, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[2], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class AttHedTree(Class1Graph):
    """梅西的身高；xx的xx"""
    template_name = 'AttHedTree'
    words_involved = {0: ('ANY', 'ATT'), 1: ('ANY', 'HED')}
    # words_involved = {0: ('梅西', 'ATT'), 1: ('身高', 'HED')}
    relations_involved = [(1, 0)]
    targets_involved = [0, 1]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[1], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAttHedTree(Class2Graph1):
    """马拉多纳一球成名的对手；xx yy的xx"""
    template_name = 'SbvAttHedTree'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ATT'),
                      2: ('ANY', 'HED')}
    relations_involved = [(2, 1), (1, 0)]
    targets_involved = [0, 1, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[2], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAttHedTree2(Class2Graph1):
    """马拉多纳怎么一球成名；马拉多纳怎么一球成名的；xx怎么xx"""
    template_name = 'SbvAttHedTree2'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ADV'),
                      2: ('ANY', 'HED')}
    relations_involved = [(2, 1), (2, 0)]
    targets_involved = [0, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '是这样', temp[1], '的', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAttHedTree2b(Class3Graph1):
    """鲁尼在国家队期间有什么一球成名吗"""
    template_name = 'SbvAttHedTree2b'
    words_involved = {0: ('ANY', ['SBV']), 1: ('ANY', ['ADV']),
                      2: ('ANY', ['ATT']), 3: ('ANY', ['POB']),
                      4: ('ANY', ['HED']), 5: (['什么', '啥'], ['VOB']),
                      6: (['一球成名', '帽子戏法'], ['VOB'])}
    relations_involved = [(4, 0), (4, 1), (4, 6), (1, 3), (4, 5), (3, 2)]
    targets_involved = [0, 6, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        # print(mapping)
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            # print(goal)
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '的', temp[2], '包括', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAttHedTree2c(Class3Graph1):
    """鲁尼在国家队期间有什么帽子戏法吗"""
    template_name = 'SbvAttHedTree2c'
    words_involved = {0: ('ANY', ['SBV']), 1: ('ANY', ['ADV']),
                      2: ('ANY', ['ATT']), 3: ('ANY', ['POB']),
                      4: ('ANY', ['HED']), 5: (['什么', '啥'], ['ATT']),
                      6: (['一球成名', '帽子戏法'], ['VOB'])}
    relations_involved = [(4, 0), (4, 1), (4, 6), (1, 3), (6, 5), (3, 2)]
    targets_involved = [0, 6, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        print(mapping)
        print(words)
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '的', temp[2], '包括', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAttHedTree3(Class2Graph1):
    """马拉多纳是怎么一球成名的"""
    template_name = 'SbvAttHedTree3'
    words_involved = {0: ('ANY', 'SBV'), 1: (['是'], 'ANY'), 2: ('ANY', 'ADV'),
                      3: ('ANY', 'VOB')}
    relations_involved = [(1, 0), (1, 3), (3, 2)]
    targets_involved = [0, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '是这样', temp[1], '的', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAttHedTree4(Class2Graph1):
    """马拉多纳一球成名；马拉多纳转会；xx yy"""
    template_name = 'SbvAttHedTree4'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'HED')}
    relations_involved = [(1, 0)]
    targets_involved = [0, 1]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], temp[1], '是这样的', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class AttAttHedTree(Class2Graph1):
    """莱因克尔帽子戏法的比赛；莱因克尔的帽子戏法的比赛；xx的xx的xx"""
    template_name = 'AttAttHedTree'
    words_involved = {0: ('ANY', 'ATT'), 1: ('ANY', 'ATT'), 2: ('ANY', 'HED')}
    # words_involved = {0: ('梅西', 'ATT'), 1: ('女友', 'ATT'), 2: ('名字', 'HED')}
    relations_involved = [(2, 1), (1, 0)]
    targets_involved = [0, 1, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[2], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob(Class3Graph1):
    """巴雷西如何评价马拉多纳; 巴雷西如何评价马拉多纳的；xx如何做xx"""
    template_name = 'SbvHedVob'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ADV'), 2: ('ANY', 'HED'),
                      3: ('ANY', 'VOB')}
    relations_involved = [(2, 0), (2, 1), (2, 3)]
    targets_involved = [0, 2, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '是这样', temp[1], temp[2], '的', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVobreal(Class3Graph1):
    """巴雷西评价马拉多纳; 马拉多纳执教阿根廷队；xx yy xx"""
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'HED'),
                      2: ('ANY', 'VOB')}
    relations_involved = [(1, 0), (1, 2)]
    targets_involved = [0, 1, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '是这样', temp[1], temp[2], '的', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob2(Class3Graph1):
    """巴雷西是如何评价马拉多纳的"""
    template_name = 'SbvHedVob2'
    words_involved = {0: ('ANY', 'SBV'), 1: (['是'], 'ANY'), 2: ('ANY', 'ADV'),
                      3: ('ANY', 'VOB'), 4: ('ANY', 'VOB')}
    relations_involved = [(1, 0), (1, 3), (3, 2), (3, 4)]
    targets_involved = [0, 3, 4]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '是这样', temp[1], temp[2], '的', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3(Class3Graph1):
    """马拉多纳执教阿根廷队的开始时间；xx做xx的xx"""
    template_name = 'SbvHedVob3'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ATT'),
                      2: ('ANY', 'VOB'), 3: ('ANY', 'HED')}
    relations_involved = [(3, 1), (1, 0), (1, 2)]
    targets_involved = [0, 1, 2, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3b(Class3Graph3):
    """马拉多纳转会到巴塞罗那的时间；xx做xx的xx"""
    template_name = 'SbvHedVob3b'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ATT'), 2: ('ANY', 'CMP'),
                      3: ('ANY', 'POB'), 4: ('ANY', 'HED')}
    relations_involved = [(4, 1), (1, 0), (1, 2), (2, 3)]
    targets_involved = [0, 1, 3, 4]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob5(Class4Graph2):
    """马拉多纳从博卡青年转会到哪里；xx从xx做yy，问yy"""
    template_name = 'SbvHedVob5'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ADV'),
                      2: ('ANY', 'POB'), 3: ('ANY', 'HED'),
                      4: ('ANY', 'CMP'), 5: ('ANY', 'POB')}
    relations_involved = [(3, 0), (3, 1), (3, 4), (1, 2), (4, 5)]
    targets_involved = [0, 3, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            goal.insert(2, ['从', 'Out'])
            goal.insert(3, ['到', 'In'])
            extra = ['名字']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['是']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVobSbvHedVob(Class4Graph3):
    """鲁尼俱乐部的队友入选英格兰国家队的有哪些"""
    template_name = 'SbvHedVobSbvHedVob'
    words_involved = {0: ('ANY', 'ATT'), 1: ('ANY', 'ATT'),
                      2: ('ANY', 'SBV'), 3: ('ANY', 'SBV'),
                      4: ('ANY', 'ATT'), 5: ('ANY', 'VOB'),
                      6: ('ANY', 'HED'), 7: ('ANY', 'VOB')}
    relations_involved = [(6, 3), (6, 7), (3, 2), (3, 5), (5, 4), (2, 1),
                          (1, 0)]
    targets_involved = [0, 1, 4, 5, 7]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            # temp = goal[2][0] + '队'
            temp = goal[2][0]
            goal[2] = [temp, relation(temp)]
            # goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result


class LibaiXieNaxieYinjiushi(Class3Graph5):
    """李白写过哪些饮酒诗；xx做过哪些xx"""
    # template_name = 'LibaiXieNaxieYinjiushi'
    words_involved = {0: ('ANY', ['SBV']),
                      1: ('ANY', ['HED']), 2: (['什么', '啥', '哪些'], ['ATT']),
                      3: ('ANY', ['VOB'])}
    relations_involved = [(1, 0), (1, 3), (3, 2)]
    targets_involved = [0, 1, 3, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = ['情况']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '的', temp[2], '包括', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class Qingxunpeixun(Class3Graph2):
    """河床青训培养过哪些球员；xx的xx做过哪些xx"""
    words_involved = {0: ('ANY', ['ATT']), 1: ('ANY', ['SBV']),
                      2: ('ANY', ['HED']), 3: (['什么', '啥', '哪些'], ['ATT']),
                      4: ('ANY', ['VOB'])}
    relations_involved = [(2, 1), (2, 4), (4, 3), (1, 0)]
    targets_involved = [0, 1, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = [goal[1][0] + '动词']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class Qiuyuanhuodeshijiebei(Class2Graph3):
    """哪些球员获得过世界杯冠军; 哪些xx做过xx的xx"""
    words_involved = {0: (['哪些'], 'ATT'), 1: ('ANY', 'SBV'),
                      2: ('ANY', 'HED'),
                      3: ('ANY', 'ATT'), 4: ('ANY', 'VOB')}
    relations_involved = [(2, 1), (4, 3), (2, 4), (1, 0)]
    targets_involved = [0, 2, 3, 4]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[2] = goal[2] + goal[3]
            goal = goal[:4]
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result
