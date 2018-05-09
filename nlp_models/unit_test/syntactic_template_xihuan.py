"""
@Project   : CubeGirl
@Module    : syntactic_template_xihuan.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/11/17 1:48 PM
@Desc      : 
"""

from Daka.chatbot.logic.text_table.common.syntactic_model import TemplatesInterpret
# from .syntactic_model import TemplatesInterpret
from Daka.chatbot.logic.text_table.common.syntactic_model import TwoTerms


class Xihuan(TemplatesInterpret):
    words_involved = ['PERSON', '喜欢']
    relations_involved = [('PERSON', '喜欢'), ('喜欢', 'PERSON')]

    def rule(self, words, arcs):
        relation1 = TwoTerms(self.relations_involved[0], words, arcs)
        relation2 = TwoTerms(self.relations_involved[1], words, arcs)
        if relation1.sbv():
            return self.class_citiao
        elif relation2.vob():
            return self.class_person
        else:
            return None


if __name__ == '__main__':
    temp = ['{PERSON}喜欢什么车', '{TEAM}的{PERSON}喜欢开什么车',
            '球员{PERSON}喜欢什么车', '{PERSON}喜欢干什么',
            '我的偶像{PERSON}喜欢什么车', '我喜欢{PERSON}', '我喜欢球员{PERSON}',
            '我喜欢{TEAM}的{PERSON}', '我喜欢{TEAM}{PERSON}',
            '我喜欢老将{PERSON}', '我老板喜欢球员{PERSON}']
    # temp2 = ['我的偶像{PERSON}喜欢什么车']
    my_xihuan = Xihuan(temp)
    categories = my_xihuan.interpret()
    for template, intent in zip(temp, categories):
        print(template, ':', intent)
