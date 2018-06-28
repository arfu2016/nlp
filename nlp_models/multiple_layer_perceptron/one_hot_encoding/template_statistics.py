"""
@Project   : CubeGirl
@Module    : template_statistics.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/4/18 6:22 PM
@Desc      : Test file quality of template-intent pairs
"""
from collections import Counter
from Daka.chatbot.logic.knowledge_graph.one_hot_encoding.load_template import \
    load_tpl_from_xlsx

if __name__ == '__main__':
    tpl_list1 = load_tpl_from_xlsx('data/robot_template_question5.xlsx')

    tpl_list1 = [(tpl, intent) for tpl, intent in tpl_list1 if intent != 1]
    print('Number of templates having valid intentions:', len(tpl_list1))

    cnt = Counter()
    intent_list = [intent for tpl, intent in tpl_list1]
    for intent in intent_list:
        cnt[intent] += 1
    print('Number of templates in different intents:', dict(cnt))

    tpl_number = {template: number for template, number in cnt.items()
                  if number > 50}

    print('Number of templates for intents with many templates:', tpl_number)
