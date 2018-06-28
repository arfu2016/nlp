#!/usr/bin/env python3

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('/home/deco/projects/cupro/CubeGirl/SourceCode')

from Daka.robot.base.redis_api import RedisAPI
from Daka.robot.database.mysql import Mysql
from Daka.robot.utils.conf import UtilConf
from Daka.robot.const.common import TPL_MYSQL_KEY
from Daka.robot.const.sql import SQL_CONTEXT_TPL_SAVE, SQL_TEXT_TPL_SAVE


def corpus_get(redis_cor, batch_size):
    temp = redis_cor.lrange('deco:corpus', 0, batch_size-1)
    item = [eval(ele) for ele in temp]
    return item


def transfer_redis_to_mysql(redis_cor, db, cur):
    batch_size = 1000
    batch_times = redis_cor.llen('deco:corpus')//batch_size+1
    gen_cor = (corpus_get(redis_cor, batch_size) for _ in range(batch_times))

    for many_items in gen_cor:
        tpl_intent = {item[2]:item[3] for item in many_items}
        tpl_name_string = '("'+','.join(tpl_intent.keys())+'")'
        intent_name_string='("'+','.join(tpl_intent.values())+'")'
        try:
            cur.execute("""SELECT id FROM robot_template_intention 
                WHERE intention_name IN {}""".format(intent_name_string))
            intent_all = cur.fetchall()
            intent_list = [intent[0] for intent in intent_all]
            tpl_intent2 = zip(tpl_intent.keys(), intent_list)
            cur.executemany(
                SQL_CONTEXT_TPL_SAVE, tpl_intent2
            )

            cur.execute("""SELECT id FROM robot_template_question
                WHERE template_content IN {}""".format(tpl_name_string))
            tpl_all = cur.fetchall()
            tpl_list = [tpl[0] for tpl in tpl_all]
            tpl_id = {key: value for key, value in zip(tpl_intent.keys(),
                                                       tpl_list)}
            for item in many_items:
                if "{" not in item[2] or "}" not in item[2]:
                    item[2] = None
                else:
                    item[2] = tpl_id[item[2]]
            many_items = [[item[0],item[1],item[2],item[4],item[5]]
                          for item in many_items]
            cur.executemany(
                SQL_TEXT_TPL_SAVE, many_items
            )
        except Exception as e:
            print("插入template/text失败！ Error:", str(e))
            break
        batch_times -= 1
        if batch_times>0:
            redis_cor.ltrim('deco:corpus', batch_size, -1)
        else:
            redis_cor.delete('deco:corpus')
            # print('delete deco:corpus')
    db.commit()
    cur.close()
    db.close()

    print('Transferring from redis to mysql was finished.')


if __name__=='__main__':
    redis_corpus = RedisAPI()
    params_tpl_mysql = UtilConf()[TPL_MYSQL_KEY]
    mysql = Mysql(**params_tpl_mysql)
    transfer_redis_to_mysql(redis_corpus._redis, mysql.conn, mysql.cursor)

# crontab /home/deco/projects/cupro/CubeGirl/SourceCode/Daka/chatbot/logic/text_table/crontab.txt
# to test locally
