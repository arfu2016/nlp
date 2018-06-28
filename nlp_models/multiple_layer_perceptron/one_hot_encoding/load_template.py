"""
@Project   : CubeGirl
@Module    : load_template.py
@Author    : Deco [deco@cubee.com]
@Created   : 11/20/17 12:21 AM
@Desc      : 从mysql或者文件中导入数据
"""

import pandas as pd


def retrieve_template(cur):
    cur.execute("SELECT * FROM robot_template_question")
    tpl_all = cur.fetchall()
    try:
        tpl_list = [(tpl[1], tpl[2]) for tpl in tpl_all]
    except IndexError:
        tpl_list = []
    return tpl_list


def load_tpl_from_csv(filename):
    df = pd.read_csv(filename)
    tpl_list = df[['template_content', 'intention_id']].values.tolist()
    tpl_intent = []
    for tpl, intent in tpl_list:
        if intent == 0:
            tpl_intent.append([tpl, 1])
        else:
            tpl_intent.append([tpl, intent])
    return tpl_intent


def load_tpl_from_xlsx(filename):
    xl = pd.ExcelFile(filename)
    print('xl.sheet_names:', xl.sheet_names)
    df = xl.parse("robot_template_question")
    tpl_list = df[['template_content', 'intention_id']].values.tolist()
    tpl_intent = []
    for tpl, intent in tpl_list:
        if intent == 0:
            tpl_intent.append([tpl, 1])
        else:
            tpl_intent.append([tpl, intent])
    return tpl_intent


if __name__ == "__main__":

    templates = load_tpl_from_csv('data/tpls.csv')
    print("Template and intention:")
    for template, intent_t in templates:
        print(template, intent_t)
