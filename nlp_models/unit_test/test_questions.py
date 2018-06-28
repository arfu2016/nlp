"""
@Project   : CubeGirl
@Module    : test_questions.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/4/18 5:16 PM
@Desc      : file in branch mlp_model_new in logic/text_table
给出了句法模板测试的几种情况
"""

from .class2_sbv_obv import SbvVobTree, SbvAdvPobTree, Convert1
from .class2_sbv_obv import SbvHedVobTree, AdvPobVobCooTree, Convert3
from .class2_sbv_obv import SbvAttVobHed, Convert2
from .class1_att_any import AttAttHedTree
from .class2_sbv_obv import SbvAttVobHed2, Convert4
from .depy_generation import get_code
from .class1_att_any import quesions_by_categories, star_dog_print


def test_template1():
    """主谓宾，请教主语的属性；主谓宾，主语的属性; 哪些专业人士赞扬过梅西"""
    questions = ['哪些专业人士赞扬过梅西']

    categories = [SbvVobTree, SbvAdvPobTree, Convert1]
    # 目前，每个类都要加载一次分词模型
    language = "sparql"

    rest_dict, none_dict = quesions_by_categories(categories, questions)
    # print('rest_dict:', rest_dict)

    print('\n')
    print('The queries not converted:', none_dict.keys(), '\n')

    for ques, true_expr in rest_dict.items():
        expr = true_expr[1]
        target, query = get_code(expr, language)
        print('The head of graph querying "{}" is:'.format(ques), target)
        print('The sparql statement of graph querying "{}" is:'.format(ques),
              query)


def test_template2():
    """主谓宾，谓语的属性; 梅西在阿根廷队有进球，谓语的进球数; 梅西怎么认识皮克的"""
    questions = ['梅西怎么认识皮克的', '梅西怎么认识皮克的呢', '梅西如何认识皮克的']

    # SbvVobHed
    categories = [SbvHedVobTree, AdvPobVobCooTree, Convert3]
    language = "sparql"

    rest_dict, none_dict = quesions_by_categories(categories, questions)
    # print('rest_dict:', rest_dict)

    print('\n')
    print('The queries not converted:', none_dict.keys(), '\n')

    for ques, true_expr in rest_dict.items():
        expr = true_expr[1]
        target, query = get_code(expr, language)
        print('The head of graph querying "{}" is:'.format(ques), target)
        print('The sparql statement of graph querying "{}" is:'.format(ques),
              query)

    from SPARQLWrapper import SPARQLWrapper, JSON

    sparql = SPARQLWrapper("http://192.168.10.2:5820/test1/query")
    sparql.setCredentials(user="admin", passwd="admin")
    questions = ['梅西怎么认识皮克的']
    for question in questions:
        star_dog_print(question, rest_dict, language, sparql, JSON)


def test_template3():
    """主谓定宾，谓语的属性; 梅西在世界杯决赛怎么输的"""
    questions = ['梅西参加世界杯决赛的情况',
                 '梅西在世界杯决赛怎么输的']
    categories = [SbvAttVobHed, Convert2]
    # 目前，每个类都要加载一次分词模型
    language = "sparql"

    rest_dict, none_dict = quesions_by_categories(categories, questions)
    # print('rest_dict:', rest_dict)

    print('\n')
    print('The queries not converted:', none_dict.keys(), '\n')

    for ques, true_expr in rest_dict.items():
        expr = true_expr[1]
        target, query = get_code(expr, language)
        print('The head of graph querying "{}" is:'.format(ques), target)
        print('The sparql statement of graph querying "{}" is:'.format(ques),
              query)


def test_template4():
    """定语+定语+名词"""
    questions = ['梅西的帽子戏法的用时',
                 '梅西的女友的名字']
    categories = [AttAttHedTree]
    # 目前，每个类都要加载一次分词模型
    language = "sparql"

    rest_dict, none_dict = quesions_by_categories(categories, questions)
    # print('rest_dict:', rest_dict)

    print('\n')
    print('The queries not converted:', none_dict.keys(), '\n')

    for ques, true_expr in rest_dict.items():
        expr = true_expr[1]
        target, query = get_code(expr, language)
        print('The head of graph querying "{}" is:'.format(ques), target)
        print('The sparql statement of graph querying "{}" is:'.format(ques),
              query)

    from SPARQLWrapper import SPARQLWrapper, JSON

    sparql = SPARQLWrapper("http://192.168.10.2:5820/test1/query")
    sparql.setCredentials(user="admin", passwd="admin")
    questions = ['梅西的女友的名字']
    for question in questions:
        star_dog_print(question, rest_dict, language, sparql, JSON)


def test_template5():
    """主状谓宾，谓语的属性；梅西首次在国家队夺冠是在哪"""
    questions = ['梅西首次在国家队夺冠是在哪']
    # '梅西参加世界杯决赛的情况'

    # SbvAttVobHed
    categories = [SbvAttVobHed2, Convert4]
    # 目前，每个类都要加载一次分词模型
    language = "sparql"

    rest_dict, none_dict = quesions_by_categories(categories, questions)
    # print('rest_dict:', rest_dict)

    print('\n')
    print('The queries not converted:', none_dict.keys(), '\n')

    for ques, true_expr in rest_dict.items():
        expr = true_expr[1]
        target, query = get_code(expr, language)
        print('The head of graph querying "{}" is:'.format(ques), target)
        print('The sparql statement of graph querying "{}" is:'.format(ques),
              query)
