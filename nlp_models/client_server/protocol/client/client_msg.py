"""
@Project   : aiball
@Module    : client_msg.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/21 13:42
@Desc      : 
"""

import logging
from aiball.consts import ClientMsgProtocol
from aiball.protocol.client.parameter import Parameter
from aiball.protocol.client.parameter import ParameterFactory


class ClientMsgData:
    support_code = [int(x) for x in ClientMsgProtocol]

    def __init__(self):
        self.code = 0
        self.ssid = 0
        self.idfa = ""
        self.version = "0.0"
        self.platform = "ios"
        self.uid = 0
        self.source = ""
        self.param = Parameter()
        self._error = ""

    def load(self, _src: dict):
        try:
            self.code = int(_src["code"])
            self.idfa = str(_src["idfa"])
            self.version = str(_src["version"])
            self.version = "%.2f" % float(_src["version"])
            self.ssid = int(_src.get("ssid", 0))
            self.platform = str(_src["platform"])
            self.uid = int(_src.get("uid"))
            self.param = ParameterFactory().create(self.code)
            self.param.load(src=_src.get("param", {}))
        except (KeyError, ValueError, TypeError) as e:
            logging.error(e)
            self._error = str(e)

        return self

    def dump(self):
        return {
            "ssid": self.ssid,
            "idfa": self.idfa,
            "version": self.version,
            "platform": self.platform,
            "param": self.param.dump(),
            "uid": self.uid,
            "code": self.code,
            "source": self.source
        }

    def valid(self):
        return self.code in self.support_code \
               and self._error == "" and self.param.valid()

    def ack(self):
        return self.param.ack()

    def button_type(self) -> int:
        return self.param.button_type()

    def content_pool_id(self) -> int:
        return self.param.content_pool_id()

    def entity_id(self) -> int:
        return self.param.entity_id()

    def entity_type(self) -> int:
        return self.param.entity_type()

    def type(self):
        return self.param.type()

    def idx(self) -> int:
        return self.param.idx()

    def res(self):
        return self.param.res()

    def msg(self):
        return self.param.msg()

    def match(self):
        return self.param.match()