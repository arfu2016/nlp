"""
@Project   : CubeGirl
@Module    : class3_sparql.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/2/18 4:23 PM
@Desc      : Sparql templates which return sparql function
"""
from .depy_relation import relation
# 可能在insert()方法中用到
from .depy_words_tpl import SparqlTpl
from .depy_sparql_connect import connect, sparql
from .sparql_statements import sparql_dict


def query_sparql(example):
    sparql.setQuery(example)
    results = sparql.query().convert()
    # 得到查询返回的json格式
    return results


def get_query_value(result, index):
    return list(result.values())[index]['value']


def parse_sparql_single(results):
    results_or = results['results']['bindings']
    results_list = [get_query_value(result, 0)
                    for result in results_or]
    return results_list


def parse_sparql_pair(results):
    results_or = results['results']['bindings']
    results_list = [(get_query_value(result, 0), get_query_value(result, 1))
                    for result in results_or]
    return results_list


class WorldCup1(SparqlTpl):
    """哪些球员是俱乐部队友"""
    example0 = sparql_dict['worldcup1_0']
    example1 = sparql_dict['worldcup1_1']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""

            results = query_sparql(self.example0)
            results_list = parse_sparql_single(results)

            result_for_return = list()

            for result in results_list:
                example = self.example1.format(
                    select='?x1',
                    expression="  ?x2 aiball:cnName {}.".
                               format('"{}"'.format(result)))

                results = query_sparql(example)
                results = parse_sparql_single(results)

                people_club = '， '.join(results) + '所在俱乐部是{}'.format(result)
                result_for_return.append(people_club)

            return result_for_return

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            goal = ['']
            result = '；\n\n'.join(results)
            return ''.join(goal) + result
        else:
            return '未找到相关信息'


class WorldCup2(SparqlTpl):
    """哪些球员俱乐部是死敌"""
    example0 = sparql_dict['worldcup2']

    def get_sparql_function(self, targets):

        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            results_json = query_sparql(self.example0)
            results_or = parse_sparql_pair(results_json)

            results_list = []
            results_inspect = []
            for front, back in results_or:
                if {front, back} not in results_inspect:
                    results_inspect.append({front, back})
                    results_list.append('{}和{}是死敌'.format(front, back))

            return results_list

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            begin = '两队球员所在的俱乐部中：\n\n'
            result = '；\n\n'.join(results)
            end = '。对于哪些球员效力于某个具体俱乐部，比如可以问"哪些球员效力于切尔西"'
            return begin + result + end
        else:
            return '未找到相关信息'


class WorldCup4(SparqlTpl):
    """哪些球员儿子是球员"""
    example0 = sparql_dict['worldcup4']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""

            example = self.example0.format(
                select='?x2',
                expression="  ?x1 aiball:type {}.".
                           format('"{}"'.format(targets[0][0])))

            results = query_sparql(example)
            results_list = parse_sparql_single(results)

            return results_list

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            end = '这些球员的儿子也是球员。 对于球员儿子的具体情况，比如可以问“克林斯曼的儿子是踢什么位置的"'
            result = ', '.join(results)
            return result + end
        else:
            return '未找到相关信息'


class WorldCup8(SparqlTpl):
    """哪些德国/英格兰球员是俱乐部队友"""
    example0 = sparql_dict['worldcup8_0']
    example1 = sparql_dict['worldcup1_1']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""

            example = self.example0.format(
                select='?x3',
                expression="  ?x4 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results = query_sparql(example)
            results_list = parse_sparql_single(results)

            result_for_return = list()

            for result in results_list:
                example = self.example1.format(
                    select='?x1',
                    expression="  ?x2 aiball:cnName {}.".
                               format('"{}"'.format(result)))

                results = query_sparql(example)
                results = parse_sparql_single(results)

                people_club = '， '.join(results) + '所在俱乐部是{}'.format(result)
                result_for_return.append(people_club)

            return result_for_return

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            goal = ['']
            result = '；\n\n'.join(results)
            return ''.join(goal) + result
        else:
            return '未找到相关信息'


class WorldCup9(SparqlTpl):
    """两队球员效力于哪些俱乐部"""

    example0 = sparql_dict['worldcup9']

    def get_sparql_function(self, targets):

        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            results_json = query_sparql(self.example0)
            results_list = parse_sparql_single(results_json)

            return results_list

        return sparql_function


class WorldCup10(SparqlTpl):
    """西德球员效力于哪些俱乐部"""

    example0 = sparql_dict['worldcup10']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""

            example = self.example0.format(
                select='?x2',
                expression="  ?x3 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list = parse_sparql_single(results_json)
            return results_list

        return sparql_function


class WorldCup11(SparqlTpl):
    """哪些球员效力于切尔西"""
    example0 = sparql_dict['worldcup11']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            example = self.example0.format(
                select='?x2',
                expression="  ?x1 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list = parse_sparql_single(results_json)

            result_words = ', '.join(results_list) + \
                           '效力于{}'.format(targets[0][0])
            return [result_words]

        return sparql_function


class WorldCup12(SparqlTpl):
    """哪些西德球员效力于切尔西"""

    example0 = sparql_dict['worldcup12']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            example = self.example0.format(
                select='?x2',
                expression1="  ?x1 aiball:cnName {}.".
                            format('"{}"'.format(targets[1][0])),
                expression2="  ?x3 aiball:cnName {}.".
                            format('"{}"'.format(targets[0][0])),
            )

            results_json = query_sparql(example)
            results_list = parse_sparql_single(results_json)
            return results_list

        return sparql_function


class WorldCup13(SparqlTpl):
    """哪些球员儿子是前锋/守门员"""

    example0 = sparql_dict['worldcup13_0']
    example1 = sparql_dict['worldcup13_1']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            example = self.example0.format(
                select='?x2',
                expression="  ?x1 aiball:position {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list = parse_sparql_single(results_json)

            result_for_return = list()

            for result in results_list:
                example = self.example1.format(
                    select='?x2',
                    expression="  ?x0 aiball:cnName {}.".
                               format('"{}"'.format(result)))
                results_json = query_sparql(example)

                results = parse_sparql_single(results_json)

                people = '{}的儿子'.format(result) + ''.join(results)
                result_for_return.append(people)
            if len(results_list) > 0:
                result_word = [', '.join(result_for_return) +
                               '司职{}'.format(targets[0][0])]
            else:
                result_word = ['暂时没有球员儿子是{}'.format(targets[0][0])]

            return result_word

        return sparql_function


class WorldCup14(SparqlTpl):
    """克林斯曼的儿子是踢什么位置的"""
    example0 = sparql_dict['worldcup14_0']
    example1 = sparql_dict['worldcup14_1']
    example2 = sparql_dict['worldcup14_2']

    def get_sparql_function(self, targets):

        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            example = self.example0.format(
                select='?x2',
                expression="  ?x0 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list_name = parse_sparql_single(results_json)

            example = self.example1.format(
                select='?x2',
                expression="  ?x0 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list_position = parse_sparql_single(results_json)

            example = self.example2.format(
                select='?x3',
                expression="  ?x0 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list_club = parse_sparql_single(results_json)

            if len(results_list_club) > 0 and len(results_list_position) > 0:

                results_list = ['{}的儿子是{}, 司职{}, 目前效力于{}俱乐部'.format(
                    targets[0][0], results_list_name[0],
                    results_list_position[0],
                    results_list_club[0])]
            else:
                results_list = []
            return results_list

        return sparql_function


class WorldCup21(SparqlTpl):
    """场上哪些西德球员俱乐部是死敌"""
    example0 = sparql_dict['worldcup21']

    def get_sparql_function(self, targets):

        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""
            example = self.example0.format(
                select='?x4 ?x5',
                expression="  ?x6 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_or = parse_sparql_pair(results_json)

            results_list = []
            results_inspect = []
            for front, back in results_or:
                if {front, back} not in results_inspect:
                    results_inspect.append({front, back})
                    results_list.append('{}和{}是死敌'.format(front, back))

            return results_list

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            goal = ['']
            result = '；\n\n'.join(results)
            return ''.join(goal) + result
        else:
            return '未找到相关信息'


class WorldCup22(SparqlTpl):
    """XX的妻子是谁"""
    code = 2190
    example0 = sparql_dict['worldcup22_0']
    example1 = sparql_dict['worldcup22_1']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""

            example = self.example0.format(
                select='?x2',
                expression="  ?x0 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list = parse_sparql_single(results_json)
            # 之前pair的时候出错, index error，意外的错误
            # 意料之中的exception专门处理，可以写入类似standard out的日志
            # 如果不是意料之中，最好写入错误日志，类似standard error的日志
            # 用日志的话，出问题的行号也能记录，可见logging的重要性

            example = self.example1.format(
                select='?x2',
                expression="  ?x0 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list_link = parse_sparql_single(results_json)
            # 之前pair的时候出错, index error，意外的错误

            if len(results_list) == 0:
                results_list = ['未找到相关信息']
            if len(results_list_link) == 0:
                results_list_link = ['']
            results_list.extend(results_list_link)

            return results_list

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            answer = results[0]
            links = (results[1],)
            return {'sentence': answer, 'links': links}
        else:
            return '未找到相关信息'


class WorldCup24(SparqlTpl):
    """XX离过几次婚"""
    example0 = sparql_dict['worldcup24']

    def get_sparql_function(self, targets):
        def sparql_function():
            """既解决怎么查的问题，也解决sparql返回结果怎么抽的问题"""

            example = self.example0.format(
                select='?x1',
                expression="  ?x0 aiball:cnName {}.".
                           format('"{}"'.format(targets[0][0])))

            results_json = query_sparql(example)
            results_list = parse_sparql_single(results_json)

            results_numbers = [result.split('.')[0] for result in results_list]
            results_list = ['{}离过{}次婚'.
                            format(targets[0][0], results_numbers[0])]

            return results_list

        return sparql_function


class WorldCup25(SparqlTpl):
    """哪个球员离婚次数最多"""

    def get_sparql_function(self, targets):
        def sparql_function():
            results_list = ['马特乌斯离婚次数最多，离过4次婚，结过5次婚']

            return results_list

        return sparql_function


class WorldCup26(SparqlTpl):
    """哪个球员老婆最漂亮"""
    code = 2190

    def get_sparql_function(self, targets):

        def sparql_function():
            results_list = ['莱因克尔老婆最漂亮',
                            'https://wx3.sinaimg.cn/mw1024/006xJSW9gy1fp2ydr80o1j31400p0dlr.jpg']

            return results_list

        return sparql_function

    @staticmethod
    def specific_nlg(results):
        if len(results) > 0:
            answer = results[0]
            links = (results[1],)
            return {'sentence': answer, 'links': links}
        else:
            return '未找到相关信息'
