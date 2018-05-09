"""
@Project   : CubeGirl
@Module    : test_syntactic_template.py
@Author    : Deco [deco@cubee.com]
@Created   : 12/11/17 3:42 PM
@Desc      : 
"""

import unittest

from Daka.chatbot.logic.text_table.syntactic_tree.syntactic_template_team import \
    Team1, Team2
from Daka.chatbot.logic.text_table.syntactic_tree.syntactic_template_xihuan import \
    Xihuan


class TestTemplate(unittest.TestCase):
    def test_Xihuan(self):
        temp = ['{PERSON}喜欢什么车', '{TEAM}的{PERSON}喜欢什么车',
                '球员{PERSON}喜欢什么车', '我的偶像{PERSON}喜欢什么车',
                '{PERSON}喜欢干什么', '我喜欢{PERSON}', '我喜欢球员{PERSON}',
                '我喜欢{TEAM}的{PERSON}', '我喜欢{TEAM}{PERSON}',
                '我喜欢老将{PERSON}', '我老板喜欢球员{PERSON}']
        results = ['citiao'] * 5 + ['person_info'] * 6
        my_xihuan = Xihuan(temp)
        categories = my_xihuan.interpret()
        self.assertEqual(categories, results)

    def test_Team1(self):
        temp = ['{PERSON}执教的{TEAM}', '{PERSON}所在的{TEAM}']
        results = ['team_info'] * 2
        my_team = Team1(temp)
        categories = my_team.interpret()
        self.assertEqual(categories, results)

    def test_Team2(self):
        temp = ['{PERSON}所在的{TEAM}是什么']
        results = ['team_info'] * 1
        my_team = Team2(temp)
        categories = my_team.interpret()
        self.assertEqual(categories, results)


if __name__ == '__main__':
    unittest.main()
