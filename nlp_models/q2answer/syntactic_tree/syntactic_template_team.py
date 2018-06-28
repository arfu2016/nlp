"""
@Project   : CubeGirl
@Module    : syntactic_template_team.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/11/17 4:21 PM
@Desc      : 
"""

from Daka.chatbot.logic.text_table.common.syntactic_model import OneTerm, \
    TwoTerms
from Daka.chatbot.logic.text_table.common.syntactic_model import \
    TemplatesInterpret


class Team1(TemplatesInterpret):
    words_involved = ['TEAM']

    def rule(self, words, arcs):
        if OneTerm(self.words_involved[0], words, arcs).hed():
            return self.class_team
        else:
            return None


class Team2(TemplatesInterpret):
    words_involved = ['TEAM', '是', '什么']
    relations_involved = [('TEAM', '是'), ('是', '什么')]

    def rule(self, words, arcs):
        relation1 = TwoTerms(self.relations_involved[0], words, arcs)
        relation2 = TwoTerms(self.relations_involved[1], words, arcs)
        # print(relation1.sbv())
        # print(relation2.vob())
        if relation1.sbv() and relation2.vob():
            return self.class_team
        else:
            return None


if __name__ == '__main__':
    temp = ['{PERSON}执教的{TEAM}', '{PERSON}所在的{TEAM}',
            '{PERSON}所在的{TEAM}是什么']
    my_team = Team1(temp)
    categories = my_team.interpret()
    print('Classification according to Team1 rule:')
    for template, intent in zip(temp, categories):
        print(template, ':', intent)
    my_team = Team2(temp)
    categories = my_team.interpret()
    print('Classification according to Team2 rule:')
    for template, intent in zip(temp, categories):
        print(template, ':', intent)
