"""
@Project   : CubeGirl
@Module    : depy_relation.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/24/18 10:26 AM
@Desc      : 词与知识图谱关系的对应，以及句子中词与词的关系
"""
from collections import defaultdict
from . import depy_transfer as transfer

namespace = "aiball"
namespace2 = "rdf"


def relation(content):
    mapping_dict = {'梅西': namespace + ':cnName',
                    '身高': namespace + ':height',
                    '女友': namespace + ':girlFriend',
                    '角球': namespace + ':cnName',
                    '定义': namespace + ':definition',
                    '妈妈': namespace + ':mother',
                    '名字': namespace + ':cnName',
                    '帽子戏法': namespace + ':hatTrick',
                    '用时': namespace + ':time',
                    '赞扬': namespace + ':praise',
                    '签约': namespace + ':sign',
                    '巴萨': namespace + ':cnName',
                    '时间': namespace + ':time',
                    '生日': namespace + ':birthDate',
                    '开始日期': namespace + ':birthDate',
                    '参加': namespace + ':participate',
                    '世界杯': namespace + ':cnName',
                    '决赛': namespace + ':final',
                    '情况': namespace + ':description',
                    '打破': namespace + ':breakOrReverse',
                    '纪录': namespace + ':cnName',
                    '描述': namespace + ':description',
                    '巴里': namespace + ':cnName',
                    '阿根廷队': namespace + ':cnName',
                    '阿根廷国家队': namespace + ':cnName',
                    '进球': namespace + ':haveGoalIn',
                    '进球数': namespace + ':goalNumber',
                    '球王': namespace + ':cnName',
                    '是': namespace + ':is',
                    '有': namespace + ':have',
                    '夺冠': namespace + ':champion',
                    '首次': namespace + ':cnName',
                    '认识': namespace + ':knows',
                    '皮克': namespace + ':cnName',
                    '哪': namespace + ':location',
                    '阿圭罗': namespace + ':cnName',
                    '马拉多纳': namespace + ':cnName',
                    '一球成名': namespace + ':goalFamous',
                    '对手': namespace + ':rival',
                    '技术评价': namespace + ':techComment',
                    '巴雷西': namespace + ':cnName',
                    '评价': namespace + ':comment',
                    '技术': namespace + ':technique',
                    '转会': namespace + ':transfer',
                    '巴塞罗那': namespace + ':cnName',
                    '博卡青年': namespace + ':cnName',
                    '所属球队': namespace + ':team',
                    '结果': namespace + ':result',
                    '比赛': namespace + ':match',
                    '莱因克尔': namespace + ':cnName',
                    '上演': namespace + ':play',
                    '首次进球': namespace + ':firstGoal',
                    '首次出场': namespace + ':debut',
                    '出场': namespace + ':appear',
                    '球队': namespace + ':team',
                    '执教': namespace + ':coachExp',
                    '开始时间': namespace + ':startTime',
                    '结束时间': namespace + ':endTime',
                    '英格兰': namespace + ':cnName',
                    '英格兰队': namespace + ':cnName',
                    '鲁尼': namespace + ':cnName',
                    '费尔南迪尼奥': namespace + ':cnName',
                    '德布劳内': namespace + ':cnName',
                    '哪些': namespace + ':cnName',
                    '俱乐部': namespace + ':type',
                    '入选': namespace + ':team',
                    '布拉沃': namespace + ':cnName',
                    '皇家社会': namespace + ':cnName',
                    '竞技队': namespace + ':cnName',
                    '日本国家队': namespace + ':cnName',
                    '韩国国家队': namespace + ':cnName',
                    '加图索': namespace + ':cnName',
                    '时候': namespace + ':time',
                    '在': namespace + ':in',
                    '期间': namespace + ':type',
                    '什么': namespace + ':type',
                    '称呼': namespace + ':called',
                    '荣誉': namespace + ':honor',
                    '技术特点': namespace + ':techCharacter',
                    '擅长位置': namespace + ':skilfulPosition',
                    '擅长技术': namespace + ':skilfulTech',
                    '执教情况': namespace + ':coachResult',
                    '李白': namespace + ':cnName',
                    '贝勒': namespace + ':cnName',
                    '写': namespace + ':write',
                    '从事': namespace + ':do',
                    '职业': namespace + ':type',
                    '饮酒诗': namespace + ':type',
                    '吉尼斯世界纪录': namespace2 + ':type',
                    '首发出场': namespace2 + ':type',
                    '欧冠决赛': namespace2 + ':type',
                    '青训': namespace2 + ':type',
                    '有矛盾': namespace2 + ':type',
                    '起矛盾': namespace2 + ':type',
                    '世界杯冠军': namespace2 + ':type',
                    '最远进球': namespace + ':cnName',
                    '膝盖十字韧带': namespace + ':body',
                    '撕裂': namespace + ':tear',
                    '获得': namespace + ':obtain',
                    '河床': namespace + ':cnName',
                    '阿森纳': namespace + ':cnName',
                    '沙尔克': namespace + ':cnName',
                    '穆里尼奥': namespace + ':cnName',
                    '贝克汉姆': namespace + ':cnName',
                    '瓜迪奥拉': namespace + ':cnName',
                    '奥比昂': namespace + ':cnName',
                    '桑普多利亚': namespace + ':cnName',
                    '本田圭佑': namespace + ':cnName',
                    '那不勒斯': namespace + ':cnName',
                    '大卫·路易斯': namespace + ':cnName',
                    '迭戈·科斯塔': namespace + ':cnName',
                    '尤尔根·克林斯曼': namespace + ':cnName',
                    '日本': namespace + ':cnName',
                    '意大利': namespace + ':cnName',
                    '智利': namespace + ':cnName',
                    '因扎吉': namespace + ':cnName',
                    '贝尼特斯': namespace + ':cnName',
                    '波尔图': namespace + ':cnName',
                    '处子球': namespace2 + ':type',
                    '表现': namespace + ':performance',
                    '体重': namespace + ':weight',
                    '队长': namespace + ':caption',
                    '首秀': namespace + ':debut',
                    '加盟': namespace + ':transfer',
                    '租借': namespace2 + ':type',
                    '首球': namespace + ':firstGoal',
                    '妻子': namespace + ':futureWife',
                    '老婆': namespace + ':futureWife',
                    '儿子': namespace + ':son',
                    '国家队': namespace + ':type'}
    mapping_dict.update(transfer.relation_transfer)
    try:
        return mapping_dict[content]
    except KeyError:
        return 'aiball:unknown'


def relation_before(content):
    mapping_dict = {'梅西': namespace + ':cnName',
                    '角球': namespace + ':cnName',
                    '世界杯': namespace + ':cnName',
                    '纪录': namespace + ':cnName',
                    '巴里': namespace + ':cnName',
                    '阿根廷队': namespace + ':cnName',
                    '阿根廷国家队': namespace + ':cnName',
                    '球王': namespace + ':cnName',
                    '首次': namespace + ':cnName',
                    '皮克': namespace + ':cnName',
                    '阿圭罗': namespace + ':cnName',
                    '马拉多纳': namespace + ':cnName',
                    '巴雷西': namespace + ':cnName',
                    '巴塞罗那': namespace + ':cnName',
                    '博卡青年': namespace + ':cnName',
                    '莱因克尔': namespace + ':cnName',
                    '英格兰': namespace + ':cnName',
                    '英格兰队': namespace + ':cnName',
                    '鲁尼': namespace + ':cnName',
                    '费尔南迪尼奥': namespace + ':cnName',
                    '德布劳内': namespace + ':cnName',
                    '哪些': namespace + ':cnName',
                    '俱乐部': namespace + ':type',
                    '入选': namespace + ':team',
                    '布拉沃': namespace + ':cnName',
                    '皇家社会': namespace + ':cnName',
                    '竞技队': namespace + ':cnName',
                    '日本国家队': namespace + ':cnName',
                    '韩国国家队': namespace + ':cnName',
                    '加图索': namespace + ':cnName',
                    '期间': namespace + ':type',
                    '什么': namespace + ':type',
                    '李白': namespace + ':cnName',
                    '贝勒': namespace + ':cnName',
                    '职业': namespace + ':type',
                    '饮酒诗': namespace + ':type',
                    '吉尼斯世界纪录': namespace2 + ':type',
                    '首发出场': namespace2 + ':type',
                    '欧冠决赛': namespace2 + ':type',
                    '青训': namespace2 + ':type',
                    '有矛盾': namespace2 + ':type',
                    '起矛盾': namespace2 + ':type',
                    '世界杯冠军': namespace2 + ':type',
                    '最远进球': namespace + ':cnName',
                    '河床': namespace + ':cnName',
                    '阿森纳': namespace + ':cnName',
                    '沙尔克': namespace + ':cnName',
                    '穆里尼奥': namespace + ':cnName',
                    '贝克汉姆': namespace + ':cnName',
                    '瓜迪奥拉': namespace + ':cnName',
                    '奥比昂': namespace + ':cnName',
                    '桑普多利亚': namespace + ':cnName',
                    '本田圭佑': namespace + ':cnName',
                    '那不勒斯': namespace + ':cnName',
                    '大卫·路易斯': namespace + ':cnName',
                    '迭戈·科斯塔': namespace + ':cnName',
                    '尤尔根·克林斯曼': namespace + ':cnName',
                    '日本': namespace + ':cnName',
                    '意大利': namespace + ':cnName',
                    '智利': namespace + ':cnName',
                    '因扎吉': namespace + ':cnName',
                    '贝尼特斯': namespace + ':cnName',
                    '波尔图': namespace + ':cnName',
                    '处子球': namespace2 + ':type',
                    '租借': namespace2 + ':type',

                    '国家队': namespace + ':type'}
    mapping_dict.update(transfer.relation_transfer)
    return mapping_dict.get(content, 'aiball:unknown')


def relation_verb(content):
    mapping_dict = {
                    '身高': namespace + ':height',
                    '女友': namespace + ':girlFriend',
                    '定义': namespace + ':definition',
                    '妈妈': namespace + ':mother',
                    '名字': namespace + ':cnName',
                    '帽子戏法': namespace + ':hatTrick',
                    '用时': namespace + ':time',
                    '赞扬': namespace + ':praise',
                    '签约': namespace + ':sign',
                    '时间': namespace + ':time',
                    '生日': namespace + ':birthDate',
                    '开始日期': namespace + ':birthDate',
                    '参加': namespace + ':participate',
                    '决赛': namespace + ':final',
                    '情况': namespace + ':description',
                    '打破': namespace + ':breakOrReverse',
                    '描述': namespace + ':description',
                    '进球': namespace + ':haveGoalIn',
                    '进球数': namespace + ':goalNumber',
                    '是': namespace + ':is',
                    '有': namespace + ':have',
                    '夺冠': namespace + ':champion',
                    '认识': namespace + ':knows',
                    '哪': namespace + ':location',
                    '一球成名': namespace + ':goalFamous',
                    '对手': namespace + ':rival',
                    '技术评价': namespace + ':techComment',
                    '评价': namespace + ':comment',
                    '技术': namespace + ':technique',
                    '转会': namespace + ':transfer',
                    '所属球队': namespace + ':team',
                    '结果': namespace + ':result',
                    '比赛': namespace + ':match',
                    '上演': namespace + ':play',
                    '首次进球': namespace + ':firstGoal',
                    '首次出场': namespace + ':debut',
                    '出场': namespace + ':appear',
                    '球队': namespace + ':team',
                    '执教': namespace + ':coachExp',
                    '开始时间': namespace + ':startTime',
                    '结束时间': namespace + ':endTime',
                    '时候': namespace + ':time',
                    '在': namespace + ':in',
                    '称呼': namespace + ':called',
                    '荣誉': namespace + ':honor',
                    '技术特点': namespace + ':techCharacter',
                    '擅长位置': namespace + ':skilfulPosition',
                    '擅长技术': namespace + ':skilfulTech',
                    '执教情况': namespace + ':coachResult',
                    '写': namespace + ':write',
                    '从事': namespace + ':do',
                    '膝盖十字韧带': namespace + ':body',
                    '撕裂': namespace + ':tear',
                    '获得': namespace + ':obtain',
                    '表现': namespace + ':performance',
                    '体重': namespace + ':weight',
                    '队长': namespace + ':caption',
                    '首秀': namespace + ':debut',
                    '加盟': namespace + ':transfer',
                    '首球': namespace + ':firstGoal',
                    '妻子': namespace + ':wife',
                    '老婆': namespace + ':wife',
                    '儿子': namespace + ':son',
                    }
    try:
        return mapping_dict[content]
    except KeyError:
        return 'aiball:unknown'


def translation(content):
    mapping_dict = {'日本队': '日本',
                    '大卫路易斯': '大卫·路易斯',
                    '迭戈科斯塔': '迭戈·科斯塔',
                    '克林斯曼': '尤尔根·克林斯曼',
                    }
    mapping_dict.update(transfer.all_transfer)
    try:
        return mapping_dict[content]
    except KeyError:
        return content


def aiballclass(content):
    mapping_list = {'青训': namespace + ':YouthSetup',
                    '租借': namespace + ':RentExp',
                    '起矛盾': namespace + ':NegativeEvent',
                    '处子球': namespace + ':FirstGoal',
                    '有矛盾': namespace + ':NegativeEvent'}
    try:
        return mapping_list[content]
    except KeyError:
        return '"{}"'.format(content)


def get_content_verb(goals):
    return [(goal, relation(goal)) for goal in goals]


class OneTermForTpl:
    def __init__(self, words):
        self.words = words
        self.mapping_dict = {'日本队': '日本',
                             '大卫路易斯': '大卫·路易斯',
                             '迭戈科斯塔': '迭戈·科斯塔',
                             }
        self.mapping_dict.update(transfer.all_transfer)
        self.mapping_dict.update(transfer.persons_worldcup1990)
        self.mapping_dict.update({
                                  '德国': '西德',
                                  '拜仁': '拜仁慕尼黑',
                                  '国米': '国际米兰',
                                  '云达不莱梅': '云达不来梅',
                                  '尤尔根克林斯曼': '尤尔根·克林斯曼',
                                  '尤尔根': '尤尔根·克林斯曼',
                                  '克林斯曼': '尤尔根·克林斯曼',
                                  '卡尔海因茨里德尔': '卡尔-海因茨·里德尔',
                                  '卡尔': '卡尔-海因茨·里德尔',
                                  '海因茨': '卡尔-海因茨·里德尔',
                                  '里德尔': '卡尔-海因茨·里德尔',
                                  '安德烈亚斯科普克': '安德烈亚斯·科普克',
                                  '安德烈亚斯': '安德烈亚斯·科普克',
                                  '科普克': '安德烈亚斯·科普克',
                                  '德斯沃克': '安德烈亚斯·科普克',
                                  '德斯': '德斯·沃克',
                                  '沃克': '德斯·沃克',
                                  '史蒂夫霍吉': '史蒂夫·霍吉',
                                  '史蒂夫': '史蒂夫·霍吉',
                                  '霍吉': '史蒂夫·霍吉',
                                  '加斯科因': '保罗·加斯科因',
                                  '巴尔斯基': '皮埃尔·利特巴尔斯基',
                                  '巡游者': '女王公园巡游者',
                                  '门将': '守门员',

                                  })

    def synonym(self, content):
        return self.mapping_dict[content]

    def get_self(self):
        content = self.words
        if content in self.mapping_dict:
            content = self.synonym(content)
        verb = relation(content)
        return content, verb

    def get_content(self):
        content = self.words
        if content in self.mapping_dict:
            content = self.synonym(content)
        return content


class OneTermForSyntac:
    def __init__(self, idx, words, arcs):
        self.idx = idx
        self.words = words
        self.arcs = arcs
        self.synonym = translation
        self.before_func = relation_before
        self.verb_func = relation_verb

    def get_self(self):
        content = self.words[self.idx]
        content = self.synonym(content)
        verb_before = self.before_func(content)
        verb = self.verb_func(content)

        return content, verb_before, verb

    def get_content(self):
        content = self.words[self.idx]
        content = self.synonym(content)
        return content

    def get_children(self):
        arcs_head = [arc.head - 1 for arc in self.arcs]
        tree_info = defaultdict(list)
        for i in range(len(arcs_head)):
            head = arcs_head[i]
            tree_info[head].append(i)
        try:
            wi = self.words.index(self.idx)
            return tree_info[wi]
        except ValueError:
            return None

    def get_vob(self):
        arc_relations = [arc.relation for arc in self.arcs]
        children = self.get_children()
        for child in children:
            if arc_relations[child] == 'VOB':
                return self.words[child]

    def get_sbv(self):
        arc_relations = [arc.relation for arc in self.arcs]
        children = self.get_children()
        for child in children:
            if arc_relations[child] == 'SBV':
                return self.words[child]


class OneTerm:
    def __init__(self, term, words, arcs):
        self.term = term
        self.words = words
        self.arcs = arcs
        self.mapping_dict = {'日本队': '日本',
                             '大卫路易斯': '大卫·路易斯',
                             '迭戈科斯塔': '迭戈·科斯塔',
                             '克林斯曼': '尤尔根·克林斯曼',
                             }
        self.mapping_dict.update(transfer.all_transfer)
        # self.mapping_dict.update({'阿根廷队': '阿根廷国家队'})

    def synonym(self, content):
        return self.mapping_dict[content]

    def get_self(self):
        content = self.words[self.term]
        if content in self.mapping_dict:
            content = self.synonym(content)
        # try:
        #     verb = relation(content)
        # except KeyError:
        #     verb = 'aiball:unknown'
        verb = relation(content)
        return content, verb

    def get_content(self):
        content = self.words[self.term]
        if content in self.mapping_dict:
            content = self.synonym(content)
        return content

    def get_children(self):
        arcs_head = [arc.head - 1 for arc in self.arcs]
        tree_info = defaultdict(list)
        for i in range(len(arcs_head)):
            head = arcs_head[i]
            tree_info[head].append(i)
        try:
            wi = self.words.index(self.term)
            return tree_info[wi]
        except ValueError:
            return None

    def get_vob(self):
        arc_relations = [arc.relation for arc in self.arcs]
        children = self.get_children()
        for child in children:
            if arc_relations[child] == 'VOB':
                return self.words[child]

    def get_sbv(self):
        arc_relations = [arc.relation for arc in self.arcs]
        children = self.get_children()
        for child in children:
            if arc_relations[child] == 'SBV':
                return self.words[child]


class TwoTerms:
    def __init__(self, term, words, arcs):
        self.term1 = term[0]
        self.term2 = term[1]
        self.words = words
        self.arcs = arcs

    def sbv(self):
        arc_heads = [arc.head for arc in self.arcs]
        arc_relations = [arc.relation for arc in self.arcs]
        arc_length = len(arc_relations)
        si = -1
        while True:
            try:
                si = arc_relations.index('SBV') + si + 1
                if self.words[si] == self.term1 and \
                   self.words[arc_heads[si] - 1] == self.term2:
                    return True
                if si + 1 < arc_length:
                    arc_relations = arc_relations[si + 1:]
                else:
                    return False
            except ValueError:
                return False

    def vob(self):
        arc_heads = [arc.head for arc in self.arcs]
        arc_relations = [arc.relation for arc in self.arcs]
        arc_length = len(arc_relations)
        si = -1
        while True:
            try:
                si = arc_relations.index('VOB') + si + 1
                if self.words[si] == self.term2 and \
                   self.words[arc_heads[si] - 1] == self.term1:
                    return True
                if si + 1 < arc_length:
                    arc_relations = arc_relations[si + 1:]
                else:
                    return False
            except ValueError:
                return False
