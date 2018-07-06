"""
@Project   : cubegirl
@Module    : cmysql.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/15 16:52
@Desc      : 
"""
import logging
import pymysql
import wrapcache
from aiball.conf import server_config_get
from .credis import redis_cache


def mysql_get_connection(db_name: str,
                         db_cfg: str,
                         use_dictcursor: bool = False):
    """
    根据指定的db名称，创建connect
    :param use_dictcursor: 是否使用DictCursor
    :param db_name: 指定的db名称
    :return: 返回mysql的连接
    """

    cursorclass = pymysql.cursors.DictCursor if use_dictcursor else \
        pymysql.cursors.Cursor
    return pymysql.connect(
        host=server_config_get(db_cfg + ".host"),
        port=server_config_get(db_cfg + ".port"),
        user=server_config_get(db_cfg + ".user"),
        passwd=server_config_get(db_cfg + ".passwd"),
        db=db_name,
        charset="utf8",
        cursorclass=cursorclass,
    )


def _execute(_db_name, _sql, _db_cfg, _use_dictcursor):
    try:
        conn = mysql_get_connection(db_name=_db_name,
                                    db_cfg=_db_cfg,
                                    use_dictcursor=_use_dictcursor)
        cursor = conn.cursor()
        cursor.execute(_sql)
        rtv = [_x for _x in cursor.fetchall()]
        conn.close()
        return rtv
    except Exception as e:
        logging.exception(e)
        return []


def do_query_local_cache(db_name: str = "db_robot",
                         sql: str = "",
                         db_cfg: str = "mysql_db_robot",
                         use_dictcursor: bool = False,
                         ex: int = 1) -> list:
    """
    在指定的DB中按_sql指定的语句查找数据，使用本地缓存
    :param use_dictcursor: 是否使用DictCursor
    :param db_name: 指定的db
    :param sql: sql语句
    :param db_cfg: db配置
    :param ex: 过期时间
    :return: 反回list结果
    """
    @wrapcache.wrapcache(timeout=ex)
    def _query(_db_name, _sql, _db_cfg, _use_dictcursor):
        return _execute(_db_name=_db_name,
                        _sql=_sql,
                        _db_cfg=_db_cfg,
                        _use_dictcursor=_use_dictcursor)

    return _query(
        _db_name=db_name,
        _sql=sql,
        _db_cfg=db_cfg,
        _use_dictcursor=use_dictcursor)


def do_query_remote_cache(db_name: str = "db_robot",
                          sql: str = "",
                          db_cfg: str = "mysql_db_robot",
                          use_dictcursor: bool = False,
                          ex: int = 1) -> list:
    """
    在指定的DB中按_sql指定的语句查找数据，使用redis缓存
    :param use_dictcursor: 是否使用DictCursor
    :param db_name: 指定的db
    :param sql: sql语句
    :param db_cfg: db配置
    :param ex: 过期时间
    :return: 反回list结果
    """
    @redis_cache(ex=ex)
    def _query(_db_name, _sql, _db_cfg, _use_dictcursor):
        return _execute(_db_name=_db_name,
                        _sql=_sql,
                        _db_cfg=_db_cfg,
                        _use_dictcursor=_use_dictcursor)

    return _query(
        _db_name=db_name,
        _sql=sql,
        _db_cfg=db_cfg,
        _use_dictcursor=use_dictcursor)
