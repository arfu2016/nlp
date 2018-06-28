"""
@Project   : CubeGirl
@Module    : tpl4_sparql.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/2/18 5:26 PM
@Desc      : Sparql template which matches the language sequence
"""
from .class_registry import registered_classes, register_class
from .class3_sparql import (WorldCup1,
                            WorldCup2,
                            WorldCup4,
                            WorldCup8, WorldCup9,
                            WorldCup10, WorldCup11,
                            WorldCup12, WorldCup13,
                            WorldCup14,
                            WorldCup21,
                            WorldCup22,
                            WorldCup24, WorldCup25,
                            WorldCup26,
                            )


@register_class
class WorldCup1Id0(WorldCup1):
    """哪些球员是俱乐部队友"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], None, ['俱乐部'], ['队友']]
    selects = []


@register_class
class WorldCup1Id1(WorldCup1):
    """谁是俱乐部队友"""
    relations_involved = [['谁', '哪些'], None, ['俱乐部'], ['队友']]
    selects = []


@register_class
class WorldCup1Id2(WorldCup1):
    """哪些球员在同一个俱乐部"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], None, ['同一个'], ['俱乐部']]
    selects = []


@register_class
class WorldCup1Id3(WorldCup1):
    """哪些球员在同一个俱乐部踢球"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], None,
                          ['同一个'], ['俱乐部'], None]
    selects = []


@register_class
class WorldCup1Id4(WorldCup1):
    """谁在同一个俱乐部"""
    relations_involved = [['谁', '哪些'], None, ['同一个', '同一家'], ['俱乐部']]
    selects = []


@register_class
class WorldCup1Id5(WorldCup1):
    """谁在同一个俱乐部踢球"""
    relations_involved = [['谁', '哪些'], None, ['同一个', '同一家'], ['俱乐部'], None]
    selects = []


@register_class
class WorldCup1Id6(WorldCup1):
    """哪些球员效力于同一个俱乐部"""
    relations_involved = [None, ['球员', '球星', '队员', '人'],
                          ['效力'], ['同一个', '同一家'], ['俱乐部']]
    selects = []


@register_class
class WorldCup2Id0(WorldCup2):
    """哪些球员俱乐部是死敌"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], ['俱乐部'], None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id1(WorldCup2):
    """谁俱乐部是死敌"""
    relations_involved = [['谁'], ['俱乐部'], None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id2(WorldCup2):
    """哪些球员效力球队是死敌"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], ['效力', '踢球'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id3(WorldCup2):
    """哪些球员当时效力球队是死敌"""
    relations_involved = [None, ['球员', '球星', '队员', '人'],
                          ['当时'], ['效力', '踢球', '所在'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id4(WorldCup2):
    """哪些球员当时所效力球队是死敌"""
    relations_involved = [None, ['球员', '球星', '队员', '人'],
                          ['当时'], None, ['效力', '踢球', '所在'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id5(WorldCup2):
    """哪些球员所效力球队是死敌"""
    relations_involved = [None, ['球员', '球星', '队员', '人'],
                          None, ['效力', '踢球', '所在'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id6(WorldCup2):
    """当前场上哪些球员当时效力的球队是死敌"""
    relations_involved = [['当前', '现在'], ['场上'], None, ['球员', '球星', '队员', '人'],
                          ['当时'], ['效力', '踢球', '所在'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = []


@register_class
class WorldCup2Id7(WorldCup2):
    """当前场上哪些球员当时所效力的球队是死敌"""
    relations_involved = [['当前', '现在'], ['场上'], None, ['球员', '球星', '队员', '人'],
                          ['当时'], None, ['效力', '踢球', '所在'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = []


@register_class
class WorldCup4Id0(WorldCup4):
    """哪些球员儿子是球员"""
    relations_involved = [None, ['球员', '球星', '队员'], ['儿子'],
                          None, ['球员']]
    selects = [4]

    @staticmethod
    def insert(existing_entity):
        """existing_entity.insert, existing_entity.append"""
        return existing_entity


@register_class
class WorldCup4Id1(WorldCup4):
    """谁儿子是球员"""
    relations_involved = [['谁'], ['儿子'],
                          None, ['球员']]
    selects = [3]


@register_class
class WorldCup8Id0(WorldCup8):
    """哪些西德球员是俱乐部队友"""
    relations_involved = [None, ['西德', '德国', '英格兰'], ['球员', '球星', '队员', '人'],
                          None, ['俱乐部'], ['队友']]
    selects = [1]


@register_class
class WorldCup8Id1(WorldCup8):
    """哪些西德球员效力于同一个俱乐部"""
    relations_involved = [None, ['西德', '德国', '英格兰'], ['球员', '球星', '队员', '人'],
                          ['效力'], ['同一个', '同一家'], ['俱乐部']]
    selects = [1]


@register_class
class WorldCup9Id0(WorldCup9):
    """两队球员效力于哪些俱乐部"""
    relations_involved = [['两'], ['队'], ['球员', '球星', '队员', '人'], ['效力'],
                          None, ['俱乐部']]
    selects = []


@register_class
class WorldCup10Id0(WorldCup10):
    """西德球员效力于哪些俱乐部"""
    relations_involved = [['西德', '德国', '英格兰'], ['球员', '球星', '队员', '人'], ['效力'],
                          None, ['俱乐部']]
    selects = [0]


@register_class
class WorldCup11Id0(WorldCup11):
    """哪些球员效力于切尔西"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], ['效力'],
                          None]
    selects = [3]


@register_class
class WorldCup11Id1(WorldCup11):
    """哪些球员效力于切尔西"""
    relations_involved = [None, ['球员', '球星', '队员', '人'], ['效力'],
                          None, None, ['巡游者']]
    selects = [5]


@register_class
class WorldCup12Id0(WorldCup12):
    """哪些西德球员效力于切尔西"""
    relations_involved = [None, ['西德', '德国', '英格兰'],
                          ['球员', '球星', '队员', '人'], ['效力'],
                          None]
    selects = [1, 4]


@register_class
class WorldCup13Id0(WorldCup13):
    """哪些球员儿子是守门员"""
    relations_involved = [None, ['球员', '球星', '队员'], ['儿子'],
                          None, ['守门员', '前锋', '中场', '后卫', '门将']]
    selects = [4]

    @staticmethod
    def insert(existing_entity):
        """existing_entity.insert, existing_entity.append"""
        return existing_entity


@register_class
class WorldCup13Id1(WorldCup13):
    """谁儿子是守门员"""
    relations_involved = [['谁'], ['儿子'],
                          None, ['守门员', '前锋', '中场', '后卫', '门将']]
    selects = [3]


@register_class
class WorldCup14Id1(WorldCup14):
    """克林斯曼的儿子是踢什么位置的"""
    relations_involved = [None, ['儿子'], None,
                          None, None, ['位置']]
    selects = [0]


@register_class
class WorldCup14Id2(WorldCup14):
    """克林斯曼的儿子踢什么位置的"""
    relations_involved = [None, ['儿子'],
                          None, None, ['位置']]
    selects = [0]


@register_class
class WorldCup21Id0(WorldCup21):
    """哪些英格兰球员俱乐部是死敌"""
    relations_involved = [None, ['西德', '德国', '英格兰'],
                          ['球员', '球星', '队员', '人'], ['俱乐部'],
                          None, ['死敌']]
    selects = [1]


@register_class
class WorldCup21Id1(WorldCup21):
    """哪些英格兰球员效力球队是死敌"""
    relations_involved = [None, ['西德', '德国', '英格兰'], ['球员', '球星', '队员', '人'], ['效力', '踢球'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = [1]


@register_class
class WorldCup21Id2(WorldCup21):
    """哪些英格兰球员当时效力球队是死敌"""
    relations_involved = [None, ['西德', '德国', '英格兰'], ['球员', '球星', '队员', '人'],
                          ['当时'], ['效力', '踢球', '所在'], ['俱乐部', '球队'],
                          None, ['死敌']]
    selects = [1]


@register_class
class WorldCup22Id0(WorldCup22):
    """马特乌斯妻子是谁"""
    relations_involved = [None, ['妻子', '老婆', '太太', '夫人', '媳妇'],
                          None, ['谁']]
    selects = [0]


@register_class
class WorldCup22Id1(WorldCup22):
    """利特巴尔斯基妻子是谁"""
    relations_involved = [['利特'], ['巴尔斯基'], ['妻子', '老婆', '太太', '夫人', '媳妇'],
                          None, ['谁']]
    selects = [1]


@register_class
class WorldCup24Id0(WorldCup24):
    """马特乌斯离过几次婚"""
    relations_involved = [None, ['离'],
                          None, ['婚']]
    selects = [0]


@register_class
class WorldCup25Id0(WorldCup25):
    """哪个球员离婚次数最多"""
    relations_involved = [None, ['球员', '球星', '队员', '人'],
                          ['离婚'], ['次数'], ['最'], ['多']]
    selects = []


@register_class
class WorldCup25Id1(WorldCup25):
    """场上哪个球员离婚次数最多"""
    relations_involved = [['场上'], None, ['球员', '球星', '队员', '人'],
                          ['离婚'], ['次数'], ['最'], ['多']]
    selects = []


@register_class
class WorldCup26Id0(WorldCup26):
    """哪个球员老婆最漂亮"""
    relations_involved = [None, ['球员', '球星', '队员', '人'],
                          ['妻子', '老婆', '太太', '夫人', '媳妇'],
                          ['最'], ['漂亮', '美丽']]
    selects = []


@register_class
class WorldCup26Id1(WorldCup26):
    """谁老婆最漂亮"""
    relations_involved = [None,
                          ['妻子', '老婆', '太太', '夫人', '媳妇'],
                          ['最'], ['漂亮', '美丽']]
    selects = []


@register_class
class WorldCup26Id2(WorldCup26):
    """场上哪个球员老婆最漂亮"""
    relations_involved = [['场上'], None, ['球员', '球星', '队员', '人'],
                          ['妻子', '老婆', '太太', '夫人', '媳妇'],
                          ['最'], ['漂亮', '美丽']]
    selects = []


@register_class
class WorldCup26Id3(WorldCup26):
    """场上谁老婆最漂亮"""
    relations_involved = [['场上'], None,
                          ['妻子', '老婆', '太太', '夫人', '媳妇'],
                          ['最'], ['漂亮', '美丽']]
    selects = []
