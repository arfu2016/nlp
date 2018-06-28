"""
@Project   : CubeGirl
@Module    : question_answer.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/17/18 1:50 PM
@Desc      : 自然语言提问，在图数据库中查询后，生成问句给出回答
"""
from .depy_dict_question import (SimpleQuestion, MultipleQuestion)
from .depy_question_template import (routine_process,
                                     questions_by_categories, tpl_process)
from .sentence_parse_tree import sen
from .depy_category_dict import ca_dict
from .depy_dict_question import specific_process
from .depy_tools import (clean_templates, clean_sentence)


def process2(questions, item_ids):
    """
    接受问题，给出答案类的字典
    :param questions: List, list of question strings
    :param item_ids:
    :return: Dict, key is the question string, value is the question instance
    """
    categories20 = ca_dict.category_dict[20]
    categories10 = ca_dict.category_dict[10]
    categories11 = ca_dict.category_dict[11]
    categories0, categories1 = \
        ca_dict.category_dict[0], ca_dict.category_dict[1]
    # 引入模板类

    questions = clean_templates(questions)
    # 去掉标点符号后的问题

    question_ids = zip(questions, item_ids)

    # question_ins = [SimpleQuestion(question) for question in questions]

    question_ins = [SimpleQuestion(question, qid)
                    for question, qid in question_ids]
    question_dict = {question: question_in for question, question_in
                     in zip(questions, question_ins)}
    # 构建问题类与问题字典

    rest_dict00, none_dict00 = questions_by_categories(categories20,
                                                       question_ins)
    tpl_process(rest_dict00, question_dict)

    questions212 = none_dict00.keys()
    if len(questions212) > 0:
        question_ins212 = [question_in for question, question_in
                           in question_dict.items()
                           if question in questions212]

        rest_dict0, none_dict0 = questions_by_categories(categories10,
                                                         question_ins212)
        complex_questions = list(rest_dict0.keys())
        convert_qs = [rest_dict0[question][1] for question in
                      complex_questions]
        convert_dict = {question: convert for question, convert
                        in zip(complex_questions, convert_qs)}
        # 实现问句的转换
        for original_question in convert_dict.keys():
            the_question = MultipleQuestion(original_question)
            the_question.run_singles(convert_dict, categories0, categories1)
            # run_singles()既做自然语言转换和查询，也做结果的修正
            question_dict[original_question].result = the_question.result
            # 对转换后的问题进行处理
    else:
        none_dict0 = none_dict00

    # 以上代码块-处理需要进行问句转换的问题：MultipleQuestion类的子问题是一般问题，
    # 如果子问题更加复杂，可以设计新的类

    none_dict1 = specific_process(none_dict0, question_dict, categories11)
    # 处理需要调整、组合查询结果的问题：用对应着单一问题类(特定问题类)
    # 的模板类来处理（查询问题是一般问题，查询在该步完成），
    # 建立新的问题类之后，只做结果的修正

    questions21 = none_dict1.keys()
    many_questions_ins21 = [question_in for question, question_in
                            in question_dict.items()
                            if question in questions21]
    routine_process(questions21, many_questions_ins21, categories0,
                    categories1)
    # 处理一般问题

    for question, question_in in question_dict.items():
        question_in.parse()
        question_in.answer_question()
        print('process() in question_answer.py:', question, question_in.tpl)
        print()
    # 产生回答

    return question_dict


def process(questions):
    item_ids = [dict()] * len(questions)
    return process2(questions, item_ids)


def test():
    questions = ['马拉多纳一球成名的对手', '马拉多纳一球成名的时间',
                 '马拉多纳一球成名的所属球队', '马拉多纳一球成名的结果',
                 '莱因克尔帽子戏法的比赛', '莱因克尔帽子戏法的结果',
                 '莱因克尔的帽子戏法的比赛',
                 '莱因克尔在什么比赛中上演帽子戏法',
                 '马拉多纳一球成名',
                 '马拉多纳怎么一球成名的',
                 '马拉多纳是怎么一球成名的',

                 '巴雷西如何评价马拉多纳的', '巴雷西如何评价马拉多纳的啊',
                 '巴雷西是如何评价马拉多纳的', '巴雷西是如何评价马拉多纳的呢',
                 '巴雷西评价马拉多纳的技术',
                 '巴雷西如何评价马拉多纳的技术',

                 '鲁尼首次在国家队出场的时间',
                 '鲁尼第一次在国家队进球的时间',

                 '非常复杂的一个测试，给出适当的回答',
                 '找不到模板',

                 '马拉多纳在国家队期间有什么高光时刻吗',
                 '马拉多纳的荣誉',

                 '李白写过哪些饮酒诗',
                 '贝勒从事过哪些职业',
                 '本田圭佑第一次在巴西队出场的时间',

                 '吉尼斯世界纪录的最远进球有多少米远',
                 '哪些球员撕裂过膝盖十字韧带',
                 '哪些球员获得过世界杯冠军',

                 # short question且知识图谱中有数据，多个模板覆盖
                 '马拉多纳的首秀',  # 首秀
                 # 定中
                 # 哈里马奎尔, 乔戈麦斯
                 # 去掉的
                 '马拉多纳第一次出场',
                 # 主状谓
                 # 首次, 马拉多纳的第一次出场
                 '马拉多纳国家队首秀',
                 # 主状谓
                 # 马拉多纳的国家队首秀, 阿根廷队
                 '马拉多纳国家队第一次出场',
                 # 主状状谓
                 # 首次, 阿根廷队
                 '马拉多纳第一次国家队出场',
                 # 主状状谓
                 # 首次
                 '本田圭佑的首球',  # 首球
                 # 原口元气, 冈崎慎司, 纳伊夫哈扎齐
                 # 去掉的
                 '本田圭佑第一次进球',
                 # 第一个
                 '本田圭佑国家队首球',
                 # 日本队
                 '本田圭佑国家队第一次进球',
                 # 第一个, 日本队
                 '本田圭佑第一次国家队进球',
                 # 第一个
                 '阿森纳青训培养过哪些球员',  # 青训
                 # 沙尔克, 河床
                 # 阿森纳的青训, 培养了, 培养, 培养出, 培养出了
                 '穆里尼奥和谁起过矛盾',  # 负面消息
                 # 瓜迪奥拉, 贝克汉姆
                 # 有矛盾, 起矛盾，起了矛盾
                 '马拉多纳从哪里转会巴塞罗那',  # 转会
                 # 正确的句法分析
                 # 那不勒斯
                 # 什么俱乐部, 啥地方, 哪儿
                 # [(4, 'SBV'), (4, 'ADV'), (2, 'POB'), (0, 'HED'), (4, 'VOB')]
                 '马拉多纳从哪里转会博卡青年',
                 # 博卡青年 ns
                 # 什么俱乐部, 啥地方 not work
                 # [(5, 'SBV'), (5, 'ADV'), (2, 'POB'), (5, 'ATT'), (0, 'HED')]
                 '马拉多纳从博卡青年转会到哪里',  # 正确的句法分析
                 # 巴塞罗那, 哪儿, 什么俱乐部
                 # [(4, 'SBV'), (4, 'ADV'), (2, 'POB'), (0, 'HED'), (4, 'CMP'),
                 # (5, 'POB')]
                 '马拉多纳从那不勒斯转会到哪里',  # 那不勒斯 ns
                 # [(5, 'SBV'), (5, 'ADV'), (2, 'POB'), (2, 'POB'), (0, 'HED'),
                 # (5, 'POB')]
                 '马拉多纳转会巴塞罗那的时间',
                 # 博卡青年，那不勒斯
                 # 去掉的
                 '马拉多纳从博卡青年转会巴塞罗那的时间',
                 # 去掉的
                 '马拉多纳加盟过哪些俱乐部',
                 '沃特福德租借过哪些球星',  # 租借
                 '哪家俱乐部既培养了阿根廷国脚，也培养了西班牙国脚',  # 复杂
                 '鲁尼俱乐部的队友入选英格兰国家队的有哪些',
                 '哪些球员在面对意大利的时候收获处子球',  # 首球
                 # 韩国, 英格兰
                 # 去掉的
                 # 面对意大利时
                 '哪些人既和大卫路易斯有矛盾，也和迭戈科斯塔有矛盾',  # 负面消息
                 # 迭戈科斯塔 and 德布劳内
                 # 又

                 # test question I
                 '马拉多纳首秀',
                 '哈里马奎尔的首秀',
                 '哈里马奎尔首秀',
                 '乔戈麦斯的首秀',
                 '乔戈麦斯首秀',
                 '哈里马奎尔第一次出场',
                 '乔戈麦斯第一次出场',
                 '哈里马奎尔国家队首秀',
                 '乔戈麦斯国家队首秀',
                 '哈里马奎尔国家队第一次出场',
                 '乔戈麦斯国家队第一次出场',
                 '哈里马奎尔第一次国家队出场',
                 '乔戈麦斯第一次国家队出场',
                 '本田圭佑首球',
                 '原口元气的首球',
                 '纳伊夫哈扎齐的首球',
                 '原口元气首球',
                 '纳伊夫哈扎齐首球',
                 '原口元气第一次进球',
                 '纳伊夫哈扎齐第一次进球',
                 '原口元气国家队首球',
                 '纳伊夫哈扎齐国家队首球',
                 '原口元气国家队第一次进球',
                 '纳伊夫哈扎齐国家队第一次进球',
                 '原口元气第一次国家队进球',
                 '纳伊夫哈扎齐第一次国家队进球',
                 '沙尔克青训培养过哪些球员',
                 '河床青训培养过哪些球员',
                 '巴塞罗那青训培养过哪些球员',
                 '瓜迪奥拉和谁起过矛盾',
                 '贝克汉姆和谁起过矛盾',
                 '保利尼奥从哪里转会广州恒大',
                 '大卫路易斯从哪里转会切尔西',
                 '内马尔从哪里转会巴塞罗那',
                 '大卫路易斯从切尔西转会到哪里',
                 '保利尼奥加盟过哪些俱乐部',
                 '大卫路易斯加盟过哪些俱乐部',
                 '内马尔加盟过哪些俱乐部',
                 '罗马租借过哪些球星',
                 '利物浦租借过哪些球星',
                 '尤文图斯租借过哪些球星',
                 '哪家俱乐部既培养了英格兰国脚，也培养了西班牙国脚',
                 '哪家俱乐部既培养了德国国脚，也培养了英格兰国脚',
                 '哪家俱乐部既培养了法国国脚，也培养了西班牙国脚',
                 '梅西俱乐部的队友入选西班牙国家队的有哪些',
                 '大卫路易斯俱乐部的队友入选英格兰国家队的有哪些',
                 '哪些球员在面对韩国的时候收获处子球',
                 '哪些球员在面对英格兰的时候收获处子球',

                 # fragile question, 知识图谱中缺乏某些数据

                 # complex question且知识图谱中有数据，多个模板覆盖
                 '马拉多纳第一次在国家队出场的对手',  # 首秀
                 # 哈里马奎尔, 乔戈麦斯
                 # 去掉的
                 # 在阿根廷队
                 '马拉多纳第一次在国家队出场的时间',
                 # 去掉的
                 # 在阿根廷队
                 '马拉多纳在国家队中第一次出场是什么时候',
                 # 在阿根廷队, 时间, 啥时候
                 '马拉多纳在国家队中第一次出场是哪个对手',
                 # 在阿根廷队, 什么
                 '费尔南迪尼奥在国家队中第一个进球是什么时候',  # 首球
                 # 原口元气, 冈崎慎司, 纳伊夫哈扎齐
                 # 在日本队, 时间, 啥时候
                 '本田圭佑第一次在国家队进球的时间',
                 # 去掉的
                 # 在日本队
                 '本田圭佑第一次在国家队进球的对手',
                 # 去掉的
                 # 在日本队

                 # good question且知识图谱中有数据
                 '哈里马奎尔第一次代表国家队出场在什么时候',
                 # [(5, 'ATT'), (3, 'ATT'), (5, 'ATT'), (5, 'ATT'), (6, 'SBV'),
                 # (0, 'HED'), (6, 'CMP'), (9, 'ATT'), (7, 'POB')]
                 '哈里马奎尔第一次代表英格兰队出场在什么时候',
                 # [(6, 'SBV'), (3, 'ATT'), (6, 'ADV'), (5, 'ATT'), (6, 'SBV'),
                 # (0, 'HED'), (6, 'CMP'), (9, 'ATT'), (7, 'POB')]
                 '哈里马奎尔第一次代表国家队出场是什么时候',  # 正确的句法分析
                 # [(5, 'ATT'), (3, 'ATT'), (5, 'ATT'), (5, 'ATT'), (6, 'SBV'), 
                 # (7, 'SBV'), (0, 'HED'), (9, 'ATT'), (7, 'VOB')]
                 '马拉多纳执教竞技队的开始时间',  # 其他：执教，转会
                 # 正确的句法分析
                 # 阿根廷队, 结束时间
                 # [(2, 'SBV'), (5, 'ATT'), (2, 'VOB'), (2, 'RAD'), (0, 'HED')]
                 '马拉多纳执教竞技队开始时间',
                 # [(2, 'SBV'), (0, 'HED'), (2, 'VOB'), (2, 'COO')]
                 '马拉多纳执教阿根廷队的情况',
                 # [(2, 'SBV'), (5, 'ATT'), (2, 'VOB'), (2, 'RAD'), (0, 'HED')]
                 '马拉多纳执教阿根廷队情况',
                 # [(2, 'SBV'), (0, 'HED'), (4, 'ATT'), (2, 'VOB')]
                 '马拉多纳执教的情况',  # 正确的句法分析
                 # 开始时间, 结束时间
                 # [(2, 'SBV'), (4, 'ATT'), (2, 'RAD'), (0, 'HED')]
                 '马拉多纳执教情况',
                 # [(2, 'SBV'), (0, 'HED'), (2, 'VOB')]
                 '马拉多纳执教',  # 其他: 执教, 转会
                 # 主谓
                 '马拉多纳执教阿根廷队',
                 # 主谓宾
                 '马拉多纳转会',
                 '马拉多纳转会巴塞罗那',
                 '因扎吉转会',
                 '因扎吉转会尤文图斯',
                 '布拉沃转会',
                 '布拉沃转会曼城',
                 '贝尼特斯执教',
                 '贝尼特斯执教切尔西',

                 # good question但数据尚未加好


                 # good question但数据出错


                 # good question但知识图谱中没有数据
                 # 两个词没问题，三个词就可能出错（能想办法纠正）
                 # 四个词及以上就比较难处理
                 '梅西的身高',
                 # 女友, 体重, 球队
                 '巴西队的队长',
                 # 荣誉
                 '鲁尼一球成名',
                 # 转会
                 '鲁尼帽子戏法',
                 # 首秀
                 '因扎吉和库伊特中，几个球员获得过世界杯冠军',

                 '哪些球员参加过2004-05赛季欧冠决赛',
                 '巴雷西怎么评价马拉多纳',
                 '2011年11月12日，在英格兰1: 0战胜西班牙的友谊赛中，巴里是否首发出场了',

                 # other question且知识图谱中有数据
                 '马拉多纳转会的情况',
                 '马拉多纳转会的时间',
                 '因扎吉从尤文图斯转会到哪里',
                 '马拉多纳从啥地方转会巴塞罗那呢',
                 '马拉多纳转会到巴塞罗那的时间',
                 '马拉多纳执教竞技队的结束时间',
                 '马拉多纳第一次在国家队出场的球队',
                 '马拉多纳第一次代表国家队出场在什么时候',
                 '马拉多纳技术特点的擅长位置',
                 '马拉多纳技术特点的擅长技术',
                 '马拉多纳从巴塞罗那转会到哪里',
                 '马拉多纳从博卡青年转会到什么地方',
                 '马拉多纳从博卡青年转会到什么俱乐部',
                 '莱因克尔首次在巴塞罗那进球的比赛',
                 '布拉沃第一次在皇家社会进球的时间',
                 '加图索在国家队中第一个进球是什么比赛',
                 '奥比昂第一次在桑普多利亚出场的表现',
                 '莱因克尔第一次代表国家队出场在什么时候',
                 '布拉沃第一次在皇家社会进球的情况',

                 # 知识图谱技术上无法准确定位的问题
                 '哪些球星第一次代表国家队出场就进球了',  # 难，比赛无法唯一确定
                 '哪些球星第一场职业比赛的对手是曼联',  # 需要增加新的类和数据

                 # complex question且知识图谱中有数据
                 '哪些人既和PERSON0有矛盾，也和PERSON1有矛盾',  # 负面消息
                 'PERSON第一次在国家队出场的对手',  # 首秀
                 'PERSON第一次代表国家队出场在什么时候',
                 'PERSON第一次在国家队出场的时间',
                 'PERSON在国家队中第一个进球是什么时候',  # 首球
                 'PERSON第一次在日本队进球的对手',
                 'PERSON在国家队中第一个进球是什么比赛',

                 # good question且知识图谱中有数据
                 'PERSON第一次在TEAM出场的表现',  # 首秀
                 'PERSON第一次在TEAM进球的情况',  # 首球
                 'PERSON第一次在日本队进球的时间',
                 'TEAM青训培养过哪些球员',  # 青训
                 'TEAM青训培养过哪些球员',
                 'TEAM青训培养过哪些球员',
                 'PERSON和谁起过矛盾',  # 负面消息
                 'PERSON和谁起过矛盾',
                 'PERSON和谁起过矛盾',
                 'PERSON执教TEAM的开始时间',  # 其他：执教，转会
                 'PERSON执教阿根廷队的情况',
                 'PERSON执教的情况',
                 'PERSON执教阿根廷队的开始时间',
                 'PERSON执教阿根廷队的结束时间',
                 'PERSON转会TEAM的时间',
                 'PERSON从哪里转会TEAM',
                 'PERSON从TEAM转会到哪里',  # 有问题
                 'PERSON从什么俱乐部转会TEAM',
                 'PERSON从啥地方转会TEAM',

                 '德布劳内的荣誉']

    # question_answer = process(questions)
    # 给出问题，得到答案类的字典
    # 接口是process， 参数questions是包含问题的列表
    # 返回值是一个字典，key是问题，value是包含答案的类实例，实例的answer属性就是
    # 想要的字符串

    questions = [sen]
    ids = [{'PERSON': 1}]
    question_answer = process2(questions, ids)

    print('test() in question_answer.py')
    print('Question and answer after answer generation:')
    for question, question_in in question_answer.items():
        print(question, ":", question_in.answer)
        # 答案在答案类的answer属性中
