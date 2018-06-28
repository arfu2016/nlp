"""
@Project   : CubeGirl
@Module    : depy_sparql_connect.py
@Author    : Deco [deco@cubee.com]
@Created   : 1/22/18 11:28 AM
@Desc      : 
"""
from SPARQLWrapper import SPARQLWrapper, JSON


class ConnectKb:
    def __init__(self):
        # sparql = SPARQLWrapper("http://192.168.10.2:5820/test1/query")
        # self.sparql.setCredentials(user="admin", passwd="admin")
        # self.sparql = SPARQLWrapper("http://120.27.193.124:5820/test0/query")
        # self.sparql = SPARQLWrapper(
        #     "http://120.27.193.124:5820/sammer_test1/query")
        self.sparql = SPARQLWrapper(
            "http://120.27.193.124:5820/WorldCup_test/query")
        # self.sparql = SPARQLWrapper(
        #     "http://120.27.193.124:5820/sammer_test3/query")
        self.sparql.setCredentials(user="admin", passwd="cubee")
        self.sparql.setReturnFormat(JSON)


connect = ConnectKb()
# 单例
sparql = connect.sparql
