"""
@Project   : CubeGirl
@Module    : class2_general.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/12/18 1:10 PM
@Desc      : 
"""
from .depy_dsl import HasProperty, ArelationB, IsRelatedTo, IsRelatedTo2
from .depy_parsing import QuestionGraph
from .depy_relation import aiballclass


class Class1Graph(QuestionGraph):
    """
    Graph template for questions like "ATT的HED"
    Ex: "梅西的身高", "角球的定义"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target1_n = '"{}"'.format(target[0][0])
        target1_v = target[0][1]
        target2_v = target[1][1]

        thing = HasProperty(target1_n, target1_v)
        goal = ArelationB(thing, target2_v)
        return goal


class Class1Graph2(QuestionGraph):
    """
    Graph template for questions like "ATT的HED"
    Ex: '吉尼斯世界纪录的最远进球'
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # '吉尼斯世界纪录'

        target1_n = '"{}"'.format(target[1][0])
        target1_v = target[1][1]
        # '最远进球'

        target2_v = target[2][1]
        # '描述'

        thing0 = HasProperty(target0_n, target0_v)
        thing1 = HasProperty(target1_n, target1_v)
        thing0.merge(thing1)
        goal = ArelationB(thing0, target2_v)
        return goal


class Class1Graph3(QuestionGraph):
    """
    Graph template for questions like "ATT的HED"
    Ex: '2011年11月12日，在英格兰1: 0战胜西班牙的友谊赛中，巴里是否首发出场了'
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # '2011年11月12日'

        target1_n = '"{}"'.format(target[1][0])
        target1_v = target[1][1]
        # '英格兰vs西班牙'

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 巴里

        target3_n = '"{}"'.format(target[3][0])
        target3_v = target[3][1]
        # 首发出场

        target4_v = target[4][1]
        # 描述

        # zhuyu1 = IsRelatedTo(thing2, reverse=False)
        thing0 = HasProperty(target0_n, 'aiball:time')
        thing1 = HasProperty(target1_n, 'aiball:match')
        thing0.merge(thing1)
        thing2 = HasProperty(target2_n, target2_v)
        thing0.merge(thing2)
        thing3 = HasProperty(target3_n, target3_v)
        thing0.merge(thing3)
        goal = ArelationB(thing0, target4_v)
        return goal


class Class2Graph1(QuestionGraph):
    """
    Graph template for questions
    Ex: "马拉多纳一球成名的对手; 马拉多纳一球成名的描述"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 马拉多纳

        target1_v = target[1][1]
        # 一球成名

        target2_v = target[2][1]
        # 对手

        thing1 = HasProperty(target0_n, target0_v)

        binyu1 = ArelationB(thing1, target1_v, reverse=True)
        goal = ArelationB(binyu1, target2_v, reverse=True)

        return goal


class Class2Graph2(QuestionGraph):
    """
    Graph template for questions
    Ex: 哪些球员参加过2004-05赛季欧冠决赛
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_v = target[0][1]
        # 哪些

        target1_v = target[1][1]
        # 参加

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 2004-05

        target3_n = '"{}"'.format(target[3][0])
        target3_v = target[3][1]
        # 欧冠决赛

        thing2 = HasProperty(target2_n, 'aiball:season')
        thing3 = HasProperty(target3_n, target3_v)
        thing2.merge(thing3)

        zhuyu1 = ArelationB(thing2, target1_v, reverse=False)
        goal = ArelationB(zhuyu1, target0_v, reverse=True)

        return goal


class Class2Graph3(QuestionGraph):
    """
    Graph template for questions
    Ex: 哪些球员撕裂过膝盖十字韧带
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_v = target[0][1]
        # 哪些

        target1_v = target[1][1]
        # 撕裂

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 膝盖十字韧带

        thing2 = HasProperty(target2_n, target2_v)

        zhuyu1 = ArelationB(thing2, target1_v, reverse=False)
        goal = ArelationB(zhuyu1, target0_v, reverse=True)

        return goal


class Class3Graph1(QuestionGraph):
    """
    Graph template for questions like
    Ex: "巴雷西评价马拉多纳, 谓语的技术评价"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 巴雷西

        target1_v = target[1][1]
        # 评价

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 马拉多纳

        target4_v = target[3][1]
        # 技术评价

        thing1 = HasProperty(target0_n, target0_v)
        binyu1 = ArelationB(thing1, target1_v, reverse=True)

        thing2 = HasProperty(target2_n, target2_v)
        zhuyu1 = IsRelatedTo(thing2, reverse=False)

        binyu1.merge(zhuyu1)
        goal = ArelationB(binyu1, target4_v)
        return goal


class Class3Graph2(QuestionGraph):
    """
    Graph template for questions like
    Ex: 河床青训培养过哪些球员
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 河床

        target1_n = aiballclass(target[1][0])
        target1_v = target[1][1]
        # 青训

        target2_v = target[2][1]
        # 哪些

        # target3_v = target[3][1]
        # 青训动词

        thing1 = HasProperty(target0_n, target0_v)
        zhuyu1 = IsRelatedTo(thing1, reverse=False)

        thing2 = HasProperty(target1_n, target1_v)
        zhuyu1.merge(thing2)
        zhuyu2 = IsRelatedTo2(zhuyu1, reverse=False)

        goal = ArelationB(zhuyu2, target2_v)
        return goal


class Class3Graph3(QuestionGraph):
    """
    Graph template for questions like
    Ex: "马拉多纳转会巴塞罗那, 谓语的时间"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 马拉多纳

        target1_v = target[1][1]
        # 转会
        target1_v_in = target[1][1] + 'In'

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 巴塞罗那

        target4_v = target[3][1]
        # 时间

        thing1 = HasProperty(target0_n, target0_v)
        binyu1 = ArelationB(thing1, target1_v, reverse=True)

        thing2 = HasProperty(target2_n, target2_v)
        zhuyu1 = ArelationB(thing2, target1_v_in, reverse=False)

        binyu1.merge(zhuyu1)
        goal = ArelationB(binyu1, target4_v)
        return goal


class Class3Graph4(QuestionGraph):
    """
    Graph template for questions like
    Ex: 对手意大利处子球过哪些球员
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 哪些

        target1_n = '"{}"'.format(target[1][0])
        target1_v = target[1][1]
        # 意大利

        target2_n = aiballclass(target[2][0])
        target2_v = target[2][1]
        # 处子球

        target3_v = target[3][1]
        # 对手

        thing1 = HasProperty(target1_n, target1_v)
        zhuyu1 = ArelationB(thing1, target3_v, reverse=False)

        thing2 = HasProperty(target2_n, target2_v)
        zhuyu1.merge(thing2)

        zhuyu2 = IsRelatedTo2(zhuyu1, reverse=False)

        goal = ArelationB(zhuyu2, target0_v)
        return goal


class Class3Graph5(QuestionGraph):
    """
    Graph template for questions like
    Ex: "李白写过哪些饮酒诗"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 李白

        target1_v = target[1][1]
        # 写

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 饮酒诗

        target4_v = target[3][1]
        # 哪些

        thing1 = HasProperty(target0_n, target0_v)
        binyu1 = ArelationB(thing1, target1_v, reverse=True)

        binyu2 = IsRelatedTo(binyu1, reverse=True)
        thing2 = HasProperty(target2_n, target2_v)

        binyu2.merge(thing2)
        goal = ArelationB(binyu2, target4_v)
        return goal


class Class4Graph1(QuestionGraph):
    """
    Graph template for questions like
    Ex: 马拉多纳从哪里转会巴塞罗那
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 马拉多纳

        target1_v = target[1][1]
        # 转会

        target1_v_prime = target[1][1] + target[2][1]
        # 后缀1，从
        target1_v_prime2 = target[1][1] + target[3][1]
        # 后缀2，到

        target3_n = '"{}"'.format(target[4][0])
        target3_v = target[4][1]
        # 巴塞罗那

        target4_v = target[5][1]
        # 名字

        thing1 = HasProperty(target0_n, target0_v)
        binyu1 = ArelationB(thing1, target1_v, reverse=True)

        thing2 = HasProperty(target3_n, target3_v)
        binyu2 = ArelationB(thing2, target1_v_prime2, reverse=False)

        binyu1.merge(binyu2)

        binyu3 = ArelationB(binyu1, target1_v_prime, reverse=True)
        goal = ArelationB(binyu3, target4_v)
        return goal


class Class4Graph2(QuestionGraph):
    """
    Graph template for questions like
    Ex: 马拉多纳从博卡青年转会到哪里
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 马拉多纳

        target1_v = target[1][1]
        # 转会

        target1_v_prime = target[1][1] + target[2][1]
        # 后缀1, 从
        target1_v_prime2 = target[1][1] + target[3][1]
        # 后缀2，到

        target3_n = '"{}"'.format(target[4][0])
        target3_v = target[4][1]
        # 博卡青年

        target4_v = target[5][1]
        # 名字

        thing1 = HasProperty(target0_n, target0_v)
        binyu1 = ArelationB(thing1, target1_v, reverse=True)

        thing2 = HasProperty(target3_n, target3_v)
        binyu2 = ArelationB(thing2, target1_v_prime, reverse=False)

        binyu1.merge(binyu2)

        binyu3 = ArelationB(binyu1, target1_v_prime2, reverse=True)
        goal = ArelationB(binyu3, target4_v)
        return goal


class Class4Graph3(QuestionGraph):
    """
    Graph template for questions like
    Ex: "鲁尼俱乐部的队友入选英格兰国家队的有哪些"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 鲁尼

        target1_n = '"{}"'.format(target[1][0])
        target1_v = target[1][1]
        # 俱乐部

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 英格兰队

        target3_n = '"{}"'.format(target[3][0])
        target3_v = target[3][1]
        # 国家队

        target4_v = target[4][1]
        # 哪些

        thing1 = HasProperty(target0_n, target0_v)
        binyu1 = IsRelatedTo(thing1, reverse=True)

        thing2 = HasProperty(target1_n, target1_v)
        binyu1.merge(thing2)
        zhuyu1 = IsRelatedTo(binyu1, reverse=False)

        thing3 = HasProperty(target2_n, target2_v)
        thing4 = HasProperty(target3_n, target3_v)
        thing3.merge(thing4)
        zhuyu2 = IsRelatedTo(thing3, reverse=False)

        zhuyu1.merge(zhuyu2)

        goal = ArelationB(zhuyu1, target4_v)
        return goal


class Class5Graph1(QuestionGraph):
    """
    Graph template for questions like
    Ex: "哪家俱乐部既培养了日本国脚，也培养了韩国国脚"
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 俱乐部

        target1_n = '"{}"'.format(target[1][0])
        target1_v = target[1][1]
        # 日本国家队

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 韩国国家队

        # target3_n = '"{}"'.format(target[3][0])
        target3_n = aiballclass(target[3][0])
        target3_v = target[3][1]
        # 青训

        target4_v = 'aiball:cnName'
        # 哪些

        zhuyu3 = HasProperty(target1_n, target1_v)
        zhuyu1 = ArelationB(zhuyu3, 'aiball:team', reverse=False)
        binyu1 = IsRelatedTo2(zhuyu1, reverse=True)

        thing2 = HasProperty(target3_n, target3_v)
        # 青训节点
        thing2.merge(binyu1)

        zhuyu5 = HasProperty(target2_n, target2_v)
        zhuyu2 = ArelationB(zhuyu5, 'aiball:team', reverse=False)
        binyu4 = IsRelatedTo2(zhuyu2, reverse=True)

        thing3 = HasProperty(target3_n, target3_v)
        thing3.merge(binyu4)

        binyu3 = IsRelatedTo(thing2, reverse=True)
        binyu4 = IsRelatedTo(thing3, reverse=True)
        binyu3.merge(binyu4)

        thing1 = HasProperty(target0_n, target0_v)
        binyu3.merge(thing1)
        # 俱乐部节点

        goal = ArelationB(binyu3, target4_v)
        return goal


class Class5Graph2(QuestionGraph):
    """
    Graph template for questions like
    Ex: 哪些人既和大卫·路易斯有矛盾，也和迭戈·科斯塔有矛盾
    """
    def graph(self, target):
        """
        target is constant data derived from natural language
        :param target:
        :return:
        """
        target0_n = '"{}"'.format(target[0][0])
        target0_v = target[0][1]
        # 大卫·路易斯

        target1_n = aiballclass(target[1][0])
        target1_v = target[1][1]
        # 有矛盾

        target2_n = '"{}"'.format(target[2][0])
        target2_v = target[2][1]
        # 迭戈·科斯塔

        target3_v = target[3][1]
        # 哪些

        thing1 = HasProperty(target0_n, target0_v)
        zhuyu1 = IsRelatedTo(thing1, reverse=False)
        thing11 = HasProperty(target1_n, target1_v)
        zhuyu1.merge(thing11)

        thing2 = HasProperty(target2_n, target2_v)
        zhuyu2 = IsRelatedTo(thing2, reverse=False)
        thing22 = HasProperty(target1_n, target1_v)
        zhuyu2.merge(thing22)

        zhuyu3 = IsRelatedTo2(zhuyu1, reverse=False)
        zhuyu4 = IsRelatedTo2(zhuyu2, reverse=False)
        zhuyu3.merge(zhuyu4)

        goal = ArelationB(zhuyu3, target3_v)
        return goal
