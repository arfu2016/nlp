"""
@Project   : CubeGirl
@Module    : depy_dsl.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/19/17 11:28 AM
@Desc      : 图结构edge定义的基类
"""
from copy import copy

from .depy_encodingpolicy import encoding_flexible_conversion
from .depy_expression import Expression


class FixedRelation(Expression):
    """
    Expression for a fixed relation. It states that "A is related to B"
    through the relation defined in `relation`.
    """

    relation = None
    reverse = False

    def __init__(self, destination, reverse=None):
        if reverse is None:
            reverse = self.reverse
        super(FixedRelation, self).__init__()
        if self.relation is None:
            raise ValueError("You *must* define the `relation` "
                             "class attribute to use this class.")
        self.nodes = copy(destination.nodes)
        self.head = destination.head
        self.decapitate(self.relation, reverse)


class FixedDataRelation(Expression):
    """
    Expression for a fixed relation. This is
    "A is related to Data" through the relation defined in `relation`.
    """

    relation = None
    language = None

    def __init__(self, data):
        super(FixedDataRelation, self).__init__()
        if self.relation is None:
            raise ValueError("You *must* define the `relation` "
                             "class attribute to use this class.")
        self.relation = encoding_flexible_conversion(self.relation)
        # could be bytes
        # relation可能是IsRelatedTo类，此处如果是这样，则会报错
        if self.language is not None:
            self.language = encoding_flexible_conversion(self.language)
            data = "\"{0}\"@{1}".format(data, self.language)
        self.add_data(self.relation, data)


class HasKeyword(FixedDataRelation):
    """
    Abstraction of an information retrieval key, something standarized used
    to look up things in the database.
    """
    relation = "quepy:Keyword"

    def __init__(self, data):
        data = self.sanitize(data)
        super(HasKeyword, self).__init__(data)

    @staticmethod
    def sanitize(text):
        # User can redefine this method if needed
        return text


class IsRelatedTo(FixedRelation):
    pass
    # Looks weird, yes, here I am using `IsRelatedTo` as a unique identifier.


IsRelatedTo.relation = IsRelatedTo
# class attribute, relation is a class
# relation could be something other than str in FixedRelation class and
# Expression class
# IsRelatedTo这个类的relation是变量，表知的是一个动词为未知的FixedRelation类


class IsRelatedTo2(FixedRelation):
    pass


IsRelatedTo2.relation = IsRelatedTo2


class HasProperty(FixedDataRelation):

    def __init__(self, data, attr):
        self.relation = attr
        super(HasProperty, self).__init__(data)


class ArelationB(FixedRelation):

    def __init__(self, destination, attr, reverse=True):
        self.relation = attr
        self.reverse = reverse
        super(ArelationB, self).__init__(destination, self.reverse)
