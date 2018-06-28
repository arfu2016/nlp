"""
@Project   : CubeGirl
@Module    : re_ne.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/8/18 1:26 PM
@Desc      : 
"""
import re
from collections import defaultdict
from .patterns_extract import team_patterns


def ne_extract_re(pa, st):

    extract = re.search(pa, st)
    if extract is not None:
        tag = True
        # span = extract.span()
        # print(span)
    else:
        tag = False
    return tag


def extract_patterns(patterns, st):
    teams = defaultdict(list)

    for pa in patterns:
        if ne_extract_re(pa, st):
            teams[st].append(pa)
    return teams


def test_re_ne():

    sentences = [
        '梅西效力于巴塞罗那, C罗不效力于巴塞罗那',
        'C罗效力于皇马',

    ]
    teams = dict()

    for st in sentences:
        teams.update(extract_patterns(team_patterns, st))

    print(teams)
