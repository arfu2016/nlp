"""
@Project   : aiball
@Module    : credis.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/14 13:34
@Desc      : 
"""
import hashlib
import json
import logging
import time
from urllib.parse import urlencode

import redis

from aiball import conf as config
from aiball.utils import singleton


class RedisConnect:
    def __init__(self, _redis="redis"):
        self.host = config.server_config_get(_redis + ".host")
        self.port = config.server_config_get(_redis + ".port")
        self.password = config.server_config_get(_redis + ".password")
        self.db = redis.StrictRedis(host=self.host,
                                    port=self.port,
                                    decode_responses=True,
                                    password=self.password,
                                    socket_keepalive=True)

    def select_db(self, _db: int):
        self.db.execute_command("SELECT", _db)


@singleton
class RedisLog(RedisConnect):
    """
    这个类用于封记录日志到redis中的功能
    """

    def __init__(self, _redis="redis"):
        super().__init__(_redis=_redis)
        self.channel = config.server_config_get("channel.log")

    def log(self, res: dict):
        try:
            _value = dict()
            _value["code"] = str(res["result"]["code"])
            _value["msg"] = res["result"]["data"]["msg"]
            _value["answered"] = str(res["result"]["answered"])
            _value["ssid"] = str(res["result"]["ssid"])
            _value["question"] = res["result"]["question"]
            _value["method"] = str(res.get("method", ""))
            _value["status"] = str(res.get("status", ""))
            _value["server"] = str(res.get("server", ""))
            _value["version"] = str(res.get("result", {}).get("version", ""))
            _value["platform"] = str(res.get("result", {}).get("platform", ""))
            _value["intent_marks"] = str(res.get("intent_marks", ""))
            _value["entity_id"] = str(
                res.get("result", {}).get("entity_id", ""))
            _value["with_story"] = int(
                res.get("result", {}).get("with_story", 0))
            _value["story_id"] = str(
                res.get("result", {}).get("story_id", "0"))
            _value["channel"] = str(res.get("result", {}).get("channel", "0"))
            _value["sub_code"] = str(
                res.get("result", {}).get("sub_code", "0"))
            _value["template"] = str(res.get("result", {}).get("template", ""))
            _value["intent_name"] = str(
                res.get("result", {}).get("intent_name", ""))
            _value["effected_regex_id"] = str(
                res.get("result", {}).get("effected_regex_id", ""))
            _value["effected_template_id"] = str(
                res.get("result", {}).get("effected_regex_id", ""))
            _value["platform"] = str(
                res.get("result", {}).get("platform", "0"))

            _user = res.get("user", list())
            _idfas = res.get("idfa", list())

            if _user and isinstance(_user, list):
                _value["uid"] = _user[0]
            if _idfas and isinstance(_idfas, list):
                _value["idfa"] = _idfas[0]
            _value["time"] = int(time.time())
            self.db.rpush(self._channel,
                          json.dumps(_value, ensure_ascii=False))
        except Exception as e:
            logging.exception(e)

    def get(self):
        ret = dict()
        try:
            ret = json.loads(self.db.rpop(self._channel))
        except Exception as e:
            logging.exception(e)
        finally:
            return ret


@singleton
class RedisBuffer(RedisConnect):
    """
    这个redids封装用于给数据库查询作缓存
    """

    def __init__(self, _redis="redis"):
        super().__init__(_redis=_redis)
        self.channel = config.server_config_get("channel.buffer")

    def save(self, value, ex: int, **kwargs) -> bool:
        try:
            _keys = urlencode(kwargs)
            key = hashlib.md5(_keys.encode()).hexdigest()
            self.db.set(name=self.channel + key, value=str(value), ex=ex)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    def get(self, **kwargs):
        _value = None
        try:
            _keys = urlencode(kwargs)
            key = hashlib.md5(_keys.encode()).hexdigest()
            _value = self.db.get(name=self.channel + key)
            if _value:
                _value = eval(_value)
        except NameError:
            logging.warning("被装饰函数返回为字符串，不应该使用当前装饰器")
        except SyntaxError:
            logging.warning("被装饰函数返回为字符串，不应该使用当前装饰器")
        except Exception as e:
            logging.exception(e)
        finally:
            return _value


def redis_cache(ex: int):
    def _ins(fun: callable):
        def wrapper(*args, **kwargs):
            _redis = RedisBuffer()
            value = _redis.get(**kwargs)
            if not value:
                try:
                    value = fun(*args, **kwargs)
                except Exception as e:
                    logging.exception(
                        "函数%s出错，请在函数内部处理该异常: %s" % (fun.__name__, str(e)))
                if value:
                    _redis.save(value=value, ex=ex, **kwargs)
            return value

        return wrapper

    return _ins


@singleton
class RedisConsumer(RedisConnect):
    """
    用于消费数据缓存队列
    """

    def __init__(self, _redis="redis_gate", timeout=0.001):
        super().__init__(_redis=_redis)
        self.channel_r = config.server_config_get("channel.receive")
        self.channel_s = config.server_config_get("channel.send")
        self.channel_c = config.server_config_get("channel.chat")
        self._connect_check_flag = "cubee_gire_redis_consumer_connect_flag"
        self._last_check_time = 0
        self.db.setnx(name=self._connect_check_flag, value=1)
        self.timeout = timeout

    def _check_and_reconnect(self):
        """
        断线重连
        :return:
        """

        def _reconnect_current_redis():
            self.__init__()
            logging.warning(
                "**********  re-connect redis:%d  ****" % int(time.time()))

        def _check_current_connect_status() -> bool:
            if self.db:
                if self.db.get(self._connect_check_flag):
                    return True
            return False

        if time.time() - self._last_check_time > 60:
            if not _check_current_connect_status():
                _reconnect_current_redis()
            self._last_check_time = time.time()

    def send(self, value):
        """
        发送消息给用户
        :param value: 需要发送到的值
        """

        def _send(_value: dict):
            try:
                if not _value:
                    return
                msg = json.dumps(_value, ensure_ascii=False)
                res = self.db.publish(self.channel_s, msg)
                logging.debug(msg="发送消息(%s)结果: %d" % (msg, res))
            except Exception as e:
                logging.exception(e)

        if isinstance(value, list):
            for v in value:
                if not isinstance(v, dict):
                    continue
                self._send(value=v)
        elif isinstance(value, dict):
            self._send(value=value)
        else:
            logging.debug("需要发送的数据类型不正确: %s" % str(value))

    def get(self):
        """
        从用户消息队列中获取用户消息
        :return:
        """
        while True:
            try:
                msg = self.db.rpop(self.channel_r)
                if not msg:
                    self._check_and_reconnect()
                    time.sleep(self.timeout)
                    continue
                yield msg
            except Exception as e:
                logging.exception(e)
                time.sleep(self.timeout)

    def save(self, data: dict):
        """
        保存聊天消息到redis队列中
        :param data: 需要保存的数据
        :return:
        """
        try:
            _data = json.dumps(data, ensure_ascii=False)
            self.db.lpush(self.channel_c, _data)
        except Exception as e:
            logging.exception(e)

    def receive(self, ignore_error=False):
        """
        从redis队列中接收闲聊信息
        :param ignore_error: 是否忽略错误
        :return:
        """
        while True:
            try:
                msg = self.db.rpop(self.channel_c)
                if not msg:
                    self._check_and_reconnect()
                    time.sleep(self.timeout)
                    continue

                data = json.loads(msg.replace("'", "\""))
                yield data
            except Exception as e:
                logging.exception(e)


@singleton
class RedisIntent(RedisConnect):
    """
    封装机器人语意理解时存储上下文关系的redis
    """

    def __init__(self, _redis="redis"):
        super().__init__(_redis=_redis)
        _db = config.server_config_get("db.redis.intent")
        self._expire = config.server_config_get("expire.redis.intent")
        self.select_db(_db)

    def intent_save(self, idfa: str, value: dict) -> int:
        """
        存储上下文关系到redis中
        :param idfa: 需要存储的上下文关系的用户的idfa值
        :param value: 需要存储的上下文关系
        :return: 返回当前用户存储的上下文关系数量
        """
        try:
            _len = self.db.rpush(idfa, json.dumps(value, ensure_ascii=False))
            self.db.expire(idfa, self._expire)

            return _len
        except Exception as e:
            logging.exception(3)
            return 0

    def intent_fetch(self, idfa: str, index: int = -1) -> dict:
        """
        获取指定用户上下文关系
        :param idfa: 批指定用户idfa
        :param index: 需要获取的上下文关系编号，-1为最后一个
        :return: 返回index指定的上下文关系字典。如果未找到，返回空字典
        """
        try:
            _value = self.db.lindex(name=idfa, index=index)
            if _value:
                return json.loads(_value.replace("None", "null"))
        except Exception as e:
            logging.exception(e)
            return {}


@singleton
class RedisReceiveEvent(RedisConnect):
    """
    用于消费数据缓存队列
    """

    def __init__(self, _redis="redis_gate", timeout=0.001):
        super().__init__(_redis=_redis)
        self.subscribe = self.db.pubsub().subscribe(
            config.server_config_get("channel.event"))
        self.on_data = None

    def receive(self, timeout=0.001, ignore_error=False):
        """
        开始接收事件，函数运行前，必须先设定on_data回调函数
        """

        def _on_data(d: str):
            logging.info("接收到事件：%s" % str(d))
            if ignore_error:
                try:
                    self.on_data(d)
                except Exception as e:
                    logging.exception(e)
            else:
                self.on_data(d)

        while True:
            try:
                msg = self.subscribe.get_message(True, timeout=0.1)
                if not msg:
                    time.sleep(timeout)
                    continue
                if msg.get("type", "") != "message":
                    continue
                data = msg.get("data")
                if data:
                    _on_data(data)
            except Exception as e:
                logging.exception(e)


if __name__ == "__main__":
    @redis_cache(20)
    def test_value(db=1, collection=2):
        return "time: %d, db: %d, collection: %d" % (
            int(time.time()), db, collection)


    for _ in range(5):
        print(test_value())
        time.sleep(5)
