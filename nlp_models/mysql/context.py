"""
用于管理上下文的类
"""
import copy
from datetime import datetime

from Daka.robot.utils.conf import UtilConf
from Daka.robot.utils.nlp import sentence_standardizing
from Daka.robot.const.common import REDIS_CONTEXT_PREFIX, \
    TPL_MYSQL_KEY, CONTEXT_STATUS_NAMES, CONTEXT_EXPIRE
from Daka.robot.const.intent import DEFAULT_INTENT_NAME
from Daka.robot.database.mysql import Mysql
from Daka.robot.const.sql import SQL_CONTEXT_TPL_SAVE
from Daka.robot.base.redis_api import RedisAPI
from Daka.robot.const.intent import NON_TOPIC_INTENTS, INTENTS_HAVE_CONFIRM


class Context(RedisAPI):

    _redis = None
    _params_tpl_mysql = UtilConf()[TPL_MYSQL_KEY]

    def __init__(self, user_id, idfa, match_id, msg, scene_id=None):
        """
        :param data: gateway->robot数据，code 273
        
        状态属性self.status为字典变量，每个key对应不同的状态类别：
        1. normal---暂不使用:
          0-正常状态;
          1-询问状态;
          
        2. status_to_confirm:
          0-未激活状态；1-激活状态
          进行“是或否”追问，需要得到确定性或否定性回复

        3. status_to_choose:
          0-未激活状态；1-激活状态
          进行"选择"追问，需要用户在给出的选择数据中做出选择
          
        4. status_wanna_next:
          0-未激活状态；1-激活状态
          has_next时，询问是否继续需要
          
        注意：
            1.意图名称中有to_confirm和to_choose意图，这里的status_to_confirm和
              status_to_choose是分别执行了to_confirm和to_choose意图后的状态；
            2.对于提供has_next结果的意图处理函数，当has_next为True时，进入
              status_wanna_next状态。

        关于intent_name, topic的说明：
        1. 
        2. intent_name为根据当前对于语句分析得到的意图，不考虑上下文和参数情况，
           是纯粹字面上的意图；
        3. topic是来自字面的、正在进行中的意图---提取自字面意图，但并非所有的
           字面意图都可以做为topic。

        每次执行意图处理，都是按照intent_name进行处理，意图完成后将topic中的
        finished修改为1，若未完成处理则继续保持原来的值0。
        """
        self._init_redis()
        # 基本的信息
        self.user_id = user_id
        self.idfa = idfa
        self.match_id = match_id
        # 场景
        if scene_id is not None:
            self.scene_id = scene_id
        else:
            if self.match_id == 0:
                self.scene_id = 1
            else:
                self.scene_id = 2

        # 目前msg只有273协议字符串数据和277协议字典数据
        self.msg = msg
        if isinstance(msg, str):
            self.std_text = sentence_standardizing(self.msg)
            self.code = 273
        else:
            self.std_text = None
            self.code = 277

        # 获取上次对话context
        self._last_context_data = self._get_last_context_data()
        # 先定义属性，后续处理流程进行实现
        self.entity = None
        self.template = None
        self.response = None
        self.intent_name = None
        self.robot_intent_name = None

        self.memory = self.last_attr("memory")
        # 将memory默认值设为{}，不可为None
        if self.memory is None:
            self.memory = {}

        self.topic = None
        self.params = {}

        # 用于版本控制的属性
        self.version = None
        self.platform = None

    def __str__(self):
        return str(self.context_data)

    @property
    def context(self):
        return self

    @property
    def context_data(self):
        """将上下文数据转化为字典变量，用于redis存储"""
        return {
            "idfa": self.idfa,
            "match_id": self.match_id,
            "scene_id": self.scene_id,
            "msg": self.msg,
            "std_text": self.std_text,
            "entity": self.entity,
            "template": self.template,
            "response": self.response,
            "intent_name": self.intent_name,
            "memory": self.memory,
            "topic": self.topic,
            "robot_intent_name": self.robot_intent_name
            # "params": self.params
        }

    @property
    def context_name(self):
        """获得redis里面用于存储上下文的name"""
        return REDIS_CONTEXT_PREFIX + self.idfa

    def del_memory(self, item_type, item_key):
        """删除memory中指定数据"""
        if item_type in self.memory and item_key in self.memory[item_type]:
            del self.memory[item_type][item_key]

    def _get_last_context_data(self):
        """上一次上下文数据"""
        return self.pre_context_data()

    # def finish_topic(self):
    #     """完成当前topic后，将完成状态改为1"""
    #     self.topic["finished"] = 1

    def gen_params(self):
        """
        根据上下文生成意图处理所需的参数，逻辑：
        1. 如果当前意图为confirm或unconfirm，则取上次对话上下文中的params作为当前参数；
        2. 如果
        将context中命名实体抽取结果的变量作为。
        """
        params = {
            "msg": self.msg,
            "std_text": self.std_text,
            "template": self.template,
            "context": self
        }

        if isinstance(self.msg, dict):
            self.params = params
            return  # 如果是277互动协议，则不需要后面的处理

        # todo 使用上下文---需要吗？
        for name_type in self.entity["ENTITIES"]:
            name_type_lower = name_type.lower()
            if len(self.entity["ENTITIES"][name_type]) == 1:
                name_data = self.entity["ENTITIES"][name_type][0]
                params[name_type_lower] = name_data[0]
                if name_data[1]:
                    if len(name_data[1]) == 1:
                        params[name_type_lower + "_id"] = name_data[1][0]
                    else:
                        params[name_type_lower + "_ids"] = name_data[1]
            else:
                for i, name_data in enumerate(
                    self.entity["ENTITIES"][name_type]
                ):
                    params[name_type_lower + str(i)] = name_data[0]
                    if name_data[1]:
                        if len(name_data[1]) == 1:
                            params[name_type_lower + "_id" + str(i)] = \
                                name_data[1][0]
                        else:
                            params[name_type_lower + "_ids" + str(i)] = \
                                name_data[1]

        # 提前处理ask_back topic
        # 1. 上次是ask_back，检查是否可以获得精确解，如仍然有多个，则继续走ask_back
        # 2. 在gen_topic中实现：如果params里面存在person_ids---即同一个名字有多个person_id，则走ask_back
        last_robot_intent_name = self.last_attr("robot_intent_name")
        if last_robot_intent_name in ["ask_back", "ask_back_again"]:
            last_topic = self.last_attr("topic")
            if last_topic is not None and last_topic.get("ask_back_status") == 1:
                choice_data = last_topic["data"]
                original_len = len(choice_data)
                # 通过person_id删选---精确删选，一旦存在便排除全部其它人员
                person_id = params.get("person_id")
                finished = False
                if person_id:
                    for data in choice_data:
                        if person_id == data["person_id"]:
                            finished = True
                            break

                # 通过team_id删选，保留全部该team_id的数据
                if not finished:
                    team_id = params.get("team_id")
                    if team_id:
                        choice_data = [
                            data for data in choice_data
                            if data["team_id"] == team_id
                        ]
                    if len(choice_data) == 1:
                        params["person_id"] = choice_data[0]["person_id"]
                        finished = True

                # 通过球员号码匹配，保留全部相同号码的数据
                if not finished:
                    shn = params.get("shirtnumber_id")
                    if shn is not None:
                        choice_data = [
                            data for data in choice_data
                            if data["shirtnumber"] == shn
                        ]
                    if len(choice_data) == 1:
                        params["person_id"] = choice_data[0]["person_id"]
                        finished = True

                # 如果没有匹配到任何询问数据，则认为转换了意图
                if len(choice_data) != original_len:
                    if not finished:
                        self.topic = last_topic
                        self.robot_intent_name = "ask_back_again"
                        self.topic["data"] = choice_data
                        self.topic["ask_back_status"] = 1
                        # self.topic["original_person_name"] = last_topic["original_person_name"]
                    else:
                        self.topic = last_topic
                        self.topic["ask_back_status"] = 2   # 待转具体意图处理
                else:
                    last_topic["ask_back_status"] = 0
                    self.intent_name = "no_idea"

        self.params = params

    def _gen_status(self):
        """获取前面对话状态值，并添加本轮对话状态值初始值"""
        status = self._last_context_data.get("status")
        if not status:
            status = {k: [0] for k in CONTEXT_STATUS_NAMES}
        else:
            status = copy.copy(status)
            # for val in status.values():
            #     val.append(0)
        return status

    def gen_topic(self):
        """
        生成topic初始值
        1. 当前意图是不可已作为topic的意图，则使用上一次对话topic，必要时
         对topic data进行更新---如没有上一次对话，则使用topic的默认值；
        2. 当前意图是可以作为topic的意图，则使用当前意图作为topic；
        3. topic data在具体的意图处理函数里面实现
        """
        default_topic = {
            "intent_name": DEFAULT_INTENT_NAME,
            "robot_intent_name": None,
            "finished": 0,
            "data": {}
        }
        last_topic = self.last_attr("topic")

        # 如果已经有了数据则直接退出---gen_params中也会对topic进行操作
        if self.topic:
            if last_topic:
                last_topic_intent_name = last_topic["intent_name"]
                if self.topic.get("ask_back_status") == 2:
                    self.intent_name = last_topic_intent_name
                    self.topic["ask_back_status"] = 0   # 清除ask_back状态
                elif self.topic.get("ask_back_status") == 1:
                    return

        # 当前意图不可以作为topic
        if self.intent_name in NON_TOPIC_INTENTS:
            if last_topic is None:
                self.topic = default_topic
            else:
                if self.intent_name == "confirm":
                    if last_topic.get("intent_name") in INTENTS_HAVE_CONFIRM:
                        self.topic = last_topic
                    # todo 新旧核心共存时，该elif为协调新旧核心代码，旧核心不再使用时删除
                    elif last_topic["intent_name"] == "to_old_kernel":
                        self.topic = last_topic
                    else:
                        self.topic = default_topic
                elif self.intent_name == "make_choice":
                    self.topic = last_topic
                else:
                    self.topic = default_topic

        # 当前意图可以作为topic
        else:
            # 判断是否有重person_id的情况，该情况需要走ask_back
            if "person_ids" in self.params:
                self.robot_intent_name = "ask_back"
                self.topic = {
                    "intent_name": self.intent_name,
                    "original_person_name": self.params["person"],
                    "data": self.params["person_ids"],
                    "ask_back_status": 1
                }
                return

            # # 如果上次是ask_back，则继续上次的意图名称
            # # 此时的topic已经在gen_params里面生成，这里只需要调整本次的意图名称
            # last_robot_intent_name = self.last_attr("robot_intent_name")
            # last_topic = self.last_attr("topic")
            # if last_robot_intent_name in ["ask_back", "ask_back_again"] \
            #         and last_topic and last_topic.get("ask_back_status", 0) == 2:
            #     last_topic_intent_name = last_topic["intent_name"]
            #     if last_topic_intent_name:
            #         self.intent_name = last_topic_intent_name
            #         self.topic = last_topic
            #         return

            if self.intent_name == "citiao":
                item = self.params.get("citiao")
                item_id = self.params.get("citiao_id")
                if item is None:
                    item = self.params.get("citiao0")
                    item_id = self.params.get("citiao_id0")
                    if item is None:
                        item = self.params.get("person_name")
                        item_id = self.params.get("person_id")
                        if item is None:
                            item = self.params.get("person_name0")
                            item_id = self.params.get("person_id0")
                            if item is None:
                                item = self.params.get("venue_name")
                                item_id = self.params.get("venue_id")
                                if item is None:
                                    item = self.params.get("venue_name0")
                                    item_id = self.params.get("venue_id0")
                                    if item is None:
                                        item = self.params.get("team_name")
                                        item_id = self.params.get("team_id")
                                        if item is None:
                                            item = self.params.get("team_name0")
                                            item_id = self.params.get("team_id0")
                                            if item is None:
                                                item = self.params.get("league_name")
                                                item_id = self.params.get("league_id")
                                                if item is None:
                                                    item = self.params.get("league_name0")
                                                    item_id = self.params.get("league_id0")
                self.topic = {
                    "intent_name": self.intent_name,
                    "finished": 0,
                    "data": {
                        "item": item,
                        "item_id": item_id,
                    }
                }
            else:   # 其它意图如有需要，在这里添加topic逻辑
                self.topic = {
                    "intent_name": self.intent_name,
                    "finished": 0,
                    "data": {}
                }

    def get_memory(self, item_type, item_data):
        """
        从memory中提取记忆的字典变量，针对不同的记忆类型，有不同的约定，
        后续可以进行补充：
            词条：
                item_type: "citiao"
                item_data: {"citiao_key": str}
                return: {"citiao_ids": list, "citiao_id": int},
                    不存在则返回{"citiao_ids": [], "citiao_id": None}
        """
        if item_type == "citiao":
            return self.memory.get("citiao", {}).get(
                item_data["citiao_key"],
                {"citiao_ids": [], "sort": -1, "tags": set()}
            )
        # todo other types

        return None

    def last_attr(self, attr_name):
        """获得上一次的上下文某个属性的数据，如不存在则返回None"""
        return self._last_context_data.get(attr_name)

    def put_memory(self, item_type, item_data):
        """
        对应get_memory，用于将数据放入记忆，对于不同的记忆数据，有不同的约定，
        后续根据需要可以继续扩充：
            词条：
                item_type: "citiao"
                item_data: {"citiao_key": str, "citiao_id": int}
                注：将citiao_id保存到self.memory["citiao"][citiao_key] = {
                    "citiao_ids": [],
                    "citiao_id": int
                }，citiao_ids用于记录所有已浏览过的词条id，citiao_id用于记录当前
                对话的词条id。
        """
        if item_type == "citiao":
            if "citiao" not in self.memory:
                self.memory["citiao"] = {}
            citiao_key = item_data["citiao_key"]
            citiao_ids = item_data["citiao_ids"]
            sort = item_data["sort"]
            tags = item_data["tags"]
            self.memory["citiao"][citiao_key] = {
                "citiao_ids": citiao_ids,
                "sort": sort,
                "tags": tags
            }

    def pre_context_data(self, index=-1):
        """
        从redis获取上下文数据
        @:param n: 获取的上下文序列号，与python list的获取方式保持一致，
        默认值-1意味着默认取redis里面的最后一个数据。
        """
        pre_context_data = self._redis.lindex(self.context_name, index)
        return eval(pre_context_data) if pre_context_data is not None else {}

    def save(self):
        """完成全部处理流程，不再使用时，将context数据保存到redis和mysql里面"""
        # 1. context -> redis
        self._redis.rpush(self.context_name, self.context_data)
        self._redis.expire(self.context_name, CONTEXT_EXPIRE)

        print(self.template)
        value = [self.raw_text, self.std_text, self.template, self.intent_name,
                 self.scene_id, datetime.now().strftime('%c')]
        # self.raw_text disappears
        print(value)
        self._redis.rpush('deco:corpus', value)
        # redis to store corpus, added by deco

    def update_topic(self, intent_name, finished=0, data=None):
        """更新topic"""
        self.topic = {
            "intent_name": intent_name,
            "finished": finished,
            "data": data if data is not None else {}
        }
