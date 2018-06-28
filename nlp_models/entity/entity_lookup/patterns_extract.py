"""
@Project   : CubeGirl
@Module    : patterns_extract.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/8/18 1:57 PM
@Desc      : 
"""
from pymongo import MongoClient
import time
import pickle
import os

team_patterns = ['巴塞罗那', '巴萨', '皇马']

# client = MongoClient('mongodb://blt:5vYLdYvH@dds-bp11b8be4f6beec42.mongodb.
# rds.aliyuncs.com:3717/robot_soccer')


def get_db():
    client = MongoClient('mongodb://115.29.164.163:27081')
    db = client.robot_soccer
    return db


def find_teams():
    db = get_db()
    print('Number of teams in team collection:', db.team.find().count())

    start_t = time.time()

    projection = {"_id": 0, "cn_club_name": 1}
    teams = db.team.find(projection=projection)
    clubs = [team["cn_club_name"] for team in teams]

    print('Time to get the clubs: {} s'.format(time.time() - start_t))

    return clubs


if __name__ == '__main__':
    print('One example from team collection:', get_db().team.find_one(), '\n')

    all_teams = find_teams()

    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_dir, 'data/teams.pkl')

    with open(file_name, 'wb') as f:
        pickle.dump(all_teams, f)

    # i = 0
    # for a in db.team.find():
    #     print(a)
    #     if i > 3:
    #         break
    #     i += 1
