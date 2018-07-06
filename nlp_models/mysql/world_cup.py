"""
@Project   : CubeGirl
@Module    : world_cup.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/2/28 15:15
@Desc      :
"""
import typing
import warnings

from pymysql.err import MySQLError
import aiball.db.query_sql_function as QSF
from aiball.consts import ErrorCode


class Record:
    """所有查询结果类的基类"""

    @classmethod
    def fromdata(cls, data: dict):
        obj = cls()
        obj.upsert(data)
        return obj

    def upsert(self, data: dict):
        for k, v in data.items():
            self._check_key(k)
            setattr(self, k, v)

    def _check_key(self, key):
        if not key in self.__dict__:
            warnings.warn('发现类{}未声明的属性{}，请检查SQL语句是否正确AS'.format(
                type(self).__name__, key))

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(self.__dict__.items())


class WorldCupPlayerInfo(Record):
    def __init__(self, _id=0):
        self.id = _id
        self.name = ""
        self.nationality = ""
        self.number = 0
        self.pos = ""


class WorldCupEvent(Record):
    """
    世界杯事件信息
    """

    def __init__(self):
        self.code = 0  # 事件类型
        self.game_year = 0  # 世界杯时间（年）
        self.match_home_id = 0  # 主队id
        self.match_away_id = 0  # 客队id
        self.match_home_name = ""  # 主队名
        self.match_away_name = ""  # 客队名
        self.team_id = 0  # 事件归属球队id
        self.team_name = ""  # 事件归属球队名称
        self.player_id = 0  # 事件发生球员id
        self.player_name = ""  # 事件发生球员名称


class WorldCupEventRecord(WorldCupEvent):
    """
    世界杯纪录事件信息
    """

    def __init__(self):
        super().__init__()
        self.player_age_year = 0  # 当时球员年龄
        self.player_age_day = 0  # 当时球员年龄多余的天数
        self.r_event_seconds = 0  # 事件发生在比赛开始后多少秒
        self.match_id = 0  # 事件发生的比赛id
        self.against_team_name = ''


class WorldCupTeamResult(Record):
    def __init__(self):
        self.team_id = 0
        self.team_name = ""
        self.rank = ""  # 冠军、亚军、季军、殿军、8强、16强、小组赛


class WorldCupTeamTrophy(Record):
    def __init__(self):
        self.team_id = 0
        self.team_name = ""
        self.trophy_num = 0
        self.trophy_list = list()  # 列表中元素为获得将杯的时间（年）
        self.count = 0  # 冠军（或其他）数量


class WorldCupMatchResult(Record):
    """
    世界杯比赛结果
    """

    def __init__(self):
        self.id = 0
        self.year = 0
        self.season_name = ""
        self.round_name = ""
        self.home_id = 0
        self.away_id = 0
        self.home_name = ""
        self.away_name = ""
        self.home_score = 0
        self.away_score = 0
        self.fs_home = 0
        self.fs_away = 0
        self.ets_home = 0
        self.ets_away = 0


class WorldCupParameter(object):
    def __init__(self):
        self.country_name_list = list()
        self.number_name_list = list()
        self.year_list = list()
        self.team_name_list = list()
        self.std_text = ""


def _world_cup_get_season_id(wp: WorldCupParameter) -> int:
    def _get_id_from_number():
        try:
            # 根据number直接匹配世界杯id
            for number in wp.number_name_list:
                _id, err = world_cup_get_season_id_by_number(_number=number)
                if err == ErrorCode.ERROR_PASS and _id > 0:
                    return _id
        except Exception as e:
            pass
        return 0

    def _get_id_from_country_list():
        try:
            # 根据举办国家和举办年份查世界杯id
            for host in wp.country_name_list:
                if host + "世界杯" not in wp.std_text:
                    continue
                if "队" in host:
                    continue
                if host + "队世界杯" in wp.std_text:
                    continue
                if wp.year_list:
                    for _year in wp.year_list:
                        _id, err = world_cup_get_season_id_by_host_and_year(
                            _host=host, _year=_year)
                        if err == ErrorCode.ERROR_PASS and _id > 0:
                            return _id
                else:
                    _id, err = world_cup_get_season_id_by_host_and_year(
                        _host=host)
                    if err == ErrorCode.ERROR_PASS and _id > 0:
                        return _id
        except Exception as e:
            pass
        return 0

    def _get_id_from_year():
        try:
            # 根据举办时间查世界杯id
            for _year in wp.year_list:
                _id, err = world_cup_get_season_id_by_year(_year=_year)
                if err == ErrorCode.ERROR_PASS and _id > 0:
                    return _id
        except Exception as e:
            pass
        return 0

    season_id = _get_id_from_number()
    if season_id == 0:
        season_id = _get_id_from_country_list()
        if season_id == 0:
            season_id = _get_id_from_year()
    return season_id


def _world_cup_get_team_ids(wp: WorldCupParameter) -> list:
    team_list = list()
    try:
        for country in wp.team_name_list:
            # "xx世界杯"这种间法，xx不应该为球队球, 但“xx队”则为球队名
            if (country + "世界杯" in wp.std_text) and "队" not in country:
                continue
            c = country.replace("国家队", "").replace("队", "")
            team_id, err = world_cup_get_team_id_by_name(c)
            if err == ErrorCode.ERROR_PASS:
                team_list.append((team_id, country))
    except Exception as e:
        pass

    return team_list


def world_cup_get_season_name_by_season_id(_season_id: int) -> (str, int):
    rtv, err = "", ErrorCode.ERROR_PASS
    try:
        res = QSF.world_cup_query_season_name_by_season_id(_season_id)
        if not res:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtv = res[0][0]
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW

    return rtv, err


def world_cup_process_parameter(contex) -> bool:
    """
    将世界杯实体抽取的
    :param contex:
    :return:
    """
    try:
        parameter = contex.world_cup_parameter
        # get season id
        season_id = _world_cup_get_season_id(parameter)

        # get team id
        team_list = _world_cup_get_team_ids(parameter)

        if not contex.params or not isinstance(contex.params, dict):
            contex.params = dict()

        # 填充season相关信息
        contex.params["cup_season_id"] = season_id
        season, err = world_cup_get_season_name_by_season_id(season_id)
        if err == ErrorCode.ERROR_PASS:
            contex.params["cup_season"] = season

        # 填充team相关信息
        if len(team_list) == 1:
            contex.params["team_id"] = team_list[0][0]
            contex.params["team"] = team_list[0][1]
        else:
            n = 0
            for team in team_list:
                _id_name = "team_id%d" % n
                _team_name = "team%d" % n
                contex.params[_id_name] = team[0]
                contex.params[_team_name] = team[1]
                n += 1

        return True
    except Exception as e:
        pass

    return False


def world_cup_get_team_id_by_name(_name: str) -> (int, int):
    rtv, err = 0, 0
    try:
        res = QSF.world_cup_get_team_info_by_name(_team_name=_name)
        if not res:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtv = int(res[0][0])
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW

    return rtv, err


# -------------------------------------------------------------------------


def world_cup_get_season_id_by_year(_year: int) -> (int, int):
    """
    通过举办年份直接查出世界杯season id（哪一届）
    :param _year: 指定的年份（4-digit）
    :return: 返回切界杯的season id以及错误码

    未找到时，error返回ERROR_YEAR_NO_GAME
    """
    rtn, err = 0, ErrorCode.ERROR_PASS
    try:
        session_id = QSF.world_cup_get_session_id_by_year(_year)[0][0]
    except IndexError:
        err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        rtn = session_id
    return rtn, err


def world_cup_get_key_by_value(value: str, dict_data: dict) -> list:
    """给定一个value,从字典数据中查找值为value的key"""
    return [k for k, v in dict_data.items() if v == value]


def world_cup_get_season_id_by_host_and_year(
        _host: str, _year: int = None) -> (int, int):
    """
    通过举办国家和年份直接查出世界杯season id（哪一届）。年份可以省略
    :param _host: 指定需要查询的举办的国家。
    :param _year: 指定的年份，如果_year<30，前面加20否则加19，如14为2014
    :return: 返回切界杯的season id以及错误码

    _host支持别名。只指定国家，且有重复数举办时，返回最近一届
    优先使用国家查询，如果有重复，两再使用年份筛选
    1. 使用国家查出只有一个，直接返回，error返回ERROR_PASSF
    2. 使用国家找到多个时，用年份筛选一个；如果给的年份为错误的，返回最近一届，error返回ERROR_YEAR_NO_GAME
    3. 使用国家未找到时，且用年份找到，返回找到的id，error返回ERROR_HOST_NO_GAME
    4. 使用国家和年份都没找到时，error返回ERROR_HOST_YEAR_NO_GAME
    """
    rtn, err = 0, ErrorCode.ERROR_PASS

    season_year_nation_dict = QSF.world_cup_get_all_year_season_name()
    season_id_dict = QSF.world_cup_get_all_season()
    nation_lst = list(season_year_nation_dict.values())
    esp_two_nation = ["韩国", "日本"]
    nation_lst.extend(esp_two_nation)
    if _host in esp_two_nation:
        rtn = season_id_dict.get("2002韩日")
    elif _host in nation_lst and _host not in esp_two_nation:
        year_lst = world_cup_get_key_by_value(_host, season_year_nation_dict)
        if len(year_lst) == 1:
            season_name = str(year_lst[0]) + _host
        else:
            if _year in year_lst:
                season_name = str(_year) + _host
            else:
                year_lst.sort()
                season_name = str(year_lst[-1]) + _host
        rtn = season_id_dict.get(season_name)
    else:
        nation = season_year_nation_dict.get(_year, "")
        if nation:
            season_name = str(_year) + nation
            rtn = season_id_dict.get(season_name)
        else:
            err = ErrorCode.ERROR_HOST_YEAR_NO_GAME
    return rtn, err


def world_cup_get_season_id_by_number(_number: int) -> (int, int):
    """
    通过世界杯编号查询season id
    :param _number: 指定的世界杯编号，目前只支持1~21
    :return: 返回切界杯的season id以及错误码

    不支持的_number，error返回ERROR_NUMBER_OUT_OF_RANGE
    """
    rtn, err = 0, ErrorCode.ERROR_PASS
    try:
        num_country_map = dict(QSF.world_cup_get_season_id_orderd_by_date())
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not num_country_map:
            err = ErrorCode.ERROR_EMPTY
        season_id = num_country_map.get(_number)
        if season_id:
            rtn = season_id
        else:
            err = ErrorCode.ERROR_NUMBER_OUT_OF_RANGE
    return rtn, err


def world_cup_get_goalscorers_list_by_season(
        _season: int, _top: int = 5) -> (list, int):
    """
    通过指定的赛季id，获取射手榜
    :param _season: 指定的赛季id。
    :param _top: 指定返回榜单的长度，默认为5个
    :return: 返回榜单列表以及错误码

    榜单内容：排名、球员名字、所属国家、进球数量
    id为0时，返回总榜，功能和word_cup_get_goal_rank_total相同
    """
    rtn, err = [['排名', '球员', '国家', '进球数量']], ErrorCode.ERROR_PASS
    try:
        rslt = QSF.world_cup_get_goalscorers_list_by_season(_season, _top)
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not rslt:
            err = ErrorCode.ERROR_EMPTY
        else:
            for _ in rslt:
                rtn.append(list(_))
    return rtn, err


def world_cup_get_goalscorers_list_total(_top: int = 5) -> (list, int):
    """
    查询世界杯总射手榜
    :param _top: 指定返回榜单的长度，默认为5个
    :return: 返回榜单列表以及错误码

    榜单内容：排名、球员名字、所属国家、进球数量
    """
    rtn, err = [['排名', '球员', '国家', '进球数量']], ErrorCode.ERROR_PASS
    try:
        rslt = QSF.world_cup_get_goalscorers_list_total(_top)
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not rslt:
            err = ErrorCode.ERROR_EMPTY
        else:
            for _ in rslt:
                rtn.append(list(_))
    return rtn, err


def world_cup_get_record_event_goal_player_age(
        _reverse: bool = False,
        _round: str = None) -> (WorldCupEventRecord, int):
    """
    查询世界杯进球球员年龄记录（进球年龄最大或最小进球球员）
    :param _reverse: 是否反转查询，True，查最小，False查最大
    :param _round: 指定查询的赛事进度，未指定时查全部。本函数只支持空值和决赛
    :return: 返回查记录的事件类实例，以及错误码
    """
    rtn, err = WorldCupEventRecord(), ErrorCode.ERROR_PASS
    try:
        assert _round in ["决赛", None]
        event_dict = QSF.world_cup_get_rocord_event_goal_player_age(
            _reverse, _round)
        if not event_dict:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtn.upsert(event_dict)
    except AssertionError:
        err = ErrorCode.ERROR_KEY_ERROR
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_fast_goal_rank(_top: int = 5) -> (list, int):
    """
    查询世界杯进球最快的榜单
    :param _top: 指定返回榜单的长度，默认为5个
    :return: 返回榜单列表以及错误码

    榜单内容：排名、进球球员、所属球队、进球秒数、对阵球队
    """
    rtn, err = [['进球球员', '所属球队', '进球秒数', '对阵球队']], ErrorCode.ERROR_PASS
    try:
        rslt = QSF.world_cup_get_fast_goal_rank(_top)
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not rslt:
            err = ErrorCode.ERROR_EMPTY
        else:
            for _ in rslt:
                rtn.append(list(_))
    return rtn, err


def world_cup_get_team_rank_by_goal(
        _top: int = 5) -> (list, int):
    """
    世界杯进球最多的球队
    :param _top: 指定返回榜单的长度，默认为5个
    :return: 返回榜单列表以及错误码

    榜单表格字段：国家名、参赛届数、总比赛场次，进球数
    """
    rtn, err = [['国家名', '参赛届数', '总比赛场次', '进球数']], ErrorCode.ERROR_PASS
    try:
        rslt = QSF.world_cup_get_team_rank_by_goal(_top)
    except AssertionError:
        err = ErrorCode.ERROR_KEY_ERROR
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not rslt:
            err = ErrorCode.ERROR_EMPTY
        else:
            for _ in rslt:
                rtn.append(list(_))
    return rtn, err


def world_cup_get_team_group_rank_by_goal(top=5):
    rtn, err = [['序号', '国家名', '参赛届数', '进球数']], ErrorCode.ERROR_PASS
    try:
        rslt = QSF.world_cup_get_team_group_rank_by_goal(top)
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not rslt:
            err = ErrorCode.ERROR_EMPTY
        else:
            for index, _ in enumerate(rslt, start=1):
                rtn.append([index, *_])
    return rtn, err


def world_cup_get_team_trophy_rank(_top: int = 5, _type: int = 0) -> (
        typing.List[WorldCupTeamTrophy], int):
    """
    世界杯夺冠次数最多的球队
    :param _top: 指定返回榜单的长度，默认为5个
    :param _type: 查询类弄：0冠军，1亚军，2决赛
    :return: 返回榜单列表以及错误码

    返回list的元素为WorldCupTeamTrophy实例
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    query_func_map = {0: QSF.world_cup_get_most_champion_team,
                      1: QSF.world_cup_get_most_second_palce_team,
                      2: QSF.world_cup_get_most_final_team}
    try:
        query_func = query_func_map[_type]
        rslt = query_func(_top)
    except IndexError:
        err = ErrorCode.ERROR_KEY_ERROR
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not rslt:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtn = [WorldCupTeamTrophy.fromdata(_) for _ in rslt]
    return rtn, err


def world_cup_get_match_by_goal_count_rank(
        _top: int = 3,
        _round: str = None) -> (list, int):
    """
    世界杯进球最多的比赛，前3场
    :param _top: 指定返回榜单的长度，默认为3个
    :param _round: 指定查询的赛事进度，未指定时查全部。本函数只支持空值，决赛和小组赛
    :return: 返回榜单列表以及错误码

    表格字段：对阵球队、比分、第几届世界杯和什么阶段
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        assert _round in ["决赛", "小组赛", None]
        rtn = QSF.world_cup_get_match_by_goal_count_rank_lst(_top, _round)
        if len(rtn) == 1:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_match_score_diff_rank(
        _top: int = 3) -> (list, int):
    """
    世界杯比分悬殊最大的比赛，前3场
    :param _top: 指定返回榜单的长度，默认为3个
    :return: 返回榜单列表以及错误码

    表格字段：对阵球队、比分、第几届世界杯和什么阶段
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_match_score_diff_rank_lst(_top)
        if len(rtn) == 1:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_fast_goal(_round: str = None) -> (WorldCupEventRecord, int):
    """
    世界杯进球最快的进球
    :param _round: 指定查询的赛事进度，未指定时查全部。本参数只支持留空，决赛和小组赛
    :return: 返回查询到的事件以及错误代码
    """
    rtn, err = WorldCupEventRecord(), ErrorCode.ERROR_PASS
    try:
        assert _round in ["决赛", "小组赛", None]
        event_dict = QSF.world_cup_get_fast_goal_by_round(_round)
        if not event_dict:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtn.upsert(event_dict)
    except AssertionError:
        err = ErrorCode.ERROR_KEY_ERROR
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_appearance_rank(_top: int = 5) -> (list, int):
    """
    世界杯出场最多的球员top n
    :param _top: 指定返回榜单的长度，默认为5个
    :return: 返回榜单列表以及错误码

    表格字段：序号、球员名、出场次数、所属国家
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_player_appearance_rank(_top)
        if len(rtn) == 1:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_player_card_rank(
        _top: int = 5, _card: int = 1) -> (list, int):
    """
    世界杯罚牌的球员top n
    :param _top: 指定返回榜单的长度，默认为5个
    :param _card: 查询罚牌类型：1黄牌，2红牌
    :return: 返回榜单列表以及错误码

    表格字段：序号、球员名、罚牌次数、所属国家
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_player_red_yellow_card_rank(_top, _card)
        if len(rtn) == 1:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


# 1- 查询每届世界杯赛果和比分----------------------------------------------------

def world_cup_get_match_by_full_information(
        _season: int, _round: str, _team: int) -> (list, int):
    """
    根据世界杯赛季+阶段+球队id查询比赛id
    :param _season: 世界杯season id
    :param _round: 世界杯阶段，空值时查全部
    :param _team: 球队id
    :return: 返回match id以及错误码
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    round_name_lst = QSF.world_cup_get_round_name_by_season_id(_season)
    if _round in round_name_lst:
        try:
            rtn = QSF.world_cup_get_match_id_by_season_round_team(
                _season, _round, _team
            )
            if not rtn:
                err = ErrorCode.ERROR_EMPTY
        except MySQLError:
            err = ErrorCode.ERROR_MYSQL_ERROR
        except Exception:
            err = ErrorCode.ERROR_UNKNOW
    else:
        err = ErrorCode.ERROR_SEASON_NO_ROUND
    return rtn, err


def world_cup_get_match_list_by_season_round(
        _season: int, _round: str) -> (list, int):
    """
    如果用户的问法中含有具体的某一届世界杯、某一个阶段，则直接给该阶段的赛果（小组赛暂时不支持）
    :param _season: 世界杯season id
    :param _round: 世界杯阶段，空值时查全部
    :return: 返回match id列表以及错误码
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    round_name_lst = QSF.world_cup_get_round_name_by_season_id(_season)
    if _round in round_name_lst:
        try:
            if _round != "小组赛":
                rtn = QSF.world_cup_get_match_id_by_season_round(
                    _season, _round
                )
                if not rtn:
                    err = ErrorCode.ERROR_EMPTY
            else:
                err = ErrorCode.ERROR_UN_SUPPORT
        except MySQLError:
            err = ErrorCode.ERROR_MYSQL_ERROR
        except Exception:
            err = ErrorCode.ERROR_UNKNOW
    else:
        err = ErrorCode.ERROR_SEASON_NO_ROUND
    return rtn, err


def world_cup_get_final_match_id_by_season_id(
        _season: int) -> (int, int):
    """
    如果用户的问法中只有某一届世界杯，则给予该世界杯的决赛的赛果
    :param _season: 世界杯season id
    :return: 返回match id列表以及错误码
    """
    rtn, err = 0, ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_match_id_by_season(_season)
        if rtn == 0:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_last_match_id_by_team_id(
        _team: int) -> (int, int):
    """
    如果用户的问法中只有某个球队，则给出最近的世界杯该球队最后一场比赛的赛果
    :param _team: 球队id
    :return: 返回该球队最后一次世界杯赛程id，以及错误码
    """
    rtn, err = 0, ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_last_match_id_by_team(_team)
        if rtn == 0:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_last_match_id_by_season_team_id(
        _season: int, _team: int) -> (int, int):
    """
    如果用户的问法中只有某个球队和某届世界杯，则给该届世界杯的这个球队最后一场的赛果
    :param _season: 世界杯season id
    :param _team: 球队id
    :return: 返回match id列表以及错误码
    """
    rtn, err = 0, ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_last_match_id_by_season_team(_season, _team)
        if rtn == 0:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_match_list_by_round(
        _round: str) -> (list, int):
    """
    如果用户的问法中只有某一阶段的，则给最近的世界杯该阶段的赛果（小组赛不支持）
    :param _round: 世界杯阶段，空值时查全部
    :return: 返回match id列表以及错误码
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        if _round != "小组赛":
            rtn = QSF.world_cup_get_match_lst_by_round(_round)
            if not rtn:
                err = ErrorCode.ERROR_EMPTY
        else:
            err = ErrorCode.ERROR_UN_SUPPORT
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_match_id_by_round_team(
        _round: str, _team: int) -> (list, int):
    """
    问法中含有具体的、某一个阶段、哪支球队，则直接给予最近世界杯该球队这个阶段的赛果
    :param _round: 世界杯阶段，空值时查全部
    :param _team: 球队id
    :return: 返回match id以及错误码
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        rtn = QSF.world_cup_get_match_id_lst_by_round_team(_round, _team)
        if not rtn:
            err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_match_list_by_two_team(
        _team1: int, _team2: int) -> (list, int):
    """
    用户的问法中含有两个球队，则给予这两个球队历史上所有的比赛赛果

    注意：查询时要查 _team1 vs _team2 以及 _team2 vs _team1
    :param _team1: 第一个球队id
    :param _team2: 第二个球队id
    :return: 返回比赛列表，以及错误码
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        match_lst = QSF.world_cup_get_match_list_by_two_team(_team1, _team2)
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        if not match_lst:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtn = [WorldCupMatchResult.fromdata(match) for match in match_lst]
    return rtn, err


def world_cup_get_match_result_by_match_id(
        match_id: int) -> (WorldCupMatchResult, int):
    """
    通过比赛id查询世界杯比赛结果
    :param match_id: 比赛id
    :return: 保存比赛结果的类实例，以及错误码
    """
    rtn, err = WorldCupMatchResult(), ErrorCode.ERROR_PASS
    try:
        match = QSF.world_cup_get_match(match_id)[0]
    except IndexError:
        err = ErrorCode.ERROR_EMPTY
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    else:
        rtn.upsert(match)
    return rtn, err


# 2- 查询每届参赛球队 ----------------------------------------------------


def world_cup_get_attend_team_list_by_season(
        _season: int) -> (list, int):
    """
    通过指定赛季，查询参加世界杯球队列表
    :param _season: 指定要查询的season id
    :return: 返回查球队列表

    list中每个元素为WorldCupTeamResult类实例
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        team_lst = QSF.world_cup_get_attend_team_lst_by_season_id(_season)
        if not team_lst:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtn = [WorldCupTeamResult.fromdata(team) for team in team_lst]
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


# 3- 查询每届世界杯的参赛球队的球队大名单 --------------------------------------


def world_cup_get_team_roster_by_season_team_id(
        _season: int, _team) -> (list, int):
    """
    根据指定的赛季和球队id，查询球队大名单
    :param _season: 赛季id
    :param _team: 球队id
    :return: 返回球员信息列表，以及错误码
    返回值list中每个元素为WorldCupPlayerInfo类实例
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        player_lst = QSF.world_cup_get_team_roster_lst_by_season_team(
            _season, _team)
        if not player_lst:
            err = ErrorCode.ERROR_EMPTY
        else:
            en_cn_position = QSF.world_cup_get_cn_position_from_mysql_table()
            for i in range(len(player_lst)):
                player_lst[i]['pos'] = en_cn_position[player_lst[i]['pos']]
            rtn = [WorldCupPlayerInfo.fromdata(player) for player in
                   player_lst]
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err


def world_cup_get_team_roster_by_team_id(_team) -> (list, int):
    """
    根据指定的球队id，查询球队大名单，查最近一次参加世界杯的大名单
    :param _team: 球队id
    :return: 返回球员信息列表，以及错误码
    返回值list中每个元素为WorldCupPlayerInfo类实例
    """
    rtn, err = [], ErrorCode.ERROR_PASS
    try:
        season_id = QSF.world_cup_get_last_season_id_by_team(_team)
        if not season_id:
            err = ErrorCode.ERROR_EMPTY
        else:
            rtn, err = world_cup_get_team_roster_by_season_team_id(
                season_id, _team
            )
    except MySQLError:
        err = ErrorCode.ERROR_MYSQL_ERROR
    except Exception:
        err = ErrorCode.ERROR_UNKNOW
    return rtn, err
