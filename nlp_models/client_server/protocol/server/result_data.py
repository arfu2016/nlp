"""
@Project   : aiball
@Module    : result_data.py
@Author    : Klose [klose@cubee.com]
@Created   : 2018/3/28 13:24
@Desc      : 
"""

from aiball.consts import ServerMsgProtocol
# from aiball.utils.decorators import singleton
from aiball.consts import ProtocolValuePictureType
from aiball.consts import EntityType


class DataItem:
    """
    服务器发送协议：Result/Data/ 中包含项基类
    """

    def export(self) -> dict:
        _dict = dict()
        _dict.update(self.__dict__)
        return _dict

    def export2(self) -> dict:
        _dict = dict()
        _dict.update(self.__dict__)
        keys = list(_dict.keys())
        for key in keys:
            if isinstance(_dict[key], DataItem):
                _dict[key] = _dict[key].export()
        return _dict

    def load(self, src: dict):
        self.__dict__.update(src)


class DataTableItem(DataItem):
    def __init__(self):
        self.value = list()
        self.entity = ""
        self.entity_id = 0
        self.url = None

    def export(self):
        res_ = super().export()
        if "url" in res_ and res_["url"] is None:
            del res_["url"]
        return res_


class DataVideoInfo(DataItem):
    def __init__(self):
        self.FileSize = ""
        self.url = ""
        self.info = ""
        self.desc = ""


class DataChartStatistics(DataItem):
    def __init__(self):
        self.item = ""
        self.away = ""
        self.home = ""
        self.away_team_name = "50%"
        self.away_rate = 0.5
        self.home_team_name = "50%"
        self.home_rate = 0.5
        self.sort = 0


class DataNewsListNews(DataItem):
    def __init__(self):
        self.pic = ""
        self.is_big_pic = 0
        self.rank = 0
        self.link = ""
        self.title = ""
        self.news_id = 0


class DataFixtureData(DataItem):
    def __init__(self):
        self.home_team_id = 0
        self.home_name = ""
        self.match_time = ""
        self.operation = 0
        self.away_name = ""
        self.fav = 0
        self.bg = ""
        self.gms_league_id = 0
        self.status = 1
        self.away_team_id = 0
        self.league_name = ""

    def get_league_name(self):
        if self.gms_league_id == 8:
            return "英超"
        return "UnKnow"

    # def export(self):
    #     res_ = super().export()
    #     res_["league_name"] = self.get_league_name()
    #     return res_



class DataAskBackValueItemPerson(DataItem):
    def __init__(self):
        self.idx = 0
        self.name = ""
        self.number = 0
        self.club = ""
        self.pos = ""


class DataAskBackValueItemTeam(DataItem):
    def __init__(self):
        self.idx = 0
        self.name = ""
        self.league = 0
        self.time = ""


class DataAskBackValue(DataItem):
    def __init__(self):
        self.items = list()
        self.type = ""
        self.title = list()
        self.line = 0

    def append(self, item: DataItem):
        self.items.append(item)

    def export(self):
        _vs = [x.export() for x in self.items]
        rvt = super().export()
        rvt["items"] = _vs
        return rvt


class DataAIButton(DataItem):
    def __init__(self):
        self.world_content = None
        self.button_content = ""
        self.button_pic = ""
        self.button_type = ""
        self.button_order = ""
        self.word_id = None
        self.button_id = 0


class DataAINews(DataItem):
    def __init__(self):
        self.order = 1
        self.content_pool_id = 0
        self.inner_content = dict()
        self.news_id = 0


class ServerMsgResultData:
    """
    服务器发送协议：Result/Data封装基类，所有服务器发送协议数据从该类派生

    类声明所有协议共有getter/setter函数
    """

    protocol = 0

    def __init__(self):
        self._msg = None
        self._team_id = None
        self._num = None
        self._event_type = None
        self._res = None
        self._url = None
        self._news = None
        self._link = None
        self._values = None
        self._away_team_id = None
        self._home_team_id = None
        self._home_name = None
        self._away_name = None
        self._season_id = None
        self._media = None
        self._media_title = None
        self._media_all = None
        self._type = None
        self._pic = None  # 图片地址
        self._title = None  # 标题
        self._player = None  # 球员信息
        self._away_formation = None  # 客队阵容
        self._home_formation = None  # 主队阵容
        self._substitutions = None  # 换人信息
        self._coach_team_h = None  # 主队教练名
        self._coach_team_a = None  # 客队教练名
        self._lineups_bench = None
        self._source = None
        self._event_id = None
        self._match_period = None
        self._home_name = None
        self._team = None
        self._score = None
        self._second = None
        self._feedtype = None
        self._minute = None
        self._owner = None
        self._competition = None
        self._ssid = None
        self._extrainfo = None
        self._origin_type = None
        self._player_name1 = None
        self._player_name2 = None
        self._br_player_1 = None
        self._br_player_2 = None
        self._player1 = None
        self._player2 = None

    @property
    def player_name1(self):
        return self._player_name1

    @player_name1.setter
    def player_name1(self, value):
        self._player_name1 = value

    @property
    def player_name2(self):
        return self._player_name2

    @player_name2.setter
    def player_name2(self, value):
        self._player_name2 = value

    @property
    def br_player_1(self):
        return self._br_player_1

    @br_player_1.setter
    def br_player_1(self, value):
        self._br_player_1 = value

    @property
    def br_player_2(self):
        return self._br_player_2

    @br_player_2.setter
    def br_player_2(self, value):
        self._br_player_2 = value

    @property
    def player1(self):
        return self._player1

    @player1.setter
    def player1(self, value):
        self._player1 = value

    @property
    def player2(self):
        return self._player2

    @player2.setter
    def player2(self, value):
        self._player2 = value

    @property
    def origin_type(self):
        return self._origin_type

    @origin_type.setter
    def origin_type(self, value):
        self._origin_type = value

    @property
    def extrainfo(self):
        return self._extrainfo

    @extrainfo.setter
    def extrainfo(self, value):
        self._extrainfo = value

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, value):
        self._ssid = value

    @property
    def competition(self):
        return self._competition

    @competition.setter
    def competition(self, value):
        self._competition = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, value):
        self._minute = value

    @property
    def feedtype(self):
        return self._feedtype

    @feedtype.setter
    def feedtype(self, value):
        self._feedtype = value

    @property
    def second(self):
        return self._second

    @second.setter
    def second(self, value):
        self._second = value

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        self._team = value

    @property
    def home_name(self):
        return self._home_name

    @home_name.setter
    def home_name(self, value):
        self._home_name = value

    @property
    def match_period(self):
        return self._match_period

    @match_period.setter
    def match_period(self, value):
        self._match_period = value

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, value):
        self._event_id = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def lineups_bench(self):
        return self._lineups_bench

    @lineups_bench.setter
    def lineups_bench(self, value):
        self._lineups_bench = value

    @property
    def substitutions(self):
        return self._substitutions

    @substitutions.setter
    def substitutions(self, value):
        self._substitutions = value

    @property
    def home_formation(self):
        return self._home_formation

    @home_formation.setter
    def home_formation(self, value):
        self._home_formation = value

    @property
    def away_formation(self):
        return self._away_formation

    @away_formation.setter
    def away_formation(self, value):
        self._away_formation = value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    @property
    def pic(self):
        return self._pic

    @pic.setter
    def pic(self, value):
        self._pic = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, value):
        self._media = value

    @property
    def media_title(self):
        return self._media_title

    @media_title.setter
    def media_title(self, value):
        self._media_title = value

    @property
    def protocol_name(self) -> str:
        return self.__class__.__name__

    def export(self) -> dict:
        """
        将实例内所有保护属性转换成字典，转换时不包含第一个"_"
        :return:
        """
        _dict = dict()
        keys = list(self.__dict__.keys())
        for _key in keys:
            try:
                if _key.startswith("_") and not _key.startswith("__"):
                    key = _key[1:]
                    if key != "" and self.__dict__[_key] is not None:
                        _dict[key] = self.__dict__[_key]
            except Exception:
                continue

        return _dict

    def append(self, value):
        pass

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, value):
        self._team_id = value

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    @property
    def event_type(self):
        return self._event_type

    @event_type.setter
    def event_type(self, value):
        self._event_type = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def news(self):
        return self._news

    @news.setter
    def news(self, value):
        self._news = value

    @property
    def away_team_id(self):
        return self._away_team_id

    @away_team_id.setter
    def away_team_id(self, value):
        self._away_team_id = value

    @property
    def home_team_id(self):
        return self._home_team_id

    @home_team_id.setter
    def home_team_id(self, value):
        self._home_team_id = value

    @property
    def home_name(self):
        return self._home_name

    @home_name.setter
    def home_name(self, value):
        self._home_name = value

    @property
    def away_name(self):
        return self._away_name

    @away_name.setter
    def away_name(self, value):
        self._away_name = value

    @property
    def season_id(self):
        return self._season_id

    @season_id.setter
    def season_id(self, value):
        self._season_id = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value


class ServerMsgResultDataMatchIdError(ServerMsgResultData):
    protocol = ServerMsgProtocol.MatchIdError

    def __init__(self):
        super().__init__()
        self._msg = ""

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value


class ServerMsgResultDataParameterError(ServerMsgResultData):
    protocol = ServerMsgProtocol.ParameterError

    def __init__(self):
        super().__init__()
        self._msg = ""


class ServerMsgResultDataEventBind(ServerMsgResultData):
    protocol = ServerMsgProtocol.EventBind

    def __init__(self):
        super().__init__()
        self._team_id = 0
        self._num = 0
        self._event_type = 30


class ServerMsgResultDataEvent(ServerMsgResultData):
    protocol = ServerMsgProtocol.Event

    def __init__(self):
        super().__init__()
        self._feedtype = "delta"
        self._score = {}
        self._match_period = "1H"
        self._type = "0"
        self._away_name = ""
        self._second = "0"
        self._origin_type = "0"
        self._owner = None
        self._minute = "0"
        self._competition = None
        self._player = None
        self._team = "0"
        self._home_name = ""
        self._away_name = ""
        self._msg = ""
        self._event_id = ""
        self._ssid = ""
        self._extrainfo = None
        self._player_name1 = None
        self._player_name2 = None
        self._br_player_1 = None
        self._br_player_2 = None
        self._player1 = None
        self._player2 = None

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if value:
            self._score = dict()
            self._score.update(value)

    def export(self):
        ret = super().export()
        if "source" not in ret:
            ret["source"] = 2

        return ret


class ServerMsgResultDataText(ServerMsgResultData):
    protocol = ServerMsgProtocol.Text

    def __init__(self):
        super().__init__()
        self._msg = ""


class ServerMsgResultDataPicture(ServerMsgResultData):
    protocol = ServerMsgProtocol.Picture

    def __init__(self):
        super().__init__()
        self._link = list()
        self._type = ProtocolValuePictureType(1)

    def append(self, img="", compress_img=""):
        self._link.append({"img": img, "compress_img": compress_img})

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        pass

    @property
    def count(self):
        return len(self._link)

    def export(self):
        ret = super().export()
        if self._type == ProtocolValuePictureType.Multiple:
            ret["count"] = self.count
        return ret


class ServerMsgResultDataChart(ServerMsgResultData):
    protocol = ServerMsgProtocol.Chart

    def __init__(self):
        super().__init__()
        self.__chart = list()

    def append(self, value: DataChartStatistics):
        self.__chart.append(value)

    def export(self):
        self.__chart = sorted(self.__chart, key=lambda x: x.sort)
        return [x.export() for x in self.__chart]


class ServerMsgResultDataTable(ServerMsgResultData):
    protocol = ServerMsgProtocol.Table

    def __init__(self):
        super().__init__()
        self._res = list()

    def export(self):
        return self._res

    def append(self, item: list):
        self._res.append(item)


class ServerMsgResultDataNews(ServerMsgResultData):
    """
    封装单条新闻协议

    ServerMsgResultNews类需要调用下面向个method设置

    self.link = ""
    self.pic = ""
    self.append("")  # 添加图片
    self.title = ""
    self.msg = ""
    例：
    {
            'link': 'http://h5.aiball.ai/#/detail/1469',
            'pic': 'http://static.aiball.ai/upload/c5747e1c8e57b0c7189eb74854b5595e82a9fbf4.jpg',
            'pics': ['http://static.aiball.ai/upload/c5747e1c8e57b0c7189eb74854b5595e82a9fbf4.jpg'],
            'title': '【我要正版球衣】中奖名单（3月5日中奖用户已公布）',
            'msg': '3月5日的获奖用户已经公布啦！看看是不是你！'
        }
    """
    protocol = ServerMsgProtocol.News

    def __init__(self):
        super().__init__()
        self._link = ""
        self._pic = ""
        self._title = ""
        self._msg = ""
        self._pics = list()

    def append(self, value):
        if not self._pics:
            self.pic = value

        self._pics.append(value)


class ServerMsgResultDataNewsList(ServerMsgResultData):
    protocol = ServerMsgProtocol.NewsList

    def __init__(self):
        super().__init__()
        self._msg = ""
        self._url = ""
        self._news = list()

    def append(self, news: DataNewsListNews):
        self._news.append(news.export())


class ServerMsgResultDataFixture(ServerMsgResultData):
    protocol = ServerMsgProtocol.Fixture

    def __init__(self):
        super().__init__()
        self._res = list()
        self._msg = ""

    def export(self):
        return self._res

    def append(self, data: DataFixtureData):
        self._res.append(data.export())


class DataFixtureDataCompetitionValue(DataItem):
    def __init__(self):
        self.league_name = ""
        self.items = list()

    def append(self, item: DataFixtureData):
        self.items.append(item.export())


class DataFixtureDataValues(DataItem):
    def __init__(self):
        self.values = dict()

    def append(self, item: DataFixtureData):
        league_name = item.get_league_name()
        if league_name not in self.values:
            self.values[league_name] = dict()

        item_ = DataFixtureDataCompetitionValue()
        item_.league_name = league_name
        item_.append(item=item)
        self.values[league_name] = item_.export()

    def _clear(self):
        keys = list(self.values.keys())
        for key in keys:
            if not self.values[key]:
                del self.values[key]

    def export(self):
        self._clear()
        keys = list()
        for key in self.values:
            if key == "英超":
                keys.insert(0, self.values[key])
            else:
                keys.append(self.values[key])
        return keys


class ServerMsgResultDataFixtureEx(ServerMsgResultData):
    """
    封装可扩展赛程协议。

    ServerMsgResultDataFixtureEx类需要调用下面几个method进行设置
        ins.msg = str()
        ins.url = ""  # 此处url需要根据league_id进行拼接
        ins.append(DataFixtureData())

    例：
    {
        "msg": "测试比赛",
        "url": "",
        "values": [{
            "items": [{
                "away_name": "",
                "away_team_id": 0,
                "bg": "",
                "fav": 0,
                "gms_league_id": 8,
                "home_name": "AA",
                "home_team_id": 0,
                "league_name": "英超",
                "match_time": "",
                "operation": 0,
                "status": 1
            }],
            "league_name": "英超"
        }]
    }
    """

    protocol = ServerMsgProtocol.FixtureEx

    def __init__(self):
        super().__init__()
        self._msg = ""
        self._values = DataFixtureDataValues()
        self._url = ""

    def append(self, data: DataFixtureData):
        self._values.append(item=data)

    def export(self):
        res_ = super().export()
        res_["values"] = self._values.export()
        return res_


class ServerMsgResultDataFormation(ServerMsgResultData):
    """
    封装球队阵容协议。

    ServerMsgResultDataFormation类需要调用下面几个method进行设置
        ins.away_team_id = int()
        ins.substitutions = dict()
        ins.home_name = str()
        ins.away_name = str()
        ins.away_formation = list()  # ["4", "5", "1"]
        ins.home_formation = list()
        ins.player = dict()
        ins.home_team_id = int()
        ins.away_team_id = int()
        ins.coach_team_h = str()
        ins.coach_team_a = str()
        ins.lineups_bench = list()
        ins.type = int()

    例：
        {
            "away_team_id": 682,
            "substitutions": {
                "away": [{
                    "xia_shirtnumber": "20",
                    "minute": 60,
                    "xia_person": "冈崎慎司",
                    "shang_person": "伊赫纳乔",
                    "shang_shirtnumber": "8"
                }],
                "home": [{
                    "xia_shirtnumber": "20",
                    "minute": 59,
                    "xia_person": "科里佐维亚克",
                    "shang_person": "菲尔德",
                    "shang_shirtnumber": "28"
                }]
            },
            "home_name": "西布罗姆维奇",
            "away_formation": ["4", "5", "1"],
            "player": {
                "away": [{
                    "position_x": "GK",
                    "position_y": "C",
                    "person": "舒梅切尔",
                    "team_id": "682",
                    "shirtnumber": "1",
                    "replaced": 0,
                    "person_id": "2841"
                }],
                "home": [{
                    "position_x": "GK",
                    "position_y": "C",
                    "person": "福斯特",
                    "team_id": "678",
                    "shirtnumber": "1",
                    "replaced": 0,
                    "person_id": "2528"
                }]
            },
            "home_team_id": 678,
            "coach_team_h": "帕杜",
            "home_formation": ["4", "3", "3"],
            "away_name": "莱斯特城",
            "coach_team_a": "皮埃尔",
            "lineups_bench": [{
                "shirtnumber": "13",
                "replaced": 0,
                "person": "迈希尔",
                "person_id": "15756",
                "team_id": "678"
            }],
            "type": 2
        }
    """
    protocol = ServerMsgProtocol.Formation

    def __init__(self):
        super().__init__()
        self._away_team_id = int()
        self._substitutions = dict()
        self._home_name = str()
        self._away_name = str()
        self._away_formation = list()  # ["4", "5", "1"]
        self._home_formation = list()
        self._player = dict()
        self._home_team_id = int()
        self._away_team_id = int()
        self._coach_team_h = str()
        self._coach_team_a = str()
        self._lineups_bench = list()
        self._type = int()


class ServerMsgResultDataTableEx(ServerMsgResultData):
    """
    封装可扩展表格协议，可用于排行榜等需要表格的协议。

    ServerMsgResultDataTableEx类需要调用下面几个method进行设置
        ins.msg = str()
        ins.column("排名,球队,场次,积分".split(","))
        ins.append([1, "曼城", 29, 78])
        ins.type = 1

    例：
    {
        "msg": "2060协议，表格列数不固定，最多有5个",
        "title": ["排名", "球队", "场次", "积分"],
        "value": [
            [1, "曼城", 29, 78],
            [2, "曼联", 29, 62],
            [3, "利物浦", 29, 60],
            [4, "托特纳姆热刺", 29, 58],
            [5, "切尔西", 29, 53]
        ],
        "type": 1
    }
    """
    protocol = ServerMsgProtocol.TableEx

    def __init__(self):
        super().__init__()
        self._msg = ""
        self._title = list()
        self._value = list()
        self._type = 1

    def append(self, value):
        self._value.append(value)

    def column(self, columns: list):
        self._title.clear()
        self._title.extend(columns)

    def add_column(self, column):
        self._title.append(column)


class ServerMsgResultDataTableSupper(ServerMsgResultData):
    protocol = ServerMsgProtocol.TableSupper

    def __init__(self):
        super().__init__()
        self._msg = ""
        self._title = list()
        self._values = list()
        self._type = 1

    def column(self, columns: list):
        self._title.clear()
        self._title.extend(columns)

    def append(self, value: DataTableItem):
        self._values.append(value.export())


class ServerMsgResultDataMatchResult(ServerMsgResultData):
    protocol = ServerMsgProtocol.MatchResult

    def __init__(self):
        super().__init__()
        self._msg = ""
        self._title = list()
        self._values = list()
        self._type = 1

    def column(self, columns: list):
        self._title.clear()
        self._title.extend(columns)

    def append(self, value: DataTableItem):
        self._values.append(value.export())


class ServerMsgResultDataVideo(ServerMsgResultData):
    """
    封装视频协议。

    ServerMsgResultDataVideo类需要调用下面几个method进行设置
    (GateWay发送的Video协议字段可能会更多)
        ins.title = ""
        ins.media = ""
        ins.media_title = ""
        ins.link = {"compress_img": "", "img": ""}
        ins.append(DataVideoInfo.export())

    media_all为不同分辨率视频全集，默认使用media_all[0]数据
    如果media_all为空，则使用media字段

    link为预图地址，只使用array第一个元素

    title为标题内容，media_title为多杂体内容


    例：
        {
        "link": [{
            "compress_img": "http://static.aiball.ai/upload/d.jpg",
            "img": "http://static.aiball.ai/upload/da.jpg?"
        }],
        "media_title": "超级无敌大回环界外球",
        "type": 1,
        "title": "美国乙级联赛球队俄克拉荷马能源主帅让球员在训练中练习空翻掷外球",
        "media": "http://video/3d911c3e01f734158fc720c2c7f18a35.mp4",
        "count": 1,
        "media_all": [{
            "FileSize": "5143604",
            "url": "http://Act-ss-mp4-ld/3d911c3e01f734158fc720c2c7f18a35.mp4",
            "info": "640x360",
            "desc": "标清"
        },
        {
            "FileSize": "9632372",
            "url": "http://3d911c3e01f734158fc720c2c7f18a35.mp4",
            "info": "848x478",
            "desc": "高清"
        },
        {
            "FileSize": "20847111",
            "url": "http://Act-ss-mp4-hd/3d911c3e01f734158fc720c2c7f18a35.mp4",
            "info": "1280x720",
            "desc": "超清"
        }]
    }
    """
    protocol = ServerMsgProtocol.Video

    def __init__(self):
        super().__init__()
        self._type = 1
        self._count = 0
        self._title = ""
        self._media = ""
        self._media_all = list()
        self._link = [""]
        self._media_title = ""

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = [value]

    def append(self, value: dict):
        self._media_all.append(value)


class ServerMsgResultDataAudio(ServerMsgResultData):
    """
    封装音频协议。

    ServerMsgResultDataAudio类需要调用下面几个method进行设置
    (GateWay发送的Audio协议字段可能会更多)
        ins.title = ""
        ins.media = ""
        ins.media_title = ""

    media_all为不同分辨率视频全集，默认使用media_all[0]数据
    如果media_all为空，则使用media字段

    link为预图地址，只使用array第一个元素


    例：
        {
            'title': '红色荣耀第37期：曼联进入黎明前最后的黑暗',
            'media': 'http: //static.aiball.ai/robot/video/f85f3c67d7be891dbb0b65f5da7cd3f1.mp3',
            'media_title': '红色荣耀37、曼联进入黎明前最后的黑暗',
        }
    """
    protocol = ServerMsgProtocol.Audio

    def __init__(self):
        super().__init__()
        self._title = ""
        self._media = ""
        self._media_title = ""


class ServerMsgResultDataPictureText(ServerMsgResultData):
    """
    封装图文协议。

    ServerMsgResultDataPictureText类需要调用下面几个method进行设置
    (GateWay发送的Audio协议字段可能会更多)
        ins.title = ""  # 文字内容
        ins.link = {"compress_img": "", "img": ""}
        ins.url = ""

    url为文字内容点击跳转地址（如新闻详情页）
    link为预图地址，只使用array第一个元素


    例：
        {
            'title': '红色荣耀第37期：曼联进入黎明前最后的黑暗',
            'media': 'http: //static.aiball.ai/robot/video/f85f3c67d7be891dbb0b65f5da7cd3f1.mp3',
            'media_title': '红色荣耀37、曼联进入黎明前最后的黑暗',
        }
    """
    protocol = ServerMsgProtocol.PictureText

    def __init__(self):
        super().__init__()
        self._title = ""
        self._link = list()
        self._url = ""

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = [value]


class EntityData(DataItem):
    """
    描术实体类型

    需要设置参数
    id: 实体id
    name: 实体名称
    type: 实体类型，1:EntityType.Person, 2:EntityType.Team, 3:EntityType.Venue...

    e = EntityData()
    e.id = 1102
    e.name = 上古时期
    e.type = EntityType.Story  # 词条
    """
    def __init__(self, _id=0, _name="", _type=0):
        self.id = _id
        self.name = _name
        self.type = _type

    def export2(self) -> dict:
        res_ = super().export2()
        keys = list(res_.keys())
        for key in keys:
            if not res_[key]:
                del res_[key]
        return res_


class PlayerClubDataEntity(EntityData):
    """
    描术球员卡牌中额外信息中，俱乐部数据中每一条目

    需要设置的参数有：
    id: 设置为当前球员所在俱乐部id
    name: 设置为当前球员所在俱乐部名称
    value: list类型，表格中每一行

    p = PlayerClubDataEntity()
    p.value = ["17-18", "切尔西", "32(15)", 15, 12]
    p.name = "切尔西"
    p.id = 661
    """
    def __init__(self):
        super().__init__()
        self.value = list()
        self.url = ""
        self.type = 2


class BasicList(DataItem):
    """
    卡牌信息中基础列表类封装

    需要设置的参数有
    text: 需要显示的信息
    title: 标格的标题栏（一个列表）
    self.append(): 添加表格条目

    p = PlayerClubDataEntity()
    b = BasicList()
    b.text = "齐达内俱乐部数据"
    b.title = ["赛季", "俱乐部", "出场", "进球", "助攻"]
    b.append(p)
    """
    def __init__(self):
        self.text = ""
        self.title = list()
        self.values = list()
        self.style = 0

    def append(self, value: EntityData):
        self.values.append(value)

    def export(self):
        res_ = super().export()
        res_["values"] = [x.export() for x in self.values]
        return res_

    def export2(self):
        res_ = super().export()
        res_["values"] = [x.export2() for x in self.values]
        return res_


class StoryItem(EntityData):
    """
    描术卡牌数据中小故事信息

    需要设置参数
    id: 设置为当前小故事id（词条id）
    type: 词条类型（实体类型），1球员，2球队，3球场，4联赛，10其他（运营词汇等）
    name: 当前词条标签
    value: 词条内容信息
    self.append(): 添加其他标签信息

    t = EntityData()
    t.id = 1001
    t.name = "基本概况"
    t.type = EntityType.Story

    s = StoryItem()
    s.id = 1001
    s.name = "上古时期"
    s.type = EntityType.Story
    s.append(t)
    """
    def __init__(self):
        super().__init__()
        self.has_next = False
        self.value = ""
        self.tags = list()
        self.pics = list()

    def append(self, value: EntityData):
        self.tags.append(value.export2())


class PlayerCardExtra:
    """
    描术球员卡牌信息中额外信息

    需要设置属性
    story: 当前球员词条信息
    append_club(): 添加俱乐部信息
    append_national(): 添加国家队信息

    p = PlayerCardExtra()
    p.story = StoryItem()
    club = PlayerClubDataEntity()

    national = PlayerClubDataEntity()
    p.append_club(club)
    p.append_national(national)

    """
    def __init__(self):
        self.story = StoryItem()
        self.data_club = BasicList()
        self.data_national = BasicList()

    def set_text(self, _text: str, _club: bool=True):
        if _club:
            self.data_club.text = _text
        else:
            self.data_national.text = _text

    def set_title(self, _title: list, _club: bool=True):
        if _club:
            self.data_club.title = _title
        else:
            self.data_national.title = _title

    def append(self, value: PlayerClubDataEntity, _club: bool=True):
        if _club:
            self.data_club.append(value)
        else:
            self.data_national.append(value)

    def export2(self):
        return {
            "story": self.story.export2(),
            "datas": {
                "club": self.data_club.export2(),
                "national": self.data_national.export2()
            }
        }


class PlayerCardBasic(EntityData):
    """
    描术球员基本介绍

    需要设置属性
    id: 当前球员id号
    name: 当前球员名称（中文）
    en_name: 当前球员英文名
    nationality: 当前球员国籍
    age: 当前球员年龄
    height: 当前球员身高
    weight: 当前球员体重
    pos: 当前球员位置
    foot: 当前球员惯用脚
    birth: 当前球员出生日期
    club: 当前球员所属俱乐部

    p = PlayerCardBasic()
    p.id = 549
    p.name = "齐达内"
    p.en_name = "Z. Zidane"
    p.nationality = "法国"
    p.age = 5
    p.height = 5
    p.weight = 5
    p.pos = "中场"
    p.foot = "右"
    p.birth = "1972-06-23"
    p.club = EntityData()  # 俱乐部实体
    """
    def __init__(self):
        super().__init__()
        self.type = EntityType.Person
        self.en_name = ""
        self.nationality = ""
        self.age = 0
        self.height = 0
        self.pos = ""
        self.foot = ""
        self.birth = ""
        self.club = EntityData()


class ServerMsgResultEntityPlayerCard(ServerMsgResultData):
    """
    描术球员卡片信息

    需要调用下面方法添加数据
    self.basic = PlayerCardBasic()
    self.extra = PlayerCardExtra()

    p = ServerMsgResultEntityPlayerCard()
    b = PlayerCardBasic()
    # 初始化b
    e = PlayerCardBasic()
    # 初始化b

    p.basic = b
    p.extra = e
    """
    protocol = ServerMsgProtocol.EntityPlayerCard

    def __init__(self):
        super().__init__()
        self._basic = None
        self._link = None
        self._extra = None
        self._msg = ""


    @property
    def basic(self):
        return self._basic

    @basic.setter
    def basic(self, value: PlayerCardBasic):
        self._basic = value
        self._link = {"value": "xx?id=%d" % value.id}

    @property
    def extra(self):
        return self._extra

    @extra.setter
    def extra(self, value: PlayerCardExtra):
        self._extra = value

    def export(self) -> dict:
        res_ = dict()
        res_["msg"] = self._msg
        if self._basic:
            res_["basic"] = self._basic.export2()
            res_["link"] = {"value": "xx?id=%d" % self._basic.id}
        if self._extra:
            res_["extra"] = self._extra.export2()
        return res_


class ServerMsgResultDataHelp(ServerMsgResultData):
    protocol = ServerMsgProtocol.Help

    def __init__(self):
        super().__init__()
        self._link = ""
        self._msg = ""


class ServerMsgResultDataAskBack(ServerMsgResultData):
    protocol = ServerMsgProtocol.AskBack

    def __init__(self):
        super().__init__()
        self._msg = ""
        self._values = list()

    def append(self, value: DataAskBackValue):
        self._values.append(value.export())


class ServerMsgResultDataNewsAbstract(ServerMsgResultData):
    protocol = ServerMsgProtocol.NewsAbstract

    def __init__(self):
        super().__init__()


class ServerMsgResultDataAINews(ServerMsgResultData):
    protocol = ServerMsgProtocol.AINews

    def __init__(self):
        super().__init__()
        self._news = DataAINews()
        self._buttons = list()

    def add_button(self, button: DataAIButton):
        self._buttons.append(button)

    def export(self):
        _buttons = [x.export() for x in self._buttons]
        return {
            "news": self._news.export(),
            "buttons": _buttons
        }


# @singleton
class ResultDataFactory:
    _result_data_list = [
        ServerMsgResultDataMatchIdError,
        ServerMsgResultDataParameterError,
        ServerMsgResultDataEventBind,
        ServerMsgResultDataEvent,
        ServerMsgResultDataText,
        ServerMsgResultDataPicture,
        ServerMsgResultDataChart,
        ServerMsgResultDataTable,
        ServerMsgResultDataNews,
        ServerMsgResultDataNewsList,
        ServerMsgResultDataFixture,
        ServerMsgResultDataFormation,
        ServerMsgResultDataTableEx,
        ServerMsgResultDataFixtureEx,
        ServerMsgResultDataTableSupper,
        ServerMsgResultDataVideo,
        ServerMsgResultDataAudio,
        ServerMsgResultDataPictureText,
        ServerMsgResultDataHelp,
        ServerMsgResultDataAskBack,
        ServerMsgResultDataNewsAbstract,
        ServerMsgResultDataAINews
    ]

    def __init__(self):
        self._protocol_table = dict()
        for rd in self._result_data_list:
            code = rd.protocol
            self._protocol_table[code] = rd

    def create(self, code) -> ServerMsgResultData:
        """
        生产code对应的ServerMsgResultData实例
        :param code: 协议号，code值不支持会抛出KeyError或ValueError
        :return:
        """
        return self._protocol_table[ServerMsgProtocol(code)]()


if __name__ == "__main__":
    import json
    factory = ResultDataFactory()
    n = 1
    for code in ServerMsgProtocol:
        try:
            res = factory.create(code)
            print("\n%d. %s\n" % (n, ServerMsgProtocol(res.protocol).name))
            print("\t%d.1 数据结构\n" % n)
            print("\t```json\n\t/**\n\t * code = %d(%s)\n\t */" % (code, ServerMsgProtocol(res.protocol).name))

            print(json.dumps(res.export(), indent=4, ensure_ascii=False, sort_keys=True))
            print("\t```\n\n\t%d.2 字段说明\n\n" % n)
        except KeyError:
            print("\n%d. code %d (%s) is not support" % (n, code, ServerMsgProtocol(code).name))

        n += 1
