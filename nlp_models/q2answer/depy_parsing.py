"""
@Project   : CubeGirl
@Module    : depy_parsing.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/19/17 11:34 AM
@Desc      : 给出句法分析类和问题图结构的基本类
"""
from collections import defaultdict


class QuestionGraph:
    """Base class to construct graph queries, 模板，单个模板与一组问题的交互"""
    # module_name = None
    # template_name = None
    words_involved = None
    relations_involved = None
    targets_involved = None

    def __new__(cls, *args, **kwargs):
        cls.template_name = cls.__name__
        return super().__new__(cls)

    def __init__(self, data):
        super(QuestionGraph, self).__init__()
        self.templates = [question.question for question in data]
        self.words_relations = [[question.words, question.postags,
                                 question.arcs] for question in data]
        self.mapping_trees = None
        self.rule_trees = None

    @staticmethod
    def length_tree(ele):
        if ele is None:
            return 0
        else:
            return len(ele)

    def interpret(self):
        # tpls_clean = self.templates
        # words_list, postags_list, arcs_list = \
        #     self.question_parser.parse_many_templates(tpls_clean)
        words_list, postags_list, arcs_list = zip(*self.words_relations)
        rule_mapping = [self.rule(list(words_list[i]), arcs_list[i])
                        for i in range(len(words_list))]

        # print('words_list in QuestionGraph.interpret() in depy_parsing.py:',
        #       [list(word_list) for word_list in words_list])
        # print('rule_mapping  in QuestionGraph.interpret() in depy_parsing:',
        #       rule_mapping)

        self.rule_trees, self.mapping_trees = zip(*rule_mapping)
        targets = [self.target(self.rule_trees[i], self.mapping_trees[i],
                               list(words_list[i]), arcs_list[i])
                   for i in range(len(words_list))]
        exprs = [self.transform(rule, target) for rule, target in
                 zip(self.rule_trees, targets)]
        # print('self.template_name in QuestionGraph in depy_parsing.py:',
        #       self.template_name)
        # print('words_list in QuestionGraph in depy_parsing.py:',
        #       [list(words) for words in words_list])
        # print('self.length_tree in QuestionGraph in depy_parsing.py:',
        #       [self.length_tree(ele) for ele in self.mapping_trees])
        return [self.rule_trees, exprs,
                [self.length_tree(ele) for ele in self.mapping_trees],
                [self.template_name]*len(exprs), self.mapping_trees]

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

    def rule(self, words, arcs):
        """本质上是分类问题，此处使用了关系（连接）规则，而非树规则"""
        relations_rule = self.relations_involved
        arcs_head = [arc.head - 1 for arc in arcs]
        arcs_relation = [arc.relation for arc in arcs]
        sentence_str = {index: (word, arcs_relation[index])
                        for index, word in enumerate(words)}
        relations_sentence = [(parent, child)
                              for child, parent in enumerate(arcs_head)
                              if parent >= 0]
        rule_tree = Trees(relations_rule)
        sentence_tree = Trees(relations_sentence)
        check = CheckPartTreeComplex(self.words_involved, sentence_str)
        if check.isParttree(sentence_tree.trees, rule_tree.trees):
            mapping_tree = check.mapping
            rule_tree = True
        else:
            mapping_tree = None
            rule_tree = False
        return rule_tree, mapping_tree

    def target(self, rule_target, mapping, words, arcs):
        pass

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result


class Child:
    def __init__(self, parent, relation, mapping, words, arcs):
        self.parent = mapping[parent]
        self.relation = relation
        self.words = words
        self.arcs = arcs

    def get_children(self):
        arcs_head = [arc.head - 1 for arc in self.arcs]
        tree_info = defaultdict(list)
        for i in range(len(arcs_head)):
            head = arcs_head[i]
            tree_info[head].append(i)
        return tree_info[self.parent]

    def get(self):
        arc_relations = [arc.relation for arc in self.arcs]
        children = self.get_children()
        for child in children:
            if arc_relations[child] == self.relation:
                return self.words[child]


class Trees:
    def __init__(self, edges):
        """Given a list of edges [parent, child], return trees. """
        trees = defaultdict(dict)

        for parent, child in edges:
            trees[parent][child] = trees[child]

        # Find roots
        if len(edges) > 0:
            parents, children = zip(*edges)
            roots = set(parents).difference(children)
            self.trees = {root: trees[root] for root in roots}
        else:
            self.trees = {}

        # return [trees[root] for root in roots]


class CheckPartTree:
    def isMatch(self, s, t):
        """
        s is the root of a large tree, t is the root of a small tree
        两棵树完全相同，或者小树为None，或者小树的children是大树children的子集
        :param s: dict
        :param t: dict
        :return: bool
        """
        if t == {}:
            return True
        if s == {}:
            return False
        troots = set([key for key in t.keys()])
        sroots = set([key for key in s.keys()])
        if not troots.issubset(sroots):
            # print(1, troots, sroots)
            return False
        for troot in list(troots):
            if not self.isMatch(s[troot], t[troot]):
                # print(2, troot)
                return False
        return True

    def isParttree(self, s, t):
        if self.isMatch(s, t):
            return True
        sroots = [key for key in s.keys()]
        for sroot in sroots:
            if self.isParttree(s[sroot], t):
                return True
        return False


def test_CheckPartTree():
    a = [(3, 4), (3, 5), (4, 1), (4, 2)]
    b = [(4, 1), (4, 2)]
    atree = Trees(a)
    btree = Trees(b)
    result = CheckPartTree().isParttree(atree.trees, btree.trees)
    print("True", result)

    a = [(3, 4), (3, 5), (4, 1), (4, 2), (2, 0)]
    b = [(4, 1), (4, 2)]
    atree = Trees(a)
    btree = Trees(b)
    result = CheckPartTree().isParttree(atree.trees, btree.trees)
    print("True", result)

    a = [(3, 4), (3, 5), (4, 2), (2, 0)]
    b = [(4, 1), (4, 2)]
    atree = Trees(a)
    btree = Trees(b)
    result = CheckPartTree().isParttree(atree.trees, btree.trees)
    print("False", result)

    a = [(3, 4), (3, 5)]
    b = [(4, 1), (4, 2)]
    atree = Trees(a)
    btree = Trees(b)
    result = CheckPartTree().isParttree(atree.trees, btree.trees)
    print("False", result)


class CheckPartTreeComplex:
    def __init__(self, rule_str, sentence_str):
        self.rule_str = rule_str
        self.sentence_str = sentence_str
        self.mapping = dict()

    @staticmethod
    def compare(a, b):
        if a == 'ANY':
            return True
        # return a == b
        return b in a

    def judge_in(self, a, b):
        for b_ele in list(b):
            if self.compare(self.rule_str[a][0], self.sentence_str[b_ele][0]) \
                    and self.compare(self.rule_str[a][1],
                                     self.sentence_str[b_ele][1]):
                return b_ele
            # 只要匹配就返回，即使list(b)中还有其他元素匹配，也不再进行
        return None

    def judge_subset(self, a, b):
        temp_mapping = dict()
        for a_ele in list(a):
            temp_judge = self.judge_in(a_ele, b)
            if temp_judge is None:
                # print('应该是None：', self.judge_in(a_ele, b))
                return None
            else:
                temp_mapping.update({a_ele: temp_judge})
        return temp_mapping

    def isMatch(self, s, t):
        """
        s is the root of a large tree, t is the root of a small tree
        两棵树完全相同，或者小树为None，或者小树的children是大树children的子集
        :param s: dict
        :param t: dict
        :return: bool
        """
        if t == {}:
            return True
        if s == {}:
            return False
        troots = set([key for key in t.keys()])
        sroots = set([key for key in s.keys()])
        temp_judge = self.judge_subset(troots, sroots)
        if temp_judge is None:
            # print(1, troots, sroots)
            return False
        self.mapping.update(temp_judge)
        # print('对应关系：', temp_judge)
        for troot in list(troots):
            if not self.isMatch(s[temp_judge[troot]], t[troot]):
                # print(2, troot)
                return False
        return True

    def isParttree(self, s, t):
        if self.isMatch(s, t):
            # print(3, s.keys(), t.keys())
            return True
        sroots = [key for key in s.keys()]
        # print(6, sroots)
        for sroot in sroots:
            if self.isParttree(s[sroot], t):
                # print(4)
                return True
        return False
