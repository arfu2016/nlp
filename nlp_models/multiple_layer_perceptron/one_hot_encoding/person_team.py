"""
@Project   : CubeGirl
@Module    : person_team.py
@Author    : Deco [deco@cubee.com]
@Created   : 2/1/18 10:00 AM
@Desc      : 从文件中提取球员、国家队、俱乐部的信息
"""

from collections import (Counter, namedtuple)
import pandas as pd
import pickle
import os


def name_split(the_name):
    temp = the_name.split('·')
    if len(temp) > 1:
        temp.append(''.join(temp))
    return tuple(temp)


def extract_column_persons():
    file_name = 'data/person_team.xlsx'
    xl = pd.ExcelFile(file_name)
    print('xl.sheet_names:', xl.sheet_names)
    df1 = xl.parse("参考名单")
    persons_column = df1['参考译名'].tolist()
    return persons_column


def extract_column_persons_id():
    file_name = 'data/person_team.xlsx'
    xl = pd.ExcelFile(file_name)
    print('xl.sheet_names:', xl.sheet_names)
    df1 = xl.parse("参考名单")
    persons_ids = df1[['参考译名', '数据库ID']].values.tolist()
    # first to numpy array, then to list
    return persons_ids


def extract_column_countries():
    file_name = 'data/person_team.xlsx'
    xl = pd.ExcelFile(file_name)
    df1 = xl.parse("参考名单")
    countries_column = df1['国籍'].tolist()
    return countries_column


def extract_column_teams():
    file_name = 'data/person_team.xlsx'
    xl = pd.ExcelFile(file_name)
    df1 = xl.parse("AI原始名单数据")
    countries_column = df1['球队名称'].tolist()
    return countries_column


def count_list(list_for_count):
    cnt = Counter()
    for person in list_for_count:
        cnt[person] += 1
    return cnt


def person_short_to_name():
    persons = extract_column_persons()

    cnt_person = count_list(persons)
    print('Most common person names:', cnt_person.most_common(5))
    person_names = list(cnt_person.keys())
    print('Number of person names:', len(person_names))

    person_dict = {name_split(person): person for person in person_names}
    short_list = list(person_dict.keys())
    short_names = [name for short in short_list for name in short]
    # short_names = []
    # for short in short_list:
    #     short_names.extend(short)
    # 注意是extend, 不是append

    cnt_s_names = count_list(short_names)
    unique_names = [name for name, num in cnt_s_names.items() if num == 1]
    person_mapping = {tuple(set(short).intersection(set(unique_names))): name
                      for short, name in person_dict.items()}

    name_transfer = dict()
    for shorts, name in person_mapping.items():
        for short in shorts:
            name_transfer.update({short: name})
    print('name_transfer needed:', name_transfer)
    print('length of name_transfer:', len(name_transfer))
    return name_transfer


def person_ids():
    persons_ids = extract_column_persons_id()
    persons, _ = zip(*persons_ids)
    cnt_person = count_list(persons)
    unique_p_names = [name for name, num in cnt_person.items() if num == 1]
    persons_ids_u = {person: pid for person, pid in persons_ids
                     if person in unique_p_names}
    persons_ids_output = dict()
    for person, pid in persons_ids_u.items():
        if pid == '无':
            persons_ids_output[person] = 0
        else:
            persons_ids_output[person] = pid
    print(persons_ids_output)
    print('Number of persons:', len(persons_ids_output))
    return persons_ids_output


def country_names():
    countries = extract_column_countries()
    countries = list(set(countries))
    country_transfer = dict()
    for country in countries:
        country_transfer.update({country + '队': country})
        country_transfer.update({country + '国家队': country})
    print('country_transfer needed:', country_transfer)
    return country_transfer


def club_names():
    teams = extract_column_teams()
    teams = list(set(teams))
    team_transfer = {team + '队': team for team in teams}
    print('team_transfer needed:', team_transfer)
    return team_transfer


'''
https://stackoverflow.com/questions/4677012/python-cant-pickle-type-x-attribute-lookup-failed?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa#comment5155907_4677063
def main():
    Sport = namedtuple('Sport', ['person', 'country', 'team'])
    # 类工厂函数，生产一个类
    football_name = Sport(person_short_to_name(),
                          country_names(), club_names())
    print(isinstance(football_name, object))
    print(isinstance(football_name, type))
    print(isinstance(Sport, type))
    football_id = Sport(person_ids(), country_names(), club_names())
    file_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(file_dir, 'data/pct180326.pkl')
    with open(filename, 'wb') as f:
        pickle.dump(football_name, f)
'''

Sport = namedtuple('Sport', ['person', 'country', 'team'])
# 类工厂函数，生产一个类
football_name = Sport(person_short_to_name(),
                      country_names(), club_names())
football_id = Sport(person_ids(), country_names(), club_names())


if __name__ == '__main__':
    filename = 'data/pct180326.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(football_name, f)
    print('football_name:', football_name)
