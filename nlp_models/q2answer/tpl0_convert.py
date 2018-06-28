"""
@Project   : CubeGirl
@Module    : tpl0_convert.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/15/18 1:20 PM
@Desc      : 问题之间转换的模板
"""
from .class0_convert import TemplateConvert
from .depy_relation import OneTerm


class SbvHedVobConvert(TemplateConvert):
    """鲁尼在国家队期间有什么高光时刻吗"""
    template_name = 'SbvHedVobConvert'
    words_involved = {0: ('ANY', ['SBV']), 1: ('ANY', ['ADV']),
                      2: ('ANY', ['ATT']), 3: ('ANY', ['POB']),
                      4: ('ANY', ['HED']), 5: ('ANY', ['ATT']),
                      6: (['高光时刻', '一球成名和帽子戏法'], ['VOB'])}
    relations_involved = [(4, 0), (4, 1), (4, 6), (1, 3), (6, 5), (3, 2)]
    targets_involved = [0, 1, 2, 3, 4, 5, 6]

    def convert(self, rule_target, mapping, words, arcs):
        if rule_target:
            targets_in = self.targets_involved[:-1]
            temp = [OneTerm(mapping[node], words, arcs).get_content()
                    for node in targets_in]
            # temp2 = temp.copy()
            # temp.append('一球成名')
            # temp2.append('帽子戏法')
            temp1 = [temp[0], temp[1], temp[2], temp[3], temp[4], temp[5],
                     '一球成名']
            temp2 = [temp[0], temp[1], temp[2], temp[3], temp[4], temp[5],
                     '帽子戏法']
            goal = [''.join(temp1), ''.join(temp2)]
            return goal

    @classmethod
    def generate(cls, mapping, words, arcs, results):
        temp = [OneTerm(mapping[node], words, arcs).get_content()
                for node in cls.targets_involved]
        goal = [temp[0], '的', temp[6], '包括', ': ']
        # print('results in generate() in SbvHedVobConvert in tpl0_convert:',
        #       results)
        result = '; '.join(results)
        return ''.join(goal) + result
