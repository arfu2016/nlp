"""
@Project   : CubeGirl
@Module    : single_question.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/2/18 2:52 PM
@Desc      : Single question and methods of calling sparql
"""
from .depy_dict_question import SparqlQuestion
from .tpl4_sparql import registered_classes
from .tpl5_syntac import syntac_dict

# todo: logging，对异常的处理
# todo: settings, depy_settings.py
# todo: 类生产工厂，或者从文本到函数或类的闭包
# todo: 实体抽取，whehter_container_extract in SparqlTpl in depy_words_tpl.py
# todo: argparse
# todo: 对外部实体抽取的调用，对追问函数的调用或者对追问函数所返回的结果的利用
# todo: 对数据库id查询接口的调用
# todo: 讲两类模板的接口更加统一，只保留意图识别的不同
# todo: 重构，删掉不必要的文件，组合文件，改文件名
# todo: 对上下文接口的调用
# todo: More Accurate Question Answering on Freebase

categories_sequence_tpl = registered_classes.values()    # 引入模板类
categories_syntac_tpl = syntac_dict.values()


def _search_tpl_and_processor(categories, question_in):
    for category in categories:
        tpl_instance = category(question_in)
        tpl_instance.interpret()
        if tpl_instance.rule_of_tpl:
            return {'name': tpl_instance.template_name,
                    'function': tpl_instance.spq_func}
    return {'name': '', 'function': None}


def _search_syntac_tpl_processor(categories, question_in):
    category_name_score = list()
    for category in categories:
        tpl_instance = category(question_in)
        tpl_instance.select_tpl()
        category_name_score.append({'instance': tpl_instance,
                                    'score': tpl_instance.score})
    score = 0
    template_index = 0
    for index, name_score in enumerate(category_name_score):
        if name_score['score'] > score:
            score = name_score['score']
            template_index = index

    if score > 0:
        tpl_instance = category_name_score[template_index]['instance']
        tpl_instance.rule_of_tpl = True
        tpl_instance.select_processor()
        return {'name': tpl_instance.template_name,
                'function': tpl_instance.spq_func}
    return {'name': '', 'function': None}


def process_single(question, item_ids=None):
    if item_ids is None:
        item_ids = dict()
    question_in = SparqlQuestion(question, item_ids)
    question_tuple = (question, question_in)
    # 问题类的构建

    try:
        name_tpl = _search_tpl_and_processor(categories_sequence_tpl,
                                             question_in)

        if len(name_tpl['name']) > 0:

            question_in.tpl = name_tpl['name']
            question_in.sparql_func = name_tpl['function']
            question_in.register = registered_classes

            question_in.answer_question()

        else:
            name_tpl = _search_syntac_tpl_processor(categories_syntac_tpl,
                                                    question_in)

            if len(name_tpl['name']) > 0:

                question_in.tpl = name_tpl['name']
                question_in.sparql_func = name_tpl['function']
                question_in.register = syntac_dict

                question_in.answer_question()

            else:

                question_in.answer = None

        # print()
        # prefix_hint = 'process_single() in single_question.py:'
        # print(prefix_hint, question, question_in.tpl)

    except IndexError:
        question_in.answer = None
    except Exception as e:
        question_in.answer = None
        print('Unexcepted exception in single_question.py '
              'in knowledge_graph:', e)

    return question_tuple


def process(questions):
    result = [process_single(question) for question in questions]
    result = dict(result)
    return result
