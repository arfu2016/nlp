"""
@Project   : CubeGirl
@Module    : tpl3_words.py
@Author    : Deco [deco@cubee.com]
@Created   : 2/6/18 10:50 AM
@Desc      : 
"""
from .class1_strict import Class2Graph1Too, Class3Graph1Too, Class1Graph2Too, \
    Class2Graph2Too, Class2Graph3Too, Class5Graph1Too, Class3Graph3Too, \
    Class3Graph2Too, \
    Class5Graph2Too, Class3Graph4Too, Class4Graph1Too, Class4Graph3Too
from .depy_relation import OneTermForTpl, relation, get_content_verb
from .depy_transfer import team_names, country_names


class Maozixifa2(Class2Graph1Too):
    """马拉多纳帽子戏法;乔戈麦斯首秀；xx yy"""
    relations_involved = [None, ['帽子戏法', '首秀']]

    def target(self, rule_target, words):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            goal = [OneTermForTpl(word).get_self() for word in words]
            extra = ['情况']
            goal.append((extra[0], relation(extra[0])))
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class Zhuanhuiboka(Class4Graph1Too):
    """马拉多纳从哪里转会博卡青年"""
    relations_involved = [None, ['从'], None, ['转会'], None]

    def target(self, rule_target, words):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            words2 = [words[i] for i in [0, 3, 4]]
            goal = [OneTermForTpl(word).get_self() for word in words2]
            goal.insert(2, ['从', 'Out'])
            goal.insert(3, ['到', 'In'])
            extra = ['名字']
            goal.append([extra[0], relation(extra[0])])
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3inshijian(Class3Graph3Too):
    """马拉多纳转会巴塞罗那时间"""
    relations_involved = [None, ['转会'], team_names,
                          None]

    def target(self, rule_target, words):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            words2 = [words[i] for i in [0, 1, 2, 3]]
            goal = [OneTermForTpl(word).get_self() for word in words2]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3zhijiaoshijian(Class3Graph1Too):
    """马拉多纳执教阿根廷队情况"""
    relations_involved = [None, ['执教'], team_names+country_names,
                          ['情况', '时间']]

    def target(self, rule_target, words):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            words2 = [words[i] for i in [0, 1, 2, 3]]
            goal = [OneTermForTpl(word).get_self() for word in words2]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class SbvHedVob3incongshijian(Class3Graph3Too):
    """马拉多纳从博卡青年转会巴塞罗那时间"""
    relations_involved = [None, ['从'], None, ['转会'], None, ['时间']]

    def target(self, rule_target, words):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            words2 = [words[i] for i in [0, 3, 4, 5]]
            goal = [OneTermForTpl(word).get_self() for word in words2]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class Intent0Style0(Class4Graph3Too):
    """鲁尼俱乐部队友入选英格兰国家队有哪些"""
    relations_involved = [None, ['俱乐部'], ['队友'], ['入选'], None, ['国家队'],
                          ['有'], ['哪些']]
    selects = [0, 1, 4, 5, 7]

    @staticmethod
    def insert(existing_entity):
        """
        existing_entity.insert, existing_entity.append
        :param existing_entity: List
        :return:
        """
        return existing_entity
