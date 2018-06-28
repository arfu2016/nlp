"""
@Project   : CubeGirl
@Module    : team_clean.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/10/18 11:16 AM
@Desc      : 
"""

import pickle
import os
import re

file_dir = os.path.dirname(os.path.abspath(__file__))


def get_all():

    file_name = os.path.join(file_dir, 'data/teams.pkl')

    with open(file_name, 'rb') as f:
        all_teams = pickle.load(f)

    return all_teams


def clean_team(team):

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
    teams = get_all()
    teams_useful = list({team for team in teams if clean_team(team)})
    teams_useful.remove('巴')

    print('Teams:', teams_useful)
    print('Number of teams:', len(teams_useful))
    print('AC米兰在列表中:', 'AC米兰' in teams_useful)

    file_useful = os.path.join(file_dir, 'data/teams_useful.pkl')

    with open(file_useful, 'wb') as f:
        pickle.dump(teams_useful, f)
