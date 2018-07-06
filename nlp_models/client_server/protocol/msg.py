"""
@Project   : aiball
@Module    : msg.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/28 12:14
@Desc      : 
"""

import json
import logging
from aiball.consts import ErrorCode
from aiball.consts import ServerMsgMethodCode as Method
from aiball.protocol.client.client_msg import ClientMsgData
from aiball.protocol.server.result_data import DataItem
from aiball.protocol.server.server_msg import ServerMsgResult


class ClientMsg:
    def __init__(self):
        self.user = 0
        self.gate_idfa = "gateway"
        self.data = ClientMsgData()

    def deserialize(self, src: str) -> int:
        """
        返序列化，加载从客户端收到的协议消息
        :param src: 客户端收到的原始协议消息
        :return:
        """
        try:
            _src = json.loads(src.replace("'", "\"").replace("。", ""))
            self.user = str(_src["user"])
            self.gate_idfa = _src["idfa"]
            self.data.load(_src=_src.get("data", {}))
        except Exception as e:
            logging.exception("接收客户端消息参数误：", e)
            return ErrorCode.ERROR_USER_PARAMETER

        return ErrorCode.ERROR_PASS

    def serialize(self):
        """
        序列化，将客户端协议从class转换成字符串
        :return:
        """
        try:
            data = {
                "idfa": self.idfa,
                "user": self.user,
                "data": self.data.dump()
            }
            return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            logging.exception(e)
            return "{}"

    def valid(self):
        return self.data.valid()

    @property
    def ssid(self):
        return self.data.ssid

    @property
    def idfa(self):
        return self.data.idfa

    @property
    def version(self):
        return self.data.version

    @property
    def platform(self):
        return self.data.platform

    @property
    def uid(self):
        return self.data.uid

    @property
    def source(self):
        return self.data.source

    @property
    def code(self):
        return self.data.code

    @property
    def msg(self):
        return self.data.param.msg()

    @property
    def ack(self):
        return self.data.param.ack()

    @property
    def res(self):
        return self.data.param.res()

    @property
    def idx(self):
        return self.data.param.idx()

    @property
    def type(self):
        return self.data.param.type()

    @property
    def content_pool_id(self):
        return self.data.param.content_pool_id()

    @property
    def entity_id(self) -> int:
        return self.data.param.entity_id()

    @property
    def entity_type(self) -> int:
        return self.data.param.entity_type()

    @property
    def button_type(self) -> int:
        return self.data.param.button_type()


class ServerMsg:
    def __init__(self, code):
        self.idfa = list()
        self.user = list()
        self.intent_marks = list()
        self.status = 0
        self.result = ServerMsgResult(int(code))
        self.server = 90000
        self.method = Method.Normal

    def append(self, item: DataItem):
        self.result.data.append(item)

    def serialize(self):
        r = self.result.export() if self.result else {}
        return {
            "server": self.server,
            "method": self.method,
            "user": self.user,
            "idfa": self.idfa,
            "intent_marks": self.intent_marks,
            "status": self.status,
            "result": r
        }


if __name__ == "__main__":
    for code in [1025, 2000, 2049, 2051, 2055, 2056, 4096, 4097, 4099]:
        s = ServerMsg(code)
        print("protocal_%d = %s\n\n" % (code,json.dumps(
            s.serialize(), ensure_ascii=False, indent=4)))
        s.result.data.msg = "1111"
