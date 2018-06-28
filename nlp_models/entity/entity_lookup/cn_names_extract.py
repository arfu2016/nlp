"""
@Project   : CubeGirl
@Module    : cn_names_extract.py
@Author    : Deco [deco@cubee.com]
@Created   : 4/11/18 6:31 PM
@Desc      : 
"""

from pymongo import MongoClient
import time
import pickle
import os


def get_db():
    client = MongoClient('mongodb://115.29.164.163:27081')
    db = client.robot_soccer
    return db


def find_persons():
    db = get_db()
    print('Number of players in squad collection:', db.team.find().count())

    start_t = time.time()

    projection = {"_id": 0, "cn_name": 1, "cn_first_name": 1,
                  "cn_middle_name": 1}  # , "cn_last_name": 1
    players = db.squad.find(projection=projection)
    persons = {player.get('cn_name', '') for player in players}

    print('Time to get the players: {} s'.format(time.time() - start_t))

    return list(persons)


if __name__ == '__main__':
    print('One example from squad collection:', get_db().squad.find_one(),
          '\n')
    all_persons = find_persons()
    print('Number of person names:', len(all_persons))

    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_dir, 'data/cn_names.pkl')

    with open(file_name, 'wb') as f:
        pickle.dump(all_persons, f)
