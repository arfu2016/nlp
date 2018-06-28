"""
@Project   : CubeGirl
@Module    : depy_convert.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/15/18 11:47 AM
@Desc      : 把一个问题转变为一个或几个问题的类
"""
from .depy_parsing import Trees, CheckPartTreeComplex
# from .depy_sen_parser import sen_parser


class TemplateConvert:
    """Base class to convert a template"""
    template_name = None
    words_involved = None
    relations_involved = None
    targets_involved = None
    # question_parser = sen_parser

    def __new__(cls, *args, **kwargs):
        cls.template_name = cls.__name__
        return super().__new__(cls)

    def __init__(self, data):
        super(TemplateConvert, self).__init__()
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

        self.rule_trees, self.mapping_trees = zip(*rule_mapping)
        targets = [self.convert(self.rule_trees[i], self.mapping_trees[i],
                                list(words_list[i]), arcs_list[i])
                   for i in range(len(words_list))]

        return [self.rule_trees, targets,
                [self.length_tree(ele) for ele in self.mapping_trees],
                [self.template_name]*len(targets), self.mapping_trees]

    def convert(self, rule_target, mapping, words, arcs):
        raise NotImplementedError(
            'subclasses of QuestionGraph must provide a convert() method')

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

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        goal = ['']
        result = '; '.join(results)
        return ''.join(goal) + result
