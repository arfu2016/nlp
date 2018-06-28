"""
@Project   : CubeGirl
@Module    : person_clean.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/12/18 10:17 AM
@Desc      : 
"""
import pickle
import os
import re

file_dir = os.path.dirname(os.path.abspath(__file__))


def get_all():

    file_name = os.path.join(file_dir, 'data/cn_names.pkl')

    with open(file_name, 'rb') as fin:
        all_persons = pickle.load(fin)

    return all_persons


def clean_person(team):

    # pattern = '^[\sa-zA-Z0-9_.-]*$'
    pattern = '[\u4e00-\u9fff]+'
    # 至少有一个汉字

    extract = re.search(pattern, team)
    if extract is not None:
        tag = True
        # span = extract.span()
        # print(span)
    else:
        tag = False
    return tag


if __name__ == '__main__':
    persons = get_all()
    persons_useful = list({person for person in persons if clean_person(person)})
    persons_useful.remove('金')

    print('Players:', persons_useful)
    print('Number of players:', len(persons_useful))
    print('内马尔在列表中:', '内马尔' in persons_useful)

    file_useful = os.path.join(file_dir, 'data/persons_useful.pkl')

    with open(file_useful, 'wb') as f:
        pickle.dump(persons_useful, f)
