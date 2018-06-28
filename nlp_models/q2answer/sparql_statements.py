"""
@Project   : CubeGirl
@Module    : sparql_statements.py
@Author    : Deco [deco@cubee.com]
@Created   : 3/14/18 3:28 PM
@Desc      : sparql语句
"""

worldcup1_0 = '''
        SELECT DISTINCT ?x3 WHERE {
          ?x0 aiball:type "俱乐部".
          ?x1 aiball:currentTeam ?x0.
          ?x2 aiball:currentTeam ?x0.
          ?x1 aiball:belong "比赛大名单".
          ?x2 aiball:belong "比赛大名单".
          ?x0 aiball:cnName ?x3.
          FILTER(?x1 != ?x2).
    
        }
        '''

worldcup1_1 = "SELECT DISTINCT {select} WHERE {{\n" + \
                   "  ?x0 aiball:cnName ?x1.\n" + \
                   "  ?x0 aiball:belong '比赛大名单'.\n" + \
                   "  ?x0 aiball:currentTeam ?x2.\n" + \
                   "{expression}\n" + \
                   "}}\n"

worldcup2 = '''
SELECT DISTINCT ?x4 ?x5 WHERE {
  ?x0 aiball:type "俱乐部".
  ?x1 aiball:type "俱乐部".
  ?x0 aiball:rival ?x1.
  ?x2 aiball:currentTeam ?x0.
  ?x3 aiball:currentTeam ?x1.
  ?x2 aiball:belong "比赛大名单".
  ?x3 aiball:belong "比赛大名单".
  ?x0 aiball:cnName ?x4.
  ?x1 aiball:cnName ?x5.

}
'''

worldcup4 = "SELECT DISTINCT {select} WHERE {{\n" + \
                       "  ?x0 aiball:son ?x1.\n" + \
                       "  ?x0 aiball:cnName ?x2.\n" + \
                       "  ?x0 aiball:belong '比赛大名单'.\n" + \
                       "{expression}\n" + \
                       "}}\n"

worldcup8_0 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:type '俱乐部'.\n" + \
           "  ?x1 aiball:currentTeam ?x0.\n" + \
           "  ?x2 aiball:currentTeam ?x0.\n" + \
           "  ?x1 aiball:currentTeam ?x4.\n" + \
           "  ?x2 aiball:currentTeam ?x4.\n" + \
           "  ?x1 aiball:belong '比赛大名单'.\n" + \
           "  ?x2 aiball:belong '比赛大名单'.\n" + \
           "  ?x0 aiball:cnName ?x3.\n" + \
           "  FILTER(?x1 != ?x2).\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup9 = '''
SELECT DISTINCT ?x2 WHERE {
  ?x0 aiball:currentTeam ?x1.
  ?x1 aiball:type "俱乐部".
  ?x0 aiball:belong "比赛大名单".
  ?x1 aiball:cnName ?x2.
}
'''

worldcup10 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:currentTeam ?x1.\n" + \
           "  ?x1 aiball:type '俱乐部'.\n" + \
           "  ?x0 aiball:belong '比赛大名单'.\n" + \
           "  ?x1 aiball:cnName ?x2.\n" + \
           "  ?x0 aiball:currentTeam ?x3.\n" + \
           "{expression}\n" + \
           "}}\n"


worldcup11 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:currentTeam ?x1.\n" + \
           "  ?x1 aiball:type '俱乐部'.\n" + \
           "  ?x0 aiball:belong '比赛大名单'.\n" + \
           "  ?x0 aiball:cnName ?x2.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup12 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:currentTeam ?x1.\n" + \
           "  ?x1 aiball:type '俱乐部'.\n" + \
           "  ?x0 aiball:belong '比赛大名单'.\n" + \
           "  ?x0 aiball:cnName ?x2.\n" + \
           "  ?x0 aiball:currentTeam ?x3.\n" + \
           "{expression1}\n" + \
           "{expression2}\n" + \
           "}}\n"

worldcup13_0 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:son ?x1.\n" + \
           "  ?x0 aiball:cnName ?x2.\n" + \
           "  ?x0 aiball:belong '比赛大名单'.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup13_1 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:son ?x1.\n" + \
           "  ?x1 aiball:cnName ?x2.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup14_0 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:son ?x1.\n" + \
           "  ?x1 aiball:cnName ?x2.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup14_1 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:son ?x1.\n" + \
           "  ?x1 aiball:position ?x2.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup14_2 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:son ?x1.\n" + \
           "  ?x1 aiball:team ?x2.\n" + \
           "  ?x2 aiball:cnName ?x3.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup21 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:type '俱乐部'.\n" + \
           "  ?x1 aiball:type '俱乐部'.\n" + \
           "  ?x0 aiball:rival ?x1.\n" + \
           "  ?x2 aiball:currentTeam ?x0.\n" + \
           "  ?x3 aiball:currentTeam ?x1.\n" + \
           "  ?x2 aiball:belong '比赛大名单'.\n" + \
           "  ?x3 aiball:belong '比赛大名单'.\n" + \
           "  ?x0 aiball:cnName ?x4.\n" + \
           "  ?x1 aiball:cnName ?x5.\n" + \
           "  ?x2 aiball:currentTeam ?x6.\n" + \
           "  ?x3 aiball:currentTeam ?x6.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup22_0 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:futureWife ?x1.\n" + \
           "  ?x1 aiball:cnName ?x2.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup22_1 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:futureWife ?x1.\n" + \
           "  ?x1 aiball:link ?x2.\n" + \
           "{expression}\n" + \
           "}}\n"

worldcup24 = "SELECT DISTINCT {select} WHERE {{\n" + \
           "  ?x0 aiball:divorceNumber ?x1.\n" + \
           "{expression}\n" + \
           "}}\n"

sparql_dict = {
    k: v for k, v in locals().items() if k.startswith("worldcup")
}
