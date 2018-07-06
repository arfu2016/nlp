"""
@Project   : aiball
@Module    : parameter.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/28 12:23
@Desc      : 
"""

from aiball.utils.decorators import singleton


class Parameter:
    """
    客户端消息参数接口
    """
    protocol = 0

    def valid(self):
        return False

    def ack(self):
        return ""

    def button_type(self) -> int:
        return -1

    def content_pool_id(self) -> int:
        return 0

    def entity_id(self) -> int:
        return 0

    def entity_type(self) -> int:
        return 0

    def type(self):
        return ""

    def idx(self) -> int:
        return -1

    def res(self):
        return 0

    def msg(self):
        return ""

    def match(self):
        return 0

    def load(self, src: dict):
        pass

    def dump(self) -> dict:
        return dict()


class ParameterConnectMatch(Parameter):
    protocol = 272

    def __init__(self):
        self._match = 0

    def dump(self) -> dict:
        return {
            "match": self._match
        }

    def load(self, src: dict):
        self._match = int(src["match"])

    def match(self):
        return self._match

    def valid(self):
        return self._match > 0


class ParameterNormalTextMsg(Parameter):
    """
    封装客户端273协议中param

    _msg为客户端发送过来的消息内容，字符串类型
    """
    protocol = 273

    def __init__(self):
        self._msg = ""
        self._button_type = -1
        self._content_pool_id = 0
        self._entity_id = 0
        self._entity_type = 0
        self._ack = ""

    def dump(self) -> dict:
        return {
            "msg": self._msg
        }

    def load(self, src: dict):
        self._msg = src["msg"]
        self._button_type = int(src.get("button_type", -1))
        self._content_pool_id = int(src.get("content_pool_id", 0))
        self._entity_id = int(src.get("entity_id", 0))
        self._entity_type = int(src.get("entity_type", 0))
        self._ack = str(src.get("ack", ""))

    def ack(self) -> str:
        return self._ack

    def button_type(self) -> int:
        return self._button_type

    def content_pool_id(self) -> int:
        return self._content_pool_id

    def entity_id(self) -> int:
        return self._entity_id

    def entity_type(self) -> int:
        return self._entity_type

    def msg(self) -> str:
        return self._msg

    def valid(self) -> bool:
        return self._msg != ""


class ParameterUserSelectAskBack(Parameter):
    protocol = 277

    def __init__(self):
        self._ack = ""
        self._idx = 5
        self._type = ""

    def dump(self) -> dict:
        return {
            "ack": self._ack,
            "idx": self._idx,
            "type": self._type,
        }

    def load(self, src: dict):
        self._ack = str(src["ack"])
        self._idx = int(src["idx"])
        self._type = str(src["type"])

    def ack(self):
        return self._ack

    def idx(self):
        return self._idx

    def type(self):
        return self._type

    def valid(self) -> bool:
        return self._idx >= 0


@singleton
class ParameterFactory:
    _support_parameter_implement = [
        ParameterConnectMatch,  # 272 连接一场比赛
        ParameterNormalTextMsg,  # 273 用户消息
        ParameterUserSelectAskBack,  # 277 追问用户选择
    ]

    _protocol_table = dict()

    def __new__(cls):
        cls._protocol_table = dict()
        for parameter in cls._support_parameter_implement:
            code = parameter.protocol
            cls._protocol_table[code] = parameter
        return cls

    @classmethod
    def create(cls, code: int) -> Parameter:
        """
        生产code对应的Parameter类
        :param code: 协议号，code值不支持会抛出KeyError
        :return:
        """
        return cls._protocol_table[int(code)]()
