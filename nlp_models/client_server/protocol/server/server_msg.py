"""
@Project   : aiball
@Module    : server_msg.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/26 14:39
@Desc      : 
"""

import uuid
import logging
from aiball.protocol.server.result_data import ResultDataFactory
from aiball.consts import ServerMsgProtocol


class ServerMsgResult:
    def __init__(self, code):
        self.answered = 1
        self.sub_code = 0
        self.seq = str(uuid.uuid1())
        self.code = int(code)
        self.data = ResultDataFactory().create(code=self.code)
        self.ssid = "0"
        self.question = None
        self.template = None
        self.intent_name = None
        self.effected_template_id = None
        self.stroy_id = None
        self.effected_regex_id = None
        self.entity_id = None
        self.broadcast = None
        self.scent = None

    def _get_method(self):
        return 1001

    def _get_power(self):
        return 2

    def str(self):
        res = {
            "method": self._get_method(),
            "status": 1,
            "answered": 1,
            "power": self._get_power(),
            "result": self.export()
        }

        return json.dumps(res, indent=4, ensure_ascii=False, sort_keys=True)

    @property
    def msg(self):
        # 2056协议因历史原因，在result层下有一个msg字段，其他协议没有
        if self.code in [ServerMsgProtocol.Fixture]:
            return self.data.msg
        return None

    @property
    def channel(self) -> int:
        return 0

    @property
    def version(self):
        return""

    @property
    def platform(self):
        return ""

    def export(self):
        ret = dict()
        try:
            # 部分协议因协议（如2048）内容中包含ssid，需以协议内容中ssid为准
            if self.data.ssid:
                self.ssid = self.data.ssid

            ret.update(self.__dict__)

            _d = self.data.export()
            ret["data"] = _d

            # 因历史原因，2056协议在result层下有一个msg字段
            ret["msg"] = self.msg

            # 删除空值字段
            keys = list(ret.keys())
            for key in keys:
                if ret[key] is None:
                    del ret[key]
        except Exception as e:
            logging.exception(e)
        return ret


if __name__ == "__main__":
    import json
    from aiball.protocol.server.result_data import DataFixtureData
    # for code in ServerMsgProtocol:
    #     try:
    #         msg = ServerMsgResult(code=code)
    #         # print("```javascript\n/**\n * code = %d(%s)\n */\n%s\n```\n\n" % (
    #         #     code, code.name, json.dumps(
    #         #         msg.export(), indent=4, ensure_ascii=False)))
    #         print("```javascript\n/**\n * code = %d(%s)\n */\n%s\n```\n\n" % (
    #             code, code.name, msg.str()))
    #     except KeyError:
    #         print("```javascript\n/**\n * code = %d(%s)\n */\n%s\n```\n\n" % (
    #             code, code.name, "{} //not support currently"))

    code = ServerMsgProtocol.FixtureEx
    msg = ServerMsgResult(code=code)
    data = DataFixtureData()
    data.home_team_id = 0
    data.home_name = "AA"
    data.match_time = ""
    data.operation = 0
    data.away_name = ""
    data.fav = 0
    data.bg = ""
    data.gms_league_id = 8
    data.status = 1
    data.away_team_id = 0
    data.league_name = "英超"
    msg.data.append(data)
    msg.data.msg = "测试比赛"
            # print("```javascript\n/**\n * code = %d(%s)\n */\n%s\n```\n\n" % (
            #     code, code.name, json.dumps(
            #         msg.export(), indent=4, ensure_ascii=False)))
    print("```javascript\n/**\n * code = %d(%s)\n */\n%s\n```\n\n" % (
        code, code.name, msg.str()))
