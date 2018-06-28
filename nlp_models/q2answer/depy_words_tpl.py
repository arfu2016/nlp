"""
@Project   : CubeGirl
@Module    : depy_words_tpl.py
@Author    : Deco [deco@cubee.com]
@Created   : 2/6/18 10:15 AM
@Desc      : Base classes for sequence templates
"""
import re

from .depy_sparql_connect import sparql
from . import depy_settings as settings

from .depy_relation import OneTermForTpl
from .depy_parsing import Trees, CheckPartTreeComplex
from .depy_generation import get_code


class WordsTpl:
    """Base class to construct graph queries, 模板，单个模板与一组问题的交互"""
    words_involved = None
    relations_involved = None
    targets_involved = None
    selects = None

    def __new__(cls, *args, **kwargs):
        cls.template_name = cls.__name__
        return super().__new__(cls)

    def __init__(self, data):
        super().__init__()
        self.templates = [question.question for question in data]
        self.words_relations = [[question.words, question.postags,
                                 question.arcs] for question in data]
        self.mapping_trees = None
        self.rule_trees = None

    def interpret(self):
        words_list, postags_list, arcs_list = zip(*self.words_relations)
        rule_mapping = [self.rule(list(words_list[i]))
                        for i in range(len(words_list))]
        self.rule_trees, self.mapping_trees = zip(*rule_mapping)

        targets = [self.target(self.rule_trees[i], list(words_list[i]))
                   for i in range(len(words_list))]
        exprs = [self.transform(rule, target) for rule, target in
                 zip(self.rule_trees, targets)]
        return [self.rule_trees, exprs,
                [ele is True for ele in self.rule_trees],
                [self.template_name]*len(exprs), [None]*len(exprs)]

    def transform(self, rule, target):
        if rule:
            graph_expression = self.graph(target)
            return graph_expression
            # a graph expression
        else:
            return None

    def graph(self, target):
        raise NotImplementedError(
            'subclasses of QuestionGraph must provide a graph() method')

    def rule(self, words):
        """本质上是分类问题，此处使用了关系（连接）规则，而非树规则"""
        relations_rule = self.relations_involved
        sentence_str = list(words)
        if len(relations_rule) != len(sentence_str):
            return False, None
        for i in range(len(relations_rule)):
            if relations_rule[i] is not None and \
                            sentence_str[i] not in relations_rule[i]:
                return False, None
        return True, None

    @staticmethod
    def insert(existing_entity):
        pass

    def target(self, rule_target, words):
        """本质上是实体抽取问题，此处需要显式的给定实体抽取的规则"""
        if rule_target:
            words2 = [words[i] for i in self.selects]
            entities = [OneTermForTpl(word).get_self() for word in words2]
            goal = self.insert(entities)
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class MetaClass(type):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        cls.template_name = cls.__name__


class SparqlTpl(metaclass=MetaClass):
    """Base class to construct sparql queries, 模板，单个模板与单个问题的交互"""
    code = 2049
    example0 = ''
    example1 = ''

    whether_sequence_tpl = True
    whether_sequence__extract = True
    relations_involved = None
    selects = None

    whether_re_tpl = False  # regular expression
    whether_re_extract = False
    whether_container_tpl = False  # 模板中规定词的集合的集合
    whehter_container_extract = False
    whether_syntac_tpl = False  # syntactic method
    whether_syntac_extract = False
    whether_dl_tpl = False  # deep learning
    whether_dl_extract = False
    whether_external_tpl = False  # external method
    whether_external_extract = False

    def __init__(self, question_in):
        self.question = question_in.question
        self.words = question_in.words
        self.postags = question_in.postags
        self.arcs = question_in.arcs
        self.rule_of_tpl = False
        #  是否符合本模板
        self.spq_func = None
        #  本模板实例的意图处理函数
        self.other_spq_funcs = None
        # 预留的接口，暂时没有用到

    def sequence_intent_recognition(self):
        """对于sequence规则，意图识别"""
        relations_rule = self.relations_involved
        sentence_str = self.words
        if len(relations_rule) != len(sentence_str):
            return False
        for i in range(len(relations_rule)):
            if relations_rule[i] is not None and \
                            sentence_str[i] not in relations_rule[i]:
                return False
        return True

    def re_intent_recognition(self):
        # todo: 添加正则规则的意图识别
        return True

    def rule(self):
        """意图识别函数"""
        if self.whether_sequence_tpl:
            sequence_match = self.sequence_intent_recognition()
        else:
            sequence_match = True

        if sequence_match:
            if self.whether_re_tpl:
                re_match = self.re_intent_recognition()
            else:
                re_match = True

            return re_match

        return sequence_match

    def sequence_entity_extract(self):
        words_select = [self.words[i] for i in self.selects]
        entities = [OneTermForTpl(word).get_self()
                    for word in words_select]
        return entities

    def target(self, rule_true):
        """本质上是实体抽取，此处使用sequence_entity_extract()方法，
        也可以使用其他方法"""
        if rule_true:
            entities = self.sequence_entity_extract()
            goal = self.insert(entities)
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

    def get_sparql_function(self, targets):
        """
        :param targets: List
        :return:
        """
        raise NotImplementedError(
            'subclasses of SparqlTpl must provide a get_sparql() method')

    @staticmethod
    def get_other_sparqls_function(target_groups):
        """
        预留的接口，暂时没有用到
        :param target_groups: List, list of list
        :return:
        """
        pass

    def interpret(self):
        """从意图识别到意图处理；
        在子类中可以重载，同时可以激活预留的self.other_spq_funcs"""
        self.rule_of_tpl = self.rule()
        # 意图识别
        target = self.target(self.rule_of_tpl)
        # 在具体模板下做实体抽取
        if self.rule_of_tpl:
            self.spq_func = self.get_sparql_function(target)
            # 得到对应的意图处理函数

    @classmethod
    def generate(cls, spq_func):
        """话术生成"""
        results = spq_func()
        return cls.specific_nlg(results)

    @staticmethod
    def specific_nlg(results):
        """话术生成的模式"""
        if len(results) > 0:
            begin = ''
            end = '。'
            result = '； '.join(results)
            answer = begin + result + end
            return answer
        else:
            return '未找到相关信息'


class SyntacTpl(SparqlTpl):

    score = 0
    words_for_syntac = []
    syntac_tree = []
    targets_for_syntac = []
    mapping = dict()
    sparql_state = ''

    def select_tpl(self):
        arcs_head = [arc.head - 1 for arc in self.arcs]
        arcs_relation = [arc.relation for arc in self.arcs]
        sentence_str = {index: (word, arcs_relation[index])
                        for index, word in enumerate(self.words)}
        check = CheckPartTreeComplex(self.words_for_syntac, sentence_str)

        relations_sentence = [(parent, child)
                              for child, parent in enumerate(arcs_head)
                              if parent >= 0]
        sentence_tree = Trees(relations_sentence)

        rule_tree = Trees(self.syntac_tree)

        if check.isParttree(sentence_tree.trees, rule_tree.trees):
            self.rule_of_tpl = True
            self.mapping = check.mapping
            self.score = len(self.syntac_tree)

    def graph(self, target):
        raise NotImplementedError(
            'subclasses of QuestionGraph must provide a graph() method')

    def select_processor(self):
        target = self.target(self.rule_of_tpl)
        if self.rule_of_tpl:
            self.spq_func = self.get_sparql_function(target)
            # 得到对应的意图处理函数

    def target(self, rule_true):
        """必须重载父类的该函数"""
        raise NotImplementedError(
            'subclasses of QuestionGraph must provide a graph() method')

    def get_sparql_function(self, targets):
        """返回一个函数"""
        # print('targets in get_sparql_function in depy_words_tpl.py',
        #       targets)

        def sparql_function():
            graph_expression = self.graph(targets)
            self.sparql_state = get_code(graph_expression, 'sparql')[1]

            sparql.setQuery(self.sparql_state)
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
                        result = re.sub(r'http://www.aiball.com/', 'aiball:',
                                        result)
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

            return result_list

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        """话术生成的模式"""
        if len(results) > 0:
            begin = ''
            end = '。'
            result = '； '.join(results)
            answer = begin + result + end
            return answer
        else:
            return None
            # return '未找到相关信息'
            # 由于句法模板的模糊性，为了避免拦住在句法模板后还要处理意图的模块
            # 比如，切尔西的死敌，不应该不句法模板拦住
