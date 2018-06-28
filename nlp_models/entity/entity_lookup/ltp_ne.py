"""
@Project   : CubeGirl
@Module    : ltp_ne.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/4/18 3:45 PM
@Desc      : 
"""
import pickle
import os
from .ltp_basic import ltp_basic
from .re_ne import extract_patterns
# from .patterns_extract import team_patterns

file_dir = os.path.dirname(os.path.abspath(__file__))


def get_team_patters():
    file_useful = os.path.join(file_dir, 'data/teams_useful.pkl')
    with open(file_useful, 'rb') as f:
        teams = pickle.load(f)
    return teams


def get_person_patters():
    file_useful = os.path.join(file_dir, 'data/persons_useful.pkl')
    with open(file_useful, 'rb') as f:
        persons = pickle.load(f)
    return persons


class EntityRole:

    # stop_words = ('的', '中', '了', '已经', '所属', '也', '还', '名',
    #               '个', '次', '过', '啊', '呀', '呢', '于')
    stop_words = set()
    lb = ltp_basic

    def __init__(self, sample):
        words = self.lb.segmentor.segment(sample)  # 分词
        words = [word for word in words if word not in self.stop_words]
        postags = list(self.lb.postagger.postag(words))  # 词性标注
        self.words = words
        self.postags = postags
        self.arcs = None
        self.netags = None
        self.roles = None

    def entity(self):
        netags = self.lb.recognizer.recognize(self.words, self.postags)
        # 命名实体识别
        self.netags = list(netags)

    def role(self):
        self.arcs = self.lb.parser.parse(self.words, self.postags)
        roles = self.lb.labeller.label(self.words,
                                       self.postags,
                                       self.arcs)  # 语义角色标注
        self.roles = list(roles)


def ne_extract(sentence):
    sen_entity = EntityRole(sentence)
    sen_entity.entity()

    persons = set()
    teams = set()
    times = list()
    bie = list()

    for i, word in enumerate(sen_entity.words):
        if sen_entity.netags[i] == 'S-Nh':
            persons.add(word)
        elif sen_entity.netags[i] == 'S-Ni':
            teams.add(word)
        elif sen_entity.postags[i] == 'nt':
            times.append((i, word))
        elif sen_entity.netags[i].startswith('B'):
            bie.clear()
            bie.append(word)
        elif sen_entity.netags[i].startswith('I'):
            bie.append(word)
        elif sen_entity.netags[i] == 'E-Nh':
            bie.append(word)
            persons.add(''.join(bie))
        elif sen_entity.netags[i] == 'E-Ni':
            bie.append(word)
            teams.add(''.join(bie))

    last_index = -2
    last_time = ''
    time_combine = set()

    # BIO system
    label = list()
    for index, time in times:
        if index-last_index == 1:
            label.append('I')
        else:
            label.append('B')
        last_index = index
    times = [time for _, time in times]
    for index, time in enumerate(times):
        if label[index] == 'B':
            time_string = time
        else:
            time_string = last_time + time
        last_time = time_string

        if index + 1 == len(times):
            time_combine.add(time_string)
        elif label[index+1] == 'B':
            time_combine.add(time_string)

    # for index, time in times:
    #     if index-last_index == 1:
    #         time_string = last_time + time
    #     else:
    #         time_string = time
    #
    #     time_combine.add(time_string)
    #
    #     last_index = index
    #     last_time = time_string

    entities = {'person': list(persons), 'team': list(teams),
                'time': list(time_combine)}

    return entities


def tp_supplement(st):
    entities = ne_extract(st)

    team_patterns = get_team_patters()
    team_dict = extract_patterns(team_patterns, st)
    entities['team'].extend(team_dict[st])
    entities['team'] = list(set(entities['team']))

    person_patterns = get_person_patters()
    person_dict = extract_patterns(person_patterns, st)
    entities['person'].extend(person_dict[st])
    entities['person'] = list(set(entities['person']))

    return entities


def test():
    sentences = [
        '国家队方面，27岁的梅西以队长身份带领阿根廷队在2014年世界杯过关斩将，'
        '连续四场成为全场最佳球员，阿根廷队决赛战至加时仅败于德国队，屈居亚军。'
        '梅西赛后获颁世界杯金球奖。',

        '2018年3月26日，梅西在欧洲冠军联赛中有上佳表现',

        '利昂内尔·安德烈斯·“莱奥”·梅西·库西提尼'
        '（西班牙语：Lionel Andrés "Leo" Messi Cuccittini，'
        '( 西班牙语发音： [ljoˈnel anˈdɾes ˈmesi] 读音 ，1987年6月24日－）（又称“美斯”），'
        '生于阿根廷圣菲省罗萨里奥，拥有加泰罗尼亚及意大利血统[3]，当今世界着名顶尖阿根廷职业足球员，'
        '现时为西班牙甲组足球联赛豪门巴塞罗那的副队长，场上主要担任翼锋，'
        '也可以担任前锋并回撤为进攻中场，这也是梅西和其他前锋不同的地方，梅西擅长用左脚，'
        '尤其以极为细腻的盘球技术、非凡的控球能力、丰富的创造力、难以置信的进球及助攻频率而举世闻名。',

        '梅西年少时已加入巴塞罗那队青训营拉玛西亚，出道至今职业生涯一直效力巴塞罗那，'
        '并随队横扫多项赛事冠军，包括四次欧洲联赛冠军盃冠军和八届西班牙甲组联赛冠军，'
        '获得辉煌的球会成就，同时打破诸多纪录。美斯被媒体、名宿和球迷广泛认定为世界球坛史上最佳球员之一[4][5][6][7]，'
        '美斯亦被球王马勒当拿视为“完美接班人”[8]。',

        '2009年，梅西以主力射手身份协助巴塞罗那连获西甲联赛、西班牙国王盃、'
        '欧洲联赛冠军盃三项冠军，成为西班牙足球史及队史上第一个三冠王球队。'
        '接着参加下半年的三项专属于冠军之间的赛事，再度荣获西班牙超级盃、欧洲超级盃、'
        '以及世界冠军球会盃三大锦标，协助巴塞隆拿完成世界足坛绝无仅有的一次「六冠王」伟业。'
        '2011年，梅西协助巴塞隆拿再夺得五项冠军，成为该年的「五冠王」。'
        '2010年、2011年、2012年，梅西连续取得首三届国际足协金球奖，总计梅西连续四年获此殊荣。'
        '2015年，梅西协助巴塞隆拿再夺得五项冠军，成为该年的「五冠王」，再获国际足协金球奖，'
        '成为历史上首位夺下五届金球奖和世界足球先生（不论合併前后）的球员[6][9][10]。',

        '2011年，梅西以24岁之龄成为巴塞隆拿足球会历史上，在正式比赛中入球数最多的球员[7][11]。'
        '至今，梅西已在巴塞隆纳所有比赛攻入558球[12]，保有欧洲联赛为单一球会入球的纪录。'
        '他亦是西甲兼欧洲单一联赛历史上入球最多的球员[13]，而且西甲助攻量也是史上之最。梅'
        '西目前为巴塞隆纳和阿根廷上场的694场比赛中，不但进了558球，连助攻次数也有206次，'
        '很少有球员能达到这个助攻数量，证明梅西是大师级人物。',

        '2017年夏天，巴黎圣日耳曼豪掷4亿欧元将内马尔和姆巴佩带到球队，两人与卡瓦尼组成了CNM组合。',


    ]

    for st in sentences:
        # print(ne_extract(st))
        print(tp_supplement(st))

    # print(persons)
    # print(teams)
    # print(times)
    #
    # print(time_combine)
    #
    # for i, word in enumerate(sen_entity.words):
    #     if sen_entity.netags[i] != 'O':  # 是欧，不是零
    #         print(sen_entity.netags[i], word)
    #     if sen_entity.postags[i] == 'nt':
    #         print('temporal noun', word)

    # sen_entity.role()
    #
    # for role in sen_entity.roles:
    #     for arg in role.arguments:
    #         if arg.name == 'TMP':
    #             print(arg.name,
    #                   sen_entity.words[role.index],
    #                   sen_entity.words[arg.range.start],
    #                   sen_entity.words[arg.range.end])

    # for role in sen_entity.roles:
    #     print(sen_entity.words[role.index], "/".join(
    #     ["%s:(%d, %d)" % (arg.name, arg.range.start, arg.range.end) for arg
    #      in role.arguments]))
    #
    # for i, word in enumerate(sen_entity.words):
    #     print(i, word)
