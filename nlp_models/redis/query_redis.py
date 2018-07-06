"""
@Project   : aiball
@Module    : query_redis.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/21 15:26
@Desc      : 
"""

import logging
from aiball.db import DataRedis


def _context_redis_key(name: str, key_name: str, value_type: str) -> str:
    """
    创建aiball项目统一redis存储name名称
    :param name: 需要存储的项目key
    :param key_name: 存储/查询的key的类型名
    :param value_type: 存储数据的类型
    :return: 返回build好的字符串

    name = _context_redis_key(name=seq, key_name="seq", value_type="context")
    """

    return "aiball_main_value:%s:key_name_%s_%s" % (
        value_type, key_name, name)


def save_context_by_seq(context: dict, seq: str, ex=900):
    """
    按照seq保存上下文
    :param context: 需要保存的上下文关系字典
    :param seq: 与上下文对应的key
    :param ex: 过期时间

    数据存储在redis中，key="aiball_main_value:context:seq_xxxx", value=context
    以seq存储的context值和seq一一对应，指定seq时可以直接获取
    """
    if seq and context:
        try:
            _redis = DataRedis()
            name = _context_redis_key(
                name=seq,
                key_name="seq",
                value_type="context")
            _redis.db.set(name=name, value=context, ex=ex)
        except Exception as e:
            logging.exception(e)


def save_string_by_seq(source: str, seq: str= "", ex=900, value_type="msg"):
    """
    按照seq保存用户提问问题
    :param source: 用户问题
    :param seq: 与seq对应的用户问题
    :param ex: 过期时间
    :param value_type: 存储数据类型

    key="aiball_main_value:question:seq_xxxx", value=question
    """
    _redis = DataRedis()
    if seq and source:
        name = _context_redis_key(
            name=seq,
            key_name="seq",
            value_type=value_type)
        _redis.db.set(name=name, value=source, ex=ex)


def save_context_by_idfa(context: dict, idfa: str= "", ex=900):
    """
    按照idfa保存上下文，上下文会被存储在一个list中
    :param context: 需要保存的上下文
    :param idfa: 用户idfa
    :param ex: 过期时间（整个list过期时间）

    key="aiball_main_value:context:idfa_xxxx", value[n]=context
    这个函数有一个风险：如果同一idfa用户地直在更新问题，则整个list永远不过期且占内存越来越多
    """
    if idfa and context:
        try:
            _redis = DataRedis()
            name = _context_redis_key(
                name=idfa, key_name="idfa",
                value_type="context")
            _redis.db.rpush(name, context)
            _redis.db.expire(name=name, time=ex)
        except Exception as e:
            logging.exception(e)


def save_string_by_idfa(value: str, idfa: str= "", ex=900, value_type=""):
    """
    按照idfa保存数据，用户问题会被存储在一个list中
    :param value: 需要保存的数据
    :param idfa: 用户idfa
    :param value_type: 数据分类
    :param ex: 过期时间（整个list过期时间）

    key="aiball_main_value:value_type:idfa_xxxx", value[n]=value
    这个函数有一个风险：如果同一idfa用户地直在更新问题，则整个list永远不过期且占内存越来越多
    """
    if idfa and value:
        _redis = DataRedis()
        name = _context_redis_key(
            name=idfa,
            key_name="idfa",
            value_type=value_type)
        _redis.db.rpush(name, value)
        _redis.db.expire(name=name, time=ex)


def save_question_by_idfa(question: str, idfa: str= "", ex=900):
    """
    按照idfa保存用户问题，用户问题会被存储在一个list中
    :param question: 需要保存的用户问题
    :param idfa: 用户idfa
    :param ex: 过期时间（整个list过期时间）

    key="aiball_main_value:question:idfa_xxxx", value[n]=question
    这个函数有一个风险：如果同一idfa用户地直在更新问题，则整个list永远不过期且占内存越来越多
    """
    if idfa and question:
        _redis = DataRedis()
        name = _context_redis_key(
            name=idfa,
            key_name="idfa",
            value_type="question")
        _redis.db.rpush(name, question)
        _redis.db.expire(name=name, time=ex)


def save_request_by_idfa(request: dict, idfa: str= "", ex=900):
    """
    按照idfa保存用户请求，用户请求会被存储在一个list中
    :param request: 需要保存的用户问题
    :param idfa: 用户idfa
    :param ex: 过期时间（整个list过期时间）

    key="aiball_main_value:request:idfa_xxxx", value[n]=request
    这个函数有一个风险：如果同一idfa用户地直在更新问题，则整个list永远不过期且占内存越来越多
    """
    if idfa and request:
        try:
            _redis = DataRedis()
            # value = str(request).replace("'", "\"")
            name = _context_redis_key(
                name=idfa,
                key_name="idfa",
                value_type="request")
            _redis.db.rpush(name, request)
            _redis.db.expire(name=name, time=ex)
        except Exception as e:
            logging.exception(e)


# -----------------------------------------------------------------------------


def read_context_by_seq(seq: str) -> dict:
    """
    根据seq获取指定的上下文关系
    :param seq: 需要获取的上下文对应的seq值
    :return: 返回上下文关系字典
    """
    _redis = DataRedis()
    name = _context_redis_key(
        name=seq,
        key_name="seq",
        value_type="context")
    try:
        # value = json.loads(_redis.db.get(name=name))
        value = eval(_redis.db.get(name=name))
        return value
    except Exception as e:
        logging.exception(e)
        return {}


def read_string_by_seq(seq: str, value_type="msg") -> str:
    """
    根据seq查询对应的用户字符串
    :param seq: 指定的seq值
    :param value_type: 存储的值的类型
    :return:
    """
    _redis = DataRedis()
    name = _context_redis_key(
        name=seq,
        key_name="seq",
        value_type=value_type)
    return _redis.db.get(name=name)


def read_context_by_idfa(idfa: str, index: int=-1) -> dict:
    """
    根据指定的用户idfa查index所对应的上下文关系
    :param idfa: 用户idfa
    :param index: 需要查找的上下文关系的index值，-1表示最后一条
    :return: 返回查找到的上下文关系的字典或者空字典

    index取值从0（第一条）开始，为负数时表示从最后一条向前推算
    """
    _redis = DataRedis()
    name = _context_redis_key(
        name=idfa,
        key_name="idfa",
        value_type="context")
    try:
        # value = json.loads(_redis.db.lindex(name=name, index=index))
        result = _redis.db.lindex(name=name, index=index)
        value = eval(result) if result is not None else {}
        return value
    except Exception as e:
        logging.exception(e)
        return {}


def read_string_by_idfa(idfa: str, index: int=-1, value_type="") -> str:
    """
    根据指定的用户idfa查index所对应的用户数据
    :param idfa: 用户idfa
    :param index: 需要查找的question的index值，-1表示最后一条
    :param value_type: 需要查询的数据的分类
    :return: 返回查找到的string的字典或者空字典

    index取值从0（第一条）开始，为负数时表示从最后一条向前推算
    """
    try:
        _redis = DataRedis()
        name = _context_redis_key(
            name=idfa,
            key_name="idfa",
            value_type=value_type)
        return _redis.db.lindex(name=name, index=index)
    except Exception as e:
        logging.exception(e)
        return ""


def read_question_by_idfa(idfa: str, index: int=-1) -> str:
    """
    根据指定的用户idfa查index所对应的用户问题
    :param idfa: 用户idfa
    :param index: 需要查找的question的index值，-1表示最后一条
    :return: 返回查找到的question的字典或者空字典

    index取值从0（第一条）开始，为负数时表示从最后一条向前推算
    """
    try:
        _redis = DataRedis()
        name = _context_redis_key(
            name=idfa,
            key_name="idfa",
            value_type="question")
        return _redis.db.lindex(name=name, index=index)
    except Exception as e:
        logging.exception(e)
        return ""


def read_request_by_idfa(idfa: str, index: int=-1) -> dict:
    """
    根据指定的用户idfa查index所对应的request
    :param idfa: 用户idfa
    :param index: 需要查找的request的index值，-1表示最后一条
    :return: 返回查找到的request的字典或者空字典

    index取值从0（第一条）开始，为负数时表示从最后一条向前推算
    """
    _redis = DataRedis()
    name = _context_redis_key(
        name=idfa,
        key_name="idfa",
        value_type="request")
    try:
        # value = json.loads(_redis.db.lindex(name=name, index=index))
        value = eval(_redis.db.lindex(name=name, index=index))
        return value
    except Exception as e:
        logging.exception(e)
        return {}


