"""
@Project   : CubeGirl
@Module    : depy_sparql_generation.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/19/17 4:40 PM
@Desc      : 把图表达式转换为sparql语句
"""
from . import depy_settings as settings
from .depy_expression import isnode, isedge
# from .depy_encodingpolicy import assert_valid_encoding

_indent = "  "


def escape(string):
    string = string.replace("\n", "")
    string = string.replace("\r", "")
    string = string.replace("\t", "")
    string = string.replace("\x0b", "")
    if not string or any([x for x in string if 0 < ord(x) < 31]) or \
            string.startswith(":") or string.endswith(":"):
        message = "Unable to generate sparql: invalid nodes or relation"
        raise ValueError(message)
    # 表示relation或者常量node的string中是否包含不该有的字符
    return string


def adapt(x, edge):
    if isnode(x):
        # 必须是变量node
        x = "?x{}".format(x)
        return x
    if isedge(x):
        x = "?y{}".format(edge[x])
        return x
    # if isinstance(x, str):
    # if isinstance(x, basestring):
    #     assert_valid_encoding(x)
    #     if x.startswith(u"\"") or ":" in x:
    #         return x
    #     return u'"{}"'.format(x)
    # return unicode(x)
    return x


def expression_to_sparql(e, full=False):
    template = "{preamble}\n" +\
               "SELECT DISTINCT {select} WHERE {{\n" +\
               "{expression}\n" +\
               "}}\n"
    try:
        y = -1
        xs = []
        edge = {}
        isrelate = {}
        for node in e.iter_nodes():
            for relation, dest in e.iter_edges(node):
                if not isinstance(relation, str):
                    # if relation is IsRelatedTo:
                    # 一种特殊的relation；关系动词是变量？
                        if relation in isrelate:
                            y = isrelate[relation]
                        else:
                            y += 1
                            isrelate.update({relation: y})
                        relation = "?y{}".format(y)
                        edge.update({(node, dest): y})
                xs.append(triple(adapt(node, edge), relation,
                                 adapt(dest, edge), indentation=1))

        head = adapt(e.get_head(), edge)
        # select = head
        if full:
            select = "*"
        else:
            select = head

        sparql = template.format(preamble=settings.SPARQL_PREAMBLE,
                                 select=select,
                                 expression="\n".join(xs))
        return select, sparql
    except AttributeError:
        print('None can not convert to sparql')


def triple(a, p, b, indentation=0):
    """
    用来把三元组格式化
    :param a:
    :param p:
    :param b:
    :param indentation:
    :return:
    """
    a = escape(a)
    b = escape(b)
    p = escape(p)
    s = _indent * indentation + "{0} {1} {2}."
    return s.format(a, p, b)
