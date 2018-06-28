"""
@Project   : CubeGirl
@Module    : depy_sparql_test.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/29/18 1:16 PM
@Desc      : 
"""

from Daka.chatbot.logic.knowledge_graph.q2answer.depy_sparql_connect \
    import connect


if __name__ == '__main__':

    example = '''
    SELECT DISTINCT ?x2 WHERE {
      ?x0 aiball:futureWife ?x1.
      ?x1 aiball:cnName ?x2.
      ?x0 aiball:cnName "保罗·加斯科因".
    }
    '''

    # 弗朗茨·贝肯鲍尔, 洛塔尔·马特乌斯
    # FILTER(?x4 != ?x5).

    # SELECT DISTINCT ?x0 WHERE {
    #   ?x0 aiball:cnName "阿根廷"
    # }
    # SELECT ?x0 ?y0 WHERE {
    #   ?x0 ?y0 "阿根廷"
    # }
    # SELECT ?x1 ?x0 WHERE {
    #   ?x1 aiball:team ?x0.
    #   ?x0 aiball:cnName "阿根廷".
    # }

    sparql = connect.sparql
    sparql.setQuery(example)
    results0 = sparql.query().convert()
    print('Result of the example:', results0, '\n')
