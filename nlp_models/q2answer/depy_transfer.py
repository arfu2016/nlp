"""
@Project   : CubeGirl
@Module    : depy_transfer.py
@Author    : Deco [deco@cubee.com]
@Created   : 2/1/18 11:57 AM
@Desc      : 
"""
import pickle
import os


def dict2list(the_dict):
    names = list(the_dict.keys())
    names.extend(list(the_dict.values()))
    return names


pkl_path = os.path.dirname(os.path.abspath(__file__))
path_relative = 'person_country_team.pkl'
with open(os.path.join(pkl_path, path_relative), 'rb') as f:
    person_transfer, country_transfer, team_transfer = pickle.load(f)
# print(person_transfer)
# print(country_transfer)
# print(team_transfer)

path_worldcup1990 = 'persons_worldcup1990.pkl'
with open(os.path.join(pkl_path, path_worldcup1990), 'rb') as f:
    persons_worldcup1990 = pickle.load(f)

# persons_worldcup1990 = persons_worldcup1990[0]

# print(persons_worldcup1990)
# print(persons_worldcup1990['马特乌斯'])

person_names = dict2list(person_transfer)
# print(person_names)
country_names = dict2list(country_transfer)
team_names = dict2list(team_transfer)

all_transfer = {**person_transfer, **country_transfer, **team_transfer}
all_names = [*person_names, *country_names, *team_names]
relation_transfer ={name: 'aiball:cnName' for name in all_names}
# print(all_transfer)
# print(relation_transfer)
# print('香川真司' in person_names)
