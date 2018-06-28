"""
@Project   : CubeGirl
@Module    : depy_question_template.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/22/18 11:42 AM
@Desc      : 
"""
import re

import numpy as np

from . import depy_settings as settings
from .depy_generation import get_code
from .depy_sparql_connect import connect


def star_dog_print(question, language, sparql):
    """从图数据库中得到查询结果"""
    if question.expr is not None:
        example = get_code(question.expr, language)[1]
    else:
        example = None
    question.sparql = example
    # print('star_dog_print() in depy_question_template.py')
    # print('Sparql of "{}":'.format(question.question), example)

    sparql.setQuery(example)
    results0 = sparql.query().convert()
    # 得到查询返回的json格式
    results_or = results0['results']['bindings']
    results = [list(result.values())[0]['value']
               for result in results_or]
    result_list = results
    results100 = [list(result.values())[0]
                  for result in results_or]
    if len(results) > 0:
        # 有查询结果
        temp = results100[0]
        if temp['type'] == 'uri':
            # 得到的是entity，进一步查询attribute
            result_list = []
            template = "{preamble}\n" + \
                       "SELECT DISTINCT {select} WHERE {{\n" + \
                       "{expression}\n" + \
                       "}}\n"
            for result in results:
                result = re.sub(r'http://www.aiball.com/', 'aiball:', result)
                query = template.format(preamble=settings.SPARQL_PREAMBLE,
                                        select='?x0',
                                        expression="  {} aiball:cnName ?x0.".
                                        format(result))
                sparql.setQuery(query)
                results01 = sparql.query().convert()
                results1 = results01['results']['bindings']
                results1 = [list(result.values())[0]['value']
                            for result in results1]
                result_list.extend(results1)

    question.result = result_list
    # print('Result of "{}":'.format(question.question), results0, '\n')


def filter_true(result):
    return [rs for rs in result if rs[0]]


def real_class(result):
    """
    当问句符合多个模板时，根据匹配分数选择最合适的模板
    :param result: list, list of list
    :return: list
    """
    if len(result) == 1:
        result = result[0]
        # 只有一个匹配的模板
    else:
        temp = list(zip(*result))
        # 行列互置
        temp2 = [te for te in temp[2]]
        # 取出result中表征匹配分数的那一列
        # temp2 = [te.len_edges() for te in temp[1]]
        temp_index = np.argmax(temp2)
        # 找到匹配分数最高的那一个模板
        result = result[temp_index]
    return result


def questions_by_categories(categories, questions):
    """
    问题与句法类别的交互
    :param categories: list, list of template classes
    :param questions: list, list of question instances
    :return: tuple
    """
    results = [category(questions).interpret() for category in categories]
    # 得到具体模板解析具体句子的标识、图表达式、匹配度、模板名称、匹配对应关系
    results = [list(zip(*result)) for result in results]
    # 对于每一个模板类型，得到多个list组成的元组，转为list，结果是list of list
    results = list(zip(*results))
    # 进一步完成矩阵的行列互换

    all_dict = {question.question: result for question, result
                in zip(questions, results)}
    # 问题字符串与解析结果的配对

    none_dict = {question: result for question, result in all_dict.items()
                 if sum(ft[0] for ft in result) == 0}
    # 和任何模板都没有匹配的句子所组成的字典

    rest_dict = {question: result for question, result in all_dict.items()
                 if question not in none_dict}
    # 和某个或者某几个模板有匹配的句子所组成的字典

    rest_dict = {question: filter_true(result) for question, result
                 in rest_dict.items()}
    # 把不匹配的模板所返回的信息去掉，只保留相匹配的几个模板所返回的信息

    rest_dict2 = rest_dict.copy()
    # 在改动rest_dict之前保留它的一个副本

    rest_dict = {question: real_class(result) for question, result
                 in rest_dict.items()}
    # 从匹配的几个模板中找到最匹配的那个模板

    for question in questions:
        if question.question in list(rest_dict2.keys()):
            # 对已经有模板匹配的问题，改动问题实例的属性
            temp = real_class(rest_dict2[question.question])
            question.tpl = temp[3]
            question.hastpl = temp[0]
            question.expr = temp[1]
            question.matchscore = temp[2]
            question.mapping = temp[4]

    return rest_dict, none_dict
    # 返回有匹配的和没匹配的问题及匹配结果的字典


def tpl_process(rest_dict00, question_dict):
    questions101 = rest_dict00.keys()
    if len(questions101) > 0:
        question_ins101 = [question_in for question, question_in
                           in question_dict.items()
                           if question in questions101]

        for question in question_ins101:
            try:
                star_dog_print(question, "sparql", connect.sparql)
            # 对于每个问题，都查询结果
            except TypeError:  # TypeError: 'NoneType' object ...
                pass


def routine_process(many_questions, many_questions_ins, categories,
                    categories2):
    """经历两层一般模板的筛选和处理；本函数不使用问题类，而是被问题类调用"""
    if len(many_questions) > 0:
        many_question_dict = {question: question_in for
                              question, question_in
                              in zip(many_questions, many_questions_ins)}
        rest_dict, none_dict = questions_by_categories(categories,
                                                       many_questions_ins)
        # 经由categories模板的第一层处理

        questions2 = none_dict.keys()
        if len(questions2) > 0:
            many_questions_ins2 = [question_in for question, question_in
                                   in many_question_dict.items()
                                   if question in questions2]

            rest_dict2, none_dict2 = \
                questions_by_categories(categories2,
                                        many_questions_ins2)
            rest_dict.update(rest_dict2)
            # 经由categories2模板的第二层处理

        for question in many_questions_ins:
            try:
                star_dog_print(question, "sparql", connect.sparql)
            # 对于每个问题，都查询结果
            except TypeError:  # TypeError: 'NoneType' object ...
                pass
