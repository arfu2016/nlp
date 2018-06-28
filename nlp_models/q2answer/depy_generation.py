"""
@Project   : CubeGirl
@Module    : depy_generation.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/19/17 4:37 PM
@Desc      : 从图表达式到sparql的入口
"""
from .depy_sparql_generation import expression_to_sparql

"""
Code generation from an expression to a database language.

The currently supported languages are:
    * MQL
    * Sparql
    * Dot: generation of graph images mainly for debugging.
"""


def get_code(expression, language):
    """
    Given an expression and a supported language, it
    returns the query for that expression on that language.
    """

    if language == "sparql":
        return expression_to_sparql(expression)
    # elif language == "dot":
    #     return expression_to_dot(expression)
    # elif language == "mql":
    #     return generate_mql(expression)
    else:
        message = "Language '{}' is not supported"
        raise ValueError(message.format(language))
