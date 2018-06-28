"""
@Project   : CubeGirl
@Module    : tpl5_syntac.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/15/18 10:52 AM
@Desc      : 句法模板
"""
from .class4_syntac import Class1Graph
from .depy_relation import OneTermForSyntac
from .class_registry import register_syntac

syntac_dict = dict()


@register_syntac(syntac_dict)
class AttHedTree(Class1Graph):
    """梅西的身高；xx的xx"""
    words_for_syntac = {0: ('ANY', 'ATT'), 1: ('ANY', 'HED')}
    syntac_tree = [(1, 0)]
    targets_for_syntac = [0, 1]

    def target(self, rule_true):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_true:
            goal = [OneTermForSyntac(self.mapping[node], self.words,
                                     self.arcs).get_self()
                    for node in self.targets_for_syntac]
            goal = self.insert(goal)
            return goal

    @staticmethod
    def insert(existing_entity):
        """
        是对target函数的补充，用于非常灵活的实体抽取，可以重载、修改本函数
        existing_entity.insert(), existing_entity.append()
        :param existing_entity: List
        :return: List
        """
        return existing_entity
