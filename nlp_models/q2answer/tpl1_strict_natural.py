"""
@Project   : CubeGirl
@Module    : tpl1_strict_natural.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/15/18 10:26 AM
@Desc      : 要求比较严格的模板
"""
from .class2_general import Class2Graph1, Class3Graph1, Class1Graph2, \
    Class2Graph2, Class2Graph3, Class5Graph1, Class3Graph3, Class3Graph2, \
    Class5Graph2, Class3Graph4, Class4Graph1
from .depy_relation import OneTerm, relation, get_content_verb


class Maozixifa(Class2Graph1):
    """马拉多纳帽子戏法;乔戈麦斯首秀；xx yy"""
    words_involved = {0: ('ANY', 'ATT'),
                      1: (['帽子戏法', '首秀', '首球'], 'HED')}
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


class SbvHedVobshoucichuchang(Class2Graph1):
    """马拉多纳首/第一次出场"""
    words_involved = {0: ('ANY', 'SBV'), 1: (['首', '第一'], 'ATT'),
                      2: ('ANY', 'ADV'),
                      3: ('ANY', 'HED')}
    relations_involved = [(3, 0), (3, 2), (2, 1)]
    targets_involved = [0, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVobdeshoucichuchang(Class2Graph1):
    """马拉多纳的首/第一次出场"""
    words_involved = {0: ('ANY', 'ATT'), 1: (['首', '第一'], 'ATT'),
                      2: ('ANY', 'ADV'),
                      3: ('ANY', 'HED')}
    relations_involved = [(3, 0), (3, 2), (2, 1)]
    targets_involved = [0, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVobdiyicijinqiu(Class2Graph1):
    """本田圭佑第一次进球"""
    words_involved = {0: ('ANY', 'ATT'), 1: (['首', '第一'], 'ATT'),
                      2: (['次', '回', '个'], 'ATT'),
                      3: ('ANY', 'HED')}
    relations_involved = [(3, 0), (3, 2), (2, 1)]
    targets_involved = [0, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cguojiaduidiyici(Class3Graph1):
    """马拉多纳国家队首/第一次出场"""
    words_involved = {0: ('ANY', 'ATT'),
                      1: ('ANY', 'SBV'), 2: (['首', '第一'], 'ATT'),
                      3: ('ANY', 'ADV'),
                      4: ('ANY', 'HED')}
    relations_involved = [(4, 1), (4, 3), (1, 0), (3, 2)]
    targets_involved = [0, 4, 1]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cbentianguojiadui(Class3Graph1):
    """本田圭佑国家队首/第一次进球"""
    words_involved = {0: ('ANY', 'ATT'),
                      1: ('ANY', 'ATT'), 2: (['首', '第一'], 'ATT'),
                      3: (['次', '回', '个'], 'ATT'),
                      4: ('ANY', 'HED')}
    relations_involved = [(4, 1), (4, 3), (1, 0), (3, 2)]
    targets_involved = [0, 4, 1]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cdiyiciguojiadui(Class3Graph1):
    """马拉多纳首/第一次国家队出场"""
    words_involved = {0: ('ANY', 'ATT'),
                      1: (['首', '第一'], 'ATT'),
                      2: (['次', '回', '个'], 'ATT'),
                      3: ('ANY', 'SBV'),
                      4: ('ANY', 'HED')}
    relations_involved = [(4, 3), (3, 0), (3, 2), (2, 1)]
    targets_involved = [0, 4, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cbentiandiyige(Class3Graph1):
    """本田圭佑第一个国家队进球"""
    words_involved = {0: ('ANY', 'ATT'),
                      1: (['首', '第一'], 'ATT'),
                      2: (['次', '回', '个'], 'ATT'),
                      3: ('ANY', 'ATT'),
                      4: ('ANY', 'HED')}
    relations_involved = [(4, 3), (3, 0), (3, 2), (2, 1)]
    targets_involved = [0, 4, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cguojiaduishouxiu(Class3Graph1):
    """马拉多纳国家队首秀"""
    words_involved = {0: ('ANY', 'ATT'),
                      1: ('ANY', 'ATT'),
                      2: (['首秀', '首球'], 'HED')}
    relations_involved = [(2, 1), (1, 0)]
    targets_involved = [0, 2, 1]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '情况'
            goal.append([temp, relation(temp)])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3ca(Class3Graph1):
    """马拉多纳第一次在国家队出场时间"""
    words_involved = {0: ('ANY', 'ATT'), 1: (['首', '第一'], 'ATT'),
                      2: (['次', '回'], 'ATT'), 3: (['在'], 'ATT'),
                      4: ('ANY', 'POB'), 5: (['出场', '进球', '破门'], 'ATT'),
                      6: ('ANY', 'HED')}
    relations_involved = [(6, 5), (6, 0), (6, 2), (6, 3), (3, 4), (2, 1)]
    targets_involved = [0, 5, 4, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3c(Class3Graph1):
    """马拉多纳首/第一次在国家队出场的时间"""
    template_name = 'SbvHedVob3c'
    words_involved = {0: ('ANY', 'SBV'), 1: (['首', '第一'], 'ATT'),
                      2: ('ANY', 'ADV'), 3: (['在'], 'ADV'),
                      4: ('ANY', 'POB'), 5: (['出场', '进球', '破门'], 'ATT'),
                      6: ('ANY', 'HED')}
    relations_involved = [(6, 5), (5, 0), (5, 2), (5, 3), (3, 4), (2, 1)]
    targets_involved = [0, 5, 4, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cb(Class3Graph1):
    """本田圭佑首/第一次在日本队出场对手"""
    words_involved = {0: ('ANY', 'SBV'), 1: (['首', '第一'], 'ATT'),
                      2: ('ANY', 'ADV'), 3: (['在'], 'HED'),
                      4: (['日本队', '巴西队'], 'ATT'),
                      5: (['出场', '进球', '破门'], 'ATT'),
                      6: ('ANY', 'POB')}
    relations_involved = [(3, 6), (3, 0), (3, 2), (6, 4), (6, 5), (2, 1)]
    targets_involved = [0, 5, 4, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3cc(Class3Graph1):
    """马拉多纳首/第一次在国家队出场对手"""
    words_involved = {0: ('ANY', 'SBV'), 1: (['首', '第一'], 'ATT'),
                      2: ('ANY', 'ADV'), 3: (['在'], 'ADV'),
                      4: ('ANY', 'POB'), 5: (['出场', '进球', '破门'], 'HED'),
                      6: ('ANY', 'VOB')}
    relations_involved = [(5, 6), (5, 0), (5, 2), (5, 3), (3, 4), (2, 1)]
    targets_involved = [0, 5, 4, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3d(Class3Graph1):
    """莱因克尔首/第一次在巴塞罗那进球的时间"""
    template_name = 'SbvHedVob3d'
    words_involved = {0: ('ANY', 'SBV'), 1: (['第一', '首'], 'ATT'),
                      2: ('ANY', 'ADV'), 3: ('ANY', 'HED'),
                      4: ('ANY', 'ATT'), 5: (['出场', '进球'], 'ATT'),
                      6: ('ANY', 'POB')}
    relations_involved = [(3, 0), (3, 2), (3, 6), (2, 1), (6, 5), (5, 4)]
    targets_involved = [0, 5, 4, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3e(Class3Graph1):
    """莱因克尔首/第一次在巴塞罗那进球的比赛"""
    template_name = 'SbvHedVob3e'
    words_involved = {0: ('ANY', ['ATT']), 1: (['首', '第一'], ['ATT']),
                      2: (['次', '回'], ['ATT']), 3: (['在'], ['ATT']),
                      4: ('ANY', ['ATT']), 5: (['出场', '进球'], ['ATT']),
                      6: ('ANY', ['HED'])}
    relations_involved = [(6, 0), (6, 2), (6, 3), (6, 5), (2, 1), (5, 4)]
    targets_involved = [0, 5, 4, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[3], '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class AttAttAttSbvHedCmp(Class3Graph1):
    """鲁尼第一次代表国家队出场在什么时候"""
    template_name = 'AttAttAttSbvHedCmp'
    words_involved = {0: ('ANY', ['ATT']), 1: (['第一'], ['ATT']),
                      2: (['次'], ['ATT']),
                      3: (['代表'], ['ATT']), 4: ('ANY', ['SBV']),
                      5: (['出场', '进球'], ['HED']),
                      6: ('ANY', ['CMP']), 7: (['时候'], ['POB'])}
    relations_involved = [(5, 4), (5, 6), (4, 0), (4, 3), (4, 2), (6, 7),
                          (2, 1)]
    targets_involved = [0, 5, 4, 7]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['时间', '是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAdvAttSbvHedVob(Class3Graph1):
    """鲁尼在国家队中第一个进球是什么时候"""
    template_name = 'SbvAdvAttSbvHedVob'
    words_involved = {0: ('ANY', ['SBV']), 1: (['在'], ['ADV']),
                      2: ('ANY', ['ATT']),
                      3: ('ANY', ['POB']), 4: (['第一'], 'ATT'),
                      5: (['个', '次', '回'], ['ATT', 'ADV']),
                      6: ('ANY', ['SBV']), 7: ('ANY', ['HED']),
                      8: ('ANY', ['VOB'])}
    relations_involved = [(7, 6), (7, 8), (6, 0), (6, 1), (6, 5), (1, 3),
                          (5, 4), (3, 2)]
    targets_involved = [0, 6, 2, 8]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvAdvAttSbvHedVob2(Class3Graph1):
    """加图索在国家队中第一个进球是什么比赛"""
    template_name = 'SbvAdvAttSbvHedVob2'
    words_involved = {0: ('ANY', ['SBV']), 1: ('ANY', ['ADV']),
                      2: ('ANY', ['ATT']),
                      3: ('ANY', ['POB']), 4: (['第一'], 'ATT'),
                      5: ('ANY', ['ATT']),
                      6: (['进球', '出场'], ['SBV']), 7: ('ANY', ['HED']),
                      8: ('ANY', ['VOB'])}
    relations_involved = [(7, 6), (7, 8), (7, 0), (7, 1), (6, 5), (1, 3),
                          (5, 4), (3, 2)]
    targets_involved = [0, 6, 2, 8]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            temp = '首次' + goal[1][0]
            goal[1] = [temp, relation(temp)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['是', ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class Jiludejinqiu(Class1Graph2):
    """吉尼斯世界纪录的最远进球"""
    words_involved = {0: (['纪录'], 'ATT'),
                      1: (['远'], 'ATT'),
                      2: (['进球'], 'ANY')}
    relations_involved = [(2, 0), (2, 1)]
    targets_involved = [0, 1, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[0] = '吉尼斯世界' + goal[0]
            goal[1] = '最' + goal[1] + goal[2]
            goal[2] = '描述'
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['是']
        result = '; '.join(results)
        return ''.join(goal) + result


class Qiuyuancanjiajuesai(Class2Graph2):
    """哪些球员参加过2004-05赛季欧冠决赛"""
    words_involved = {0: (['哪些'], 'ATT'), 1: ('ANY', 'SBV'),
                      2: ('ANY', 'HED'),
                      3: ('ANY', 'ATT'), 4: (['赛季'], 'ATT'),
                      5: (['欧冠'], 'ATT'),
                      6: ('ANY', 'VOB')}
    relations_involved = [(2, 1), (2, 6), (1, 0), (6, 4), (6, 5), (4, 3)]
    targets_involved = [0, 2, 3, 5, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[3] = goal[3] + goal[4]
            goal = goal[:4]
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result


class Qiuyuansilierendai(Class2Graph3):
    """哪些球员撕裂过膝盖十字韧带"""
    words_involved = {0: (['哪些'], 'ATT'), 1: ('ANY', 'SBV'),
                      2: ('ANY', 'HED'),
                      3: (['膝盖'], 'VOB'), 4: (['十字韧带'], 'VOB')}
    relations_involved = [(2, 1), (2, 3), (2, 4), (1, 0)]
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


class Peiyangguojiao(Class5Graph1):
    """哪家俱乐部既培养了日本国脚，也培养了韩国国脚"""
    words_involved = {0: ('ANY', ['ATT']), 1: ('ANY', ['SBV']),
                      2: (['培养'], ['HED']),
                      3: ('ANY', ['ATT']), 4: (['国脚'], 'VOB'),
                      5: ('ANY', ['COO']), 6: ('ANY', ['ATT']),
                      7: (['国脚'], 'VOB')}
    relations_involved = [(2, 1), (2, 4), (2, 5), (1, 0), (4, 3), (5, 7),
                          (7, 6)]
    targets_involved = [1, 3, 6]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            # goal[1] = goal[1] + '国家队'
            # goal[2] = goal[2] + '国家队'
            goal.append('青训')
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3in(Class3Graph3):
    """马拉多纳转会巴塞罗那的时间"""
    template_name = 'SbvHedVob3in'
    words_involved = {0: ('ANY', 'SBV'), 1: (['转会'], 'ATT'),
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


class SbvHedVob3inin(Class3Graph3):
    """马拉多纳转会巴塞罗那"""
    words_involved = {0: ('ANY', 'SBV'), 1: (['转会'], 'HED'),
                      2: ('ANY', 'VOB')}
    relations_involved = [(1, 0), (1, 2)]
    targets_involved = [0, 1, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            goal.append(['情况', relation('情况')])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob4(Class4Graph1):
    """马拉多纳从哪里转会巴塞罗那；xx从yy做xx，问yy"""
    template_name = 'SbvHedVob4'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ADV'),
                      2: ('ANY', 'POB'), 3: ('ANY', 'HED'),
                      4: ('ANY', 'VOB')}
    relations_involved = [(3, 0), (3, 1), (3, 4), (1, 2)]
    targets_involved = [0, 3, 4]

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


class Qimaodun(Class3Graph2):
    """穆里尼奥起矛盾的对手；穆里尼奥和谁起过矛盾"""
    words_involved = {0: ('ANY', ['SBV']), 1: (['谁'], 'COO'),
                      2: ('ANY', 'HED'), 3: (['矛盾', '冲突'], 'VOB')}
    relations_involved = [(2, 0), (2, 3), (0, 1)]
    targets_involved = [0, 2, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[1] = goal[1] + goal[2]
            goal[2] = '哪些'
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedAttVob(Class3Graph1):
    """巴雷西如何评价马拉多纳的技术"""
    template_name = 'SbvHedAttVob'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'ADV'), 2: ('ANY', 'HED'),
                      3: ('ANY', 'ATT'), 4: (['技术', '性格'], 'VOB')}
    relations_involved = [(2, 0), (2, 1), (2, 4), (4, 3)]
    targets_involved = [0, 2, 3, 4]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = [goal[3][0] + goal[1][0]]
            goal[3] = [extra[0], relation(extra[0])]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '这样', temp[1], temp[2], '的', temp[3], ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedAttVob2(Class3Graph1):
    """巴雷西评价马拉多纳的技术"""
    template_name = 'SbvHedAttVob2'
    words_involved = {0: ('ANY', 'SBV'), 1: ('ANY', 'HED'),
                      2: ('ANY', 'ATT'), 3: (['技术', '性格'], 'VOB')}
    relations_involved = [(1, 0), (1, 3), (3, 2)]
    targets_involved = [0, 1, 2, 3]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_self()
                    for node in self.targets_involved]
            extra = [goal[3][0] + goal[1][0]]
            # print(extra[0])
            try:
                goal[3] = [extra[0], relation(extra[0])]
            except KeyError:
                goal[3] = [extra[0], 'aiball:unknown']
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '这样', temp[1], temp[2], '的', temp[3], ': ']
        result = '; '.join(results)
        return ''.join(goal) + result


class Maodunjiye(Class5Graph2):
    """哪些人既和PRESON0有矛盾，也和PERSON1有矛盾"""
    words_involved = {0: (['哪些'], 'ATT'), 1: (['人', '球员', '教练'], 'SBV'),
                      2: (['大卫·路易斯', '迭戈·科斯塔', '大卫路易斯', '迭戈科斯塔',
                           'PERSON0', 'PERSON1'], 'SBV'),
                      3: ('ANY', 'HED'), 4: ('ANY', 'VOB'),
                      5: (['和'], 'ADV'), 6: ('ANY', 'POB'),
                      7: ('ANY', 'COO'), 8: ('ANY', 'VOB')}
    relations_involved = [(3, 1), (3, 2), (3, 4), (3, 7), (1, 0), (7, 5),
                          (7, 8), (5, 6)]
    targets_involved = [2, 3, 4, 6, 0]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal[1] = goal[1] + goal[2]
            goal[2] = goal[3]
            goal[3] = goal[4]
            goal = goal[:4]
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result


class Qiuyuanchuziqiu(Class3Graph4):
    """哪些球员在面对意大利的时候收获处子球"""
    words_involved = {0: (['哪些'], 'ATT'), 1: ('ANY', 'SBV'),
                      2: ('ANY', 'ADV'),
                      3: (['面对', '对阵'], 'ATT'), 4: ('ANY', 'VOB'),
                      5: ('ANY', 'POB'), 6: ('ANY', 'HED'),
                      7: ('ANY', 'VOB')}
    relations_involved = [(6, 1), (6, 2), (6, 7), (1, 0), (2, 5), (5, 3),
                          (3, 4)]
    targets_involved = [0, 4, 7]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal.append('对手')
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result


class Qiuyuanchuziqiu2(Class3Graph4):
    """哪些球员在面对意大利时候收获处子球"""
    words_involved = {0: (['哪些'], 'ATT'), 1: ('ANY', 'SBV'),
                      2: (['在'], 'ADV'),
                      3: (['面对', '对阵'], 'ADV'), 4: ('ANY', 'ATT'),
                      5: ('ANY', 'POB'), 6: ('ANY', 'HED'),
                      7: ('ANY', 'VOB')}
    relations_involved = [(6, 1), (6, 2), (6, 7), (1, 0), (3, 5), (6, 3),
                          (5, 4)]
    targets_involved = [0, 4, 7]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            goal.append('对手')
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result


class Zujienaxieqiuxing(Class3Graph2):
    """沃特福德租借过哪些球星"""
    words_involved = {0: ('ANY', ['SBV']),
                      1: (['租借'], ['HED']), 2: (['什么', '啥', '哪些'], ['ATT']),
                      3: ('ANY', ['VOB'])}
    relations_involved = [(1, 0), (1, 3), (3, 2)]
    targets_involved = [0, 1, 2]

    def target(self, rule_target, mapping, words, arcs):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in self.targets_involved]
            return get_content_verb(goal)

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = ['包括']
        result = '; '.join(results)
        return ''.join(goal) + result
