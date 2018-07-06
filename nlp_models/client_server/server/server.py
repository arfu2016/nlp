import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
from public_api.cg_api import *
from db import *
from constants.constants_common import CONFIG as config
import json
import threading
from Daka.chatbot.logic.chatbot import Chatbot as ChatbotNew
from public.interface import nlg_update_from_mysql
from public.interface import tick_start
from public.interface import cmd_start_listen
from public.interface import cmd_register_function


def init_logging(pid: int=0):
    _level = config["logging"]["level"]
    _f = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    _d = '%a, %d %b %Y %H:%M:%S'
    _file = "CubeGirl_%s_%d.log" % (time.strftime("%Y-%m-%d %H%M%S"), pid)
    logging.basicConfig(level=_level,
                        format=_f,
                        datefmt=_d,
                        filename=_file,
                        filemode="w")


class ServerKernel:
    def __init__(self):
        self.protocol_codes = [257, 258, 272, 273, 274, 275, 277, 278]
        self.redis_chat = RedisReceiveChatMsg()
        self.robot_new = ChatbotNew()

    def _get_protocol_code(self, message: dict) -> (int, bool):
        """
        获取消息的protocol代码
        :param message:
        :return:
        """
        if message:
            data = message.get("data", {})
            if data:
                code = data.get("code", 0)
                if code in self.protocol_codes:
                    return code, True

        logging.debug("无效msg，msg中未找到data或msg.data中未找到有效code")
        return 0, False

    def process_message_new(self, message: dict) -> dict:
        """
        处理用户发送过来消息
        :param message: 用户发送过来的消息
        :return: 返回机器人处理后的消息字典或空字典
        """

        ret = {}
        code, res = self._get_protocol_code(message=message)
        if not res:
            return ret

        try:
            if code in [273, 274, 277, 278]:
                ret = self.robot_new.process(data=message)
        except Exception as e:
            logging.exception(e)

        return ret


class Server:
    def __init__(self):
        self.redis_send = RedisPublish()
        self.redis_log = RedisLog()
        self.redis_message = RedisConsumer()
        self.processes = list()
        self.server_kernel = ServerKernel()

    @staticmethod
    def prepare_actions():
        # 开启Tick线程，以tick推动定时执行的函数
        tick_start()

        # 注册更新话述函数，开启监听管理后台服务
        cmd_register_function(fun=nlg_update_from_mysql, cmd="UPDATE", name="TERM")
        cmd_start_listen()

        # 开启缓存
        RedisBufferForDB()
        nlg_update_from_mysql()

    def _do_consume(self):
        def _do_process_msg(_msg: str):
            print(_msg)
            _message = json.loads(_msg.replace("'", "\"").replace("。", ""))
            # 临时修改方案：客户端有可能传空字符串作为ssid，强行转换为整型
            if "data" in _message:
                if "ssid" in _message["data"]:
                    if _message["data"]["ssid"] == "":
                        _message["data"]["ssid"] = 0
                if "param" in _message["data"]:
                    if "idx" in _message["data"]["param"]:
                        if _message["data"]["param"]["idx"] != "":
                            _message["data"]["param"]["idx"] = int(_message["data"]["param"]["idx"])
                        else:
                            _message["data"]["param"]["idx"] = 0

            ret = self.server_kernel.process_message_new(_message)

            if isinstance(ret, list):
                for r in ret:
                    self.redis_send.send(r)
                    self.redis_log.log(r)
            elif isinstance(ret, dict):
                self.redis_send.send(ret)
                self.redis_log.log(ret)

        for msg in self.redis_message.get():
            try:
                _do_process_msg(_msg=msg)
            except KeyboardInterrupt as e:
                logging.warning("exit by user")
                break
            except Exception as e:
                logging.exception(e)
                continue

    def start(self):
        """
        处理用户消息进程，消费src指定的队列中的消息，处理过后的结果存入dst中
        """
        self.prepare_actions()
        print("Server (%d) started, waiting data..." % os.getpid())
        thread_list = list()
        for _ in range(5):
            thread_consume = threading.Thread(target=self._do_consume)
            thread_list.append(thread_consume)
            thread_consume.start()

        for t in thread_list:
            t.join()


if __name__ == "__main__":
    try:
        init_logging(pid=os.getpid())
        s = Server()
        s.start()
    except KeyboardInterrupt as e:
        logging.warning("exit by user")
    except Exception as e:
        logging.error(str(e))
