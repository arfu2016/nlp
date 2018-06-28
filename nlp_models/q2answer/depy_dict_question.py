"""
@Project   : CubeGirl
@Module    : tpl_dict.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/16/18 2:44 PM
@Desc      : Question类，从名字到问题类的转换字典
"""
from .depy_sen_parser import sen_parser
from .depy_question_template import star_dog_print, questions_by_categories
from .depy_sparql_connect import connect
from .depy_question_template import routine_process
from .class_registry import registered_classes


def specific_process(none_dict0, question_dict, categories11):
    """在本函数中使用了问题类，适用于对应着唯一问题类的模板类"""
    questions11 = none_dict0.keys()
    if len(questions11) > 0:
        questions_ins11 = [question_in for question, question_in
                           in question_dict.items()
                           if question in questions11]

        rest_dict1, none_dict1 = questions_by_categories(categories11,
                                                         questions_ins11)

        questions12 = rest_dict1.keys()
        questions_ins12 = [question_in for question, question_in
                           in question_dict.items()
                           if question in questions12]

        for question in questions_ins12:
            try:
                star_dog_print(question, "sparql", connect.sparql)
            # 对于每个问题，都查询结果
            except TypeError:  # TypeError: 'NoneType' object ...
                pass

        for question in questions12:
            template = \
                registered_classes[question_dict[question].tpl].question_template
            the_question = question_tpl[template](question)
            # 难点在于函数调用避免循环调用，在本函数中调用了问题类，所以在问题类的方法中，
            # 就不应该使用本函数了
            # 一个问题最多对应着两套Question类，一套是SimpleQuestion,
            # 另一套是MutltipleQuestion或者具体的问题类
            the_question.expr = question_dict[question].expr
            the_question.result = question_dict[question].result

            the_question.modify_result()
            question_dict[question].result = the_question.result

        return none_dict1
    else:
        return none_dict0


class Question:

    def __init__(self, question, qid=dict()):
        self.question = question
        # 保存的是原始问题
        self.tpl = None
        self.hastpl = None
        self.matchscore = None
        self.expr = None
        self.sparql = None
        self.result = None
        self.answer = None
        self.mapping = None

        words, postags, arcs = sen_parser.parse_one_template(question)
        self.words = list(words)
        self.postags = list(postags)
        self.arcs = arcs
        self.code = -1

    def parse(self):
        pass

    def modify_result(self):
        pass

    def answer_question(self):
        words = self.words
        arcs = self.arcs

        rule = self.hastpl
        results = self.result
        template = self.tpl

        mapping = self.mapping
        if rule:
            targets = registered_classes[template].generate(mapping, words,
                                                            arcs,
                                                            results)
            self.answer = targets

        temp = self.result
        if temp is None or len(''.join(temp).strip()) == 0:
            # 对于一个问题拆成多个问题的情况，result可能是[' ']
            # self.answer = '对不起，没有您需要的信息'
            self.answer = None


class SparqlQuestion(Question):
    """直接查询sparql的问题"""
    def __init__(self, question, qid=dict()):
        super().__init__(question, qid)
        self.sparql_func = None
        self.register = registered_classes
        # 也可以使用一个属性保存对应的模板类实例，即类的组合

    def answer_question(self):
        template = self.tpl

        if len(template) > 0:
            answer = self.register[template].generate(self.sparql_func)
            self.answer = answer
            self.code = self.register[template].code
        else:
            self.answer = None


class SimpleQuestion(Question):
    """一般问题"""
    pass


class MultipleQuestion(Question):
    """可以进行转换的问题，一个转一个或者一个转多个"""

    def run_singles(self, convert_dict, categories, categories2):
        many_questions = convert_dict[self.question]
        many_questions_ins = [SimpleQuestion(question) for question
                              in many_questions]
        routine_process(many_questions, many_questions_ins, categories,
                        categories2)

        result_list = [question.result for question in many_questions_ins]
        result_list = [result[0] if len(result) > 0 else ''
                       for result in result_list]
        # 把本属于一个原始问题的结果放到一个列表当中
        self.result = [' '.join(result_list)]
        # 此处，连接多个sparql所产生的结果时，中间用空格


class YesornoQuestion(Question):
    """问有没有、是不是的问题"""

    def modify_result(self):
        try:
            if len(self.result) == 0:
                self.result = ['No']
            else:
                self.result = ['Yes']
        except TypeError:
            self.result = None


class HowmanyQuestion(Question):
    """问有几个的问题"""

    def modify_result(self):
        try:
            if len(self.result) == 0:
                self.result = ['一个都没有']
            else:
                temp = ', '.join(self.result)
                num = len(self.result)
                self.result = ['有{}个：'.format(num), temp]
        except TypeError:
            self.result = None


class Howmanycanjiashijiebei(HowmanyQuestion):
    """参加过多少次世界杯"""

    def modify_result(self):
        self.parse()
        person_list = [self.words[i] for i in [0, 2]]
        temp = self.result
        self.result = [person for person in person_list if person in temp]
        super().modify_result()


class QuestionAfterQuestion(Question):
    """有代表性的复杂问法，存在sparql的嵌套"""
    def multiple_queries(self):
        """构建所需要的多次查询"""
        pass

    def concatenate_results(self):
        """把多次查询的结果连起来"""
        pass


class SpecificQuestion(Question):
    """没有代表性的复杂问法，存在sparql的嵌套，具体问题具体处理"""
    def generate_sparql(self):
        """带参数的sparql模板，一旦参数确定，sparql语句就确定"""
        pass

    class Template:
        """确定符合模板，通过某个函数返回查询语句需要的参数"""
        pass


question_tpl = {'YesornoQuestion': YesornoQuestion,
                'Howmanycanjiashijiebei': Howmanycanjiashijiebei}
